import itertools
import logging
try:
    import gurobipy
except ImportError:
    pass
import time
try:
    import z3
except ImportError:
    pass

try:
    import pycryptosat
except ImportError:
    pass

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class Solver(object):
    def __init__(self):
        self.candidates = dict()
        self.reverse_candidates = dict()
        self.variable_index = 1
        self.num_constraints = 0

    def add_constraint(self, disable=None, enable=None):
        self.num_constraints += 1
        logger.debug("Disabling {0}".format(disable))
        logger.debug("Enabling {0}".format(enable))

    def associate_candidate_with_last_variable(self, candidate):
        self.candidates[candidate] = self.last_variable
        self.reverse_candidates[str(self.last_variable)].append(candidate)

    def update(self):
        pass


class Z3Solver(Solver):
    def __init__(self, random_seed=0):
        super(Z3Solver, self).__init__()
        z3.set_param('smt.random_seed', random_seed)
        self.z3_solver = z3.Solver()

    def add_constraint(self, disable=None, enable=None):
        super(Z3Solver, self).add_constraint(disable=disable, enable=enable)
        disable = [] if disable is None else disable
        enable = [] if enable is None else enable
        self.z3_solver.add(z3.Or(*([z3.Not(self.candidates[edge]) for edge in disable] +
                                   [self.candidates[edge] for edge in enable])))

    def add_determinism_constraints(self, per_state_label_candidate_edges):
        for edges in per_state_label_candidate_edges.values():
            for edge1, edge2 in itertools.combinations(edges, 2):
                self.z3_solver.add(z3.Not(z3.And(self.candidates[edge1], self.candidates[edge2])))

    def add_input_output_state_constraint(self, input_candidates, output_candidates):
        for candidate1 in input_candidates:
            for candidate2 in output_candidates:
                logger.debug("Not {} and {}".format(candidate1, candidate2))
                self.z3_solver.add(z3.Not(z3.And(self.candidates[candidate1], self.candidates[candidate2])))

    def add_variable(self, candidate):
        variable = z3.Bool(self.variable_index)
        self.candidates[candidate] = variable
        self.reverse_candidates[str(variable)] = [candidate]
        self.last_variable = variable
        self.last_variable_index = self.variable_index
        self.variable_index += 1

    def solve(self):
        t1 = time.time()
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Z3 solver result is {}.".
                         format(self.z3_solver.check()))
        if self.z3_solver.check() == z3.unsat:
            return False
        t2 = time.time()
        logger.info("Solver took {0} seconds.".format(t2 - t1))
        model = self.z3_solver.model()
        new_transitions = []
        for variable in model:
            if z3.is_true(model[variable]):
                new_transitions += self.reverse_candidates[str(variable)]
        return new_transitions

class CryptoSolver(Solver):
    def __init__(self):
        super(CryptoSolver, self).__init__()
        self.crypto_solver = pycryptosat.Solver()

    def add_constraint(self, disable=None, enable=None):
        super(CryptoSolver, self).add_constraint(disable=disable, enable=enable)
        disable = [] if disable is None else disable
        enable = [] if enable is None else enable
        self.crypto_solver.add_clause([-self.candidates[edge] for edge in disable] +
                                      [self.candidates[edge] for edge in enable])

    def add_determinism_constraints(self, per_state_label_candidate_edges):
        for edges in per_state_label_candidate_edges.values():
            for edge1, edge2 in itertools.combinations(edges, 2):
                self.crypto_solver.add_clause([-self.candidates[edge1], -self.candidates[edge2]])

    def add_input_output_state_constraint(self, input_candidates, output_candidates):
        for candidate1 in input_candidates:
            for candidate2 in output_candidates:
                logger.debug("Not {} and {}".format(candidate1, candidate2))
                self.crypto_solver.add_clause([-self.candidates[candidate1], -self.candidates[candidate2]])

    def add_variable(self, candidate):
        variable = self.variable_index
        self.candidates[candidate] = variable
        self.reverse_candidates[str(variable)] = [candidate]
        self.last_variable = variable
        self.last_variable_index = self.variable_index
        self.variable_index += 1

    def solve(self):
        t1 = time.time()
        sat, solution = self.crypto_solver.solve()
        t2 = time.time()
        logger.info("Solver took {0} seconds.".format(t2 - t1))
        if not sat:
            return False
        new_transitions = []
        for variable, value in enumerate(solution[1:], 1):
            if value:
                new_transitions += self.reverse_candidates[str(variable)]
        return new_transitions

class Z3MinimumSolver(Z3Solver):
    def __init__(self, random_seed=0):
        super(Z3MinimumSolver, self).__init__(random_seed)
        self.edges_bound = 0
        self.edge_indicators = []
        self.indicator_sum = None
        self.bound_propositional_variable = None

    def add_variable(self, candidate):
        super(Z3MinimumSolver, self).add_variable(candidate)
        indicator = z3.Int('i{}'.format(self.variable_index))
        variable = z3.Bool(self.variable_index - 1)
        self.edge_indicators.append(indicator)
        self.z3_solver.add(z3.Implies(variable, indicator == 1))
        self.z3_solver.add(indicator >= 0)

    def solve(self):
        t1 = time.time()
        while True:
            if self.z3_solver.check(self.bound_propositional_variable) == z3.unsat:
                self.edges_bound += 1
                self.bound_propositional_variable = z3.Bool('bound{}'.format(self.edges_bound))
                self.z3_solver.add(z3.Implies(self.bound_propositional_variable,
                                              self.indicator_sum == self.edges_bound))
                if self.edges_bound > self.variable_index:
                    return False
            else:
                break
        t2 = time.time()
        logger.info("Solver took {0} seconds.".format(t2 - t1))
        model = self.z3_solver.model()
        new_transitions = []
        for variable in model:
            if z3.is_true(model[variable]):
                if str(variable) in self.reverse_candidates:
                    new_transitions += self.reverse_candidates[str(variable)]
        return new_transitions

    def update(self):
        self.indicator_sum = z3.Sum(self.edge_indicators)
        self.bound_propositional_variable = z3.Bool('bound{}'.format(self.edges_bound))
        self.z3_solver.add(z3.Implies(self.bound_propositional_variable,
                                      self.indicator_sum == self.edges_bound))


class Z3SolverWithRelevancyPropagation(Z3Solver):
    def __init__(self, random_seed=0):
        super(Z3SolverWithRelevancyPropagation, self).__init__(random_seed)
        self.z3_solver = z3.SimpleSolver()
        self.z3_solver.set(auto_config=False, relevancy=2)


class Z3SolverManualMinimal(Z3Solver):
    def solve(self):
        t1 = time.time()
        if self.z3_solver.check() == z3.unsat:
            return False
        model = self.z3_solver.model()
        true_variables = []
        false_variables = []
        for edges in self.reverse_candidates.values():
            edge = edges[0]
            variable = self.candidates[edge]
            if z3.is_true(model[variable]):
                true_variables.append(variable)
            else:
                false_variables.append(variable)
        logger.info("Initial model has {} edges".format(len(true_variables)))
        logger.debug("True variables {}".format([str(t) for t in true_variables]))
        logger.debug("False variables {}".format(false_variables))
        while True:
            logger.debug("starting")
            is_minimal = True
            for variable in true_variables:
                logger.debug("Checking if %s is redundant", variable)
                new_true_variables = []
                new_false_variables = list(false_variables)
                for true_var in true_variables:
                    if str(true_var) != str(variable):
                        new_true_variables.append(true_var)
                new_false_variables.append(variable)
                formula = (new_true_variables +
                           [z3.Not(f) for f in new_false_variables])
                self.z3_solver.push()
                self.z3_solver.add(z3.And(*formula))
                if self.z3_solver.check() == z3.sat:
                    true_variables = new_true_variables
                    false_variables = new_false_variables
                    logger.debug("Variable %s was found redundant", variable)
                    is_minimal = False
                else:
                    logger.debug("Variable %s might not be redundant", variable)
                self.z3_solver.pop()
            if is_minimal:
                break

        t2 = time.time()
        logger.info("Final model has {} edges".format(len(true_variables)))
        logger.info("Solver took {0} seconds.".format(t2 - t1))

        new_transitions = []
        for variable in true_variables:
            new_transitions += self.reverse_candidates[str(variable)]
        return new_transitions


class Z3SolverOpt(Z3Solver):
    def __init__(self, random_seed=0):
        super(Z3SolverOpt, self).__init__(random_seed)
        self.z3_solver = z3.Optimize()

    def add_variable(self, candidate):
        super(Z3SolverOpt, self).add_variable(candidate)
        self.z3_solver.add_soft(z3.Not(self.last_variable))


class GurobiSolver(Solver):
    def __init__(self):
        super(GurobiSolver, self).__init__()
        self.ilp_problem = gurobipy.Model("sat")
        self.ilp_problem.setParam('OutputFlag', False)
        self.negative_candidates = dict()
        self.reverse_negative_candidates = dict()
        self.num_constraints = 0

    def add_constraint(self, disable=[], enable=[]):
        super(GurobiSolver, self).add_constraint(disable=disable, enable=enable)
        self.ilp_problem.addConstr(sum([self.negative_candidates[edge] for edge in disable] +
                                       [self.candidates[edge] for edge in enable]) >= 1)

    def add_determinism_constraints(self, per_state_label_candidate_edges):
        for edges in per_state_label_candidate_edges.values():
            for edge1, edge2 in itertools.combinations(edges, 2):
                self.ilp_problem.addConstr(self.negative_candidates[edge1] + self.negative_candidates[edge2] >= 1)

    def add_input_output_state_constraint(self, input_candidates, output_candidates):
        self.ilp_problem.addConstr(sum([self.candidates[candidate] for candidate in input_candidates]) *
                                   sum([self.candidates[candidate] for candidate in output_candidates]) == 0)

    def add_variable(self, candidate):
        x = self.ilp_problem.addVar(vtype=gurobipy.GRB.BINARY, name='x%d' % self.variable_index)
        xnot = self.ilp_problem.addVar(vtype=gurobipy.GRB.BINARY, name='x%dnot' % self.variable_index)
        self.candidates[candidate] = x
        self.negative_candidates[candidate] = xnot
        self.reverse_candidates['x%d' % self.variable_index] = [candidate]
        self.reverse_negative_candidates['x%dnot' % self.variable_index] = [candidate]
        self.last_variable = x
        self.last_negative_variable = xnot
        self.last_variable_index = self.variable_index
        self.variable_index += 1

    def associate_candidate_with_last_variable(self, candidate):
        self.candidates[candidate] = self.last_variable
        self.negative_candidates[candidate] = self.last_negative_variable
        self.reverse_candidates['x%d' % self.last_variable_index].append(candidate)
        self.reverse_negative_candidates['x%dnot' % self.last_variable_index].append(candidate)

    def solve(self):
        t1 = time.time()
        self.ilp_problem.optimize()
        t2 = time.time()
        logger.info("Solver took {0} seconds.".format(t2 - t1))
        if self.ilp_problem.getAttr('Status') == gurobipy.GRB.INFEASIBLE:
            logger.info("ILP solver says infeasible")
            return False
        new_transitions = []
        for variable in self.ilp_problem.getVars():
            if variable.x > 0 and not variable.varName.encode('ascii').endswith("not"):
                if not set(self.reverse_candidates[variable.varName.encode('ascii')]).issubset(set(new_transitions)):
                    new_transitions += self.reverse_candidates[variable.varName.encode('ascii')]
        return new_transitions

    def update(self):
        self.ilp_problem.update()
        seen_edges = []
        for edge in self.candidates:
            if edge not in seen_edges:
                self.ilp_problem.addConstr(self.candidates[edge] + self.negative_candidates[edge] == 1)
            seen_edges.append(edge)
        self.ilp_problem.setObjective(sum([self.candidates[e] for e in self.candidates]), gurobipy.GRB.MINIMIZE)
