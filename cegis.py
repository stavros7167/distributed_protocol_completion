"""
TODO: move candidate generation in solver
"""
import itertools
import networkx
import logging

import product
import cegis_solver
import incomplete_product
import util


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def add_determinism_constraints(solver, automata):
    # determinism constraints
    # TODO check if this is correct when output transitions are allowed.
    logger.debug("Adding determinism constraints")
    for a in automata:
        per_state_label_candidate_edges = {}
        for state1, label, state2 in a.candidate_edges():
            assert (a.name, state1, label, state2) in solver.candidates
            if (state1, label) not in per_state_label_candidate_edges:
                per_state_label_candidate_edges[(state1, label)] = []
            per_state_label_candidate_edges[(state1, label)].append((a.name, state1, label, state2))
        solver.add_determinism_constraints(per_state_label_candidate_edges)

        # for a specific state, if there are both input and output candidates leaving the state
        # then a completion has to either pick output or input transitions
        for state in a.states():
            if not a.is_input_state(state) and not a.is_output_state(state) and not 'final' in a.node[state]:
                logger.debug("Adding constraints for {}".format(state))
                input_candidates, output_candidates = [], []
                for start, label, end in a.candidate_edges_from_state(state):
                    if label.endswith('?'):
                        input_candidates.append((a.name, start, label, end))
                    elif label.endswith('!'):
                        output_candidates.append((a.name, start, label, end))
                logger.debug("Input candidates are {}".format(input_candidates))
                logger.debug("Output candidates are {}".format(output_candidates))
                solver.add_input_output_state_constraint(input_candidates, output_candidates)

                # for a specific state, no two output transitions can be enabled
                for candidate1, candidate2 in itertools.combinations(output_candidates, 2):
                    solver.add_constraint(disable=[candidate1, candidate2])


def synthesize(p, solver_type, solutions_file, seed, print_dead_annotation,
               snb=False, snb_messages=[], all=False):
    """
    Args:
      - snb: if set then strong non-blockingness will be used as a requirement
        during synthesis and will be satisfied by all returned solutions.
      - snb_messages: messages on which to enforce strong non-blockingness, it
        is ignored if snb is False.
    """
    num_solutions = 0

    # non_monitors_product is only needed for dead edge detection.
    non_monitors = [auto for auto in p.automata if not auto.is_monitor]
    non_monitors_product = product.Product(non_monitors)
    try:
        synthesizer = synthesize_all(p, solver_type, seed, snb, snb_messages)
        while True:
            solution = next(synthesizer)
            edges, results = solution
            if type(edges) == str:
                message = edges
                print(message)
                return
            num_solutions += 1
            print "SOLUTION #{} FOUND:".format(num_solutions)
            if solutions_file is not None:
                solutions_file.write(
                    "** Solution {} **\n".format(num_solutions))

            dead_edges = []
            if print_dead_annotation:
                non_monitors_product.add_automata_edges_by_name(edges)
                dead_transitions_map = non_monitors_product.dead_automata_transitions()
                for auto_name, source, label, target in edges:
                    auto = non_monitors_product.automaton_by_name(auto_name)
                    if (source, label, target) in dead_transitions_map[auto]:
                        dead_edges.append((auto_name, source, label, target))
                non_monitors_product.remove_automata_edges_by_name(edges)
            for edge in sorted(edges):
                if solutions_file is not None:
                    solutions_file.write("{}".format(edge))
                    if print_dead_annotation and edge in dead_edges:
                        solutions_file.write(' * dead *')
                    solutions_file.write('\n')
            if solutions_file is not None:
                solutions_file.write("{}\n".format(results))
                solutions_file.flush()
            if not all:
                return edges
    except StopIteration:
        return None


def synthesize_all(p, solver_type, seed, snb, snb_messages):
    """
    Args:
      - p: product automaton whose constituents include process, environment,
        and monitor automata.
      - solver_type: one of guorbi, z3, z3minimum, z3rel, z3manualminimal, z3opt
        used to create the right instance of cegis solver. Raises ValueError
        exception if not one of the options listed above.
      - snb: if set then strong non-blockingness will be used as a requirement
        together with deadlock-freedom and safety/liveness monitor emptiness.
      - snb_messages: messages on which to enforce non blockingness, it will be
        ignored if snb is False.
    """
    if solver_type == 'gurobi':
        solver = cegis_solver.GurobiSolver()
    elif solver_type == 'z3':
        solver = cegis_solver.Z3Solver(seed)
    elif solver_type == 'z3minimum':
        solver = cegis_solver.Z3MinimumSolver(seed)
    elif solver_type == 'z3rel':
        solver = cegis_solver.Z3SolverWithRelevancyPropagation(seed)
    elif solver_type == 'z3manualminimal':
        solver = cegis_solver.Z3SolverManualMinimal(seed)
    elif solver_type == 'z3opt':
        solver = cegis_solver.Z3SolverOpt(seed)
    elif solver_type == "crypto":
        solver = cegis_solver.CryptoSolver()
    else:
        raise ValueError(
            "Solver type not recognized: {}".format(solver_type))

    logger.debug("Product equivalent automata: %s", p.equivalent_automata)
    if p.equivalent_automata == []:
        automata = [a for a in p.automata if not a.is_environment]
    else:
        automata = [a for a in p.automata
                    if (not a.is_environment and
                        a not in p.equivalent_automata)]
        automata.append(p.equivalent_automata[0])
    deadlock_product_automata = [a for a in p.automata if not a.is_monitor]
    safety_monitors = [a for a in p.automata if a.is_safety]
    safety_product_automata = [deadlock_product_automata + [a]
                               for a in safety_monitors]
    liveness_monitors = [a for a in p.automata if a.is_liveness]
    liveness_product_automata = [deadlock_product_automata + [a]
                                 for a in liveness_monitors]
    main_product = product.Product(deadlock_product_automata)
    safety_products = [product.Product(aa)
                       for aa in safety_product_automata]
    liveness_products = [product.Product(aa)
                         for aa in liveness_product_automata]

    deadlocks = main_product.deadlock_states()
    blocking_states = []
    if snb:
        blocking_states = main_product.strong_blocking_states(snb_messages)
    is_safe = all(safety_product.is_safe() for safety_product in safety_products)
    is_live = all(len(liveness_product.strong_fair_cycles()) == 0
                  for liveness_product in liveness_products)

    # If a state has no transition (output or input) we assume that it could be
    # input and hence state is not input enabled.
    is_input_enabled = all(a.state_neighbors.get(state, {}).get(message + '?', []) != []
                           for a in automata
                           for message in a.input_enabled
                           for state in a.states()
                           if not a.is_output_state(state))

    if (len(deadlocks) == 0 and len(blocking_states) == 0 and is_safe and
            is_live and is_input_enabled):
        yield ('Nothing to synthesize: given protocol already satisfies the '
               'requirements.', None)
        return

    logger.debug("Creating candidate transition variables")
    for a in automata:
        for start, label, end in a.candidate_edges():
            solver.add_variable((a.name, start, label, end))
            logger.debug("Adding variable for transitition {} to {} "
                         "on {} in {}".format(start, end, label, a.name))
            if a in p.equivalent_automata:
                b = p.equivalent_automata[1]
                start2 = util.switch_strings(start, p.equivalent_names[0], p.equivalent_names[1])
                label2 = util.switch_strings(label, p.equivalent_names[0], p.equivalent_names[1])
                end2 = util.switch_strings(end, p.equivalent_names[0], p.equivalent_names[1])
                solver.associate_candidate_with_last_variable((b.name, start2, label2, end2))
    logger.debug("# of variables {0}".format(len(set([str(v) for v in solver.candidates.values()]))))

    if len(set([str(v) for v in solver.candidates.values()])) == 0:
        return

    solver.update()

    incomplete = incomplete_product.IncompleteProduct(p.automata, snb_messages)

    add_determinism_constraints(solver, automata)

    if logger.isEnabledFor(logging.DEBUG):
        if len(main_product.deadlock_states()) > 0:
            logger.debug("Adding initial deadlock constraints, # deadloocks {}".
                         format(len(main_product.deadlock_states())))
            logger.debug('Number of constraints {0}'.format(solver.num_constraints))
        else:
            logger.debug("No deadlocks.")

    for d in main_product.deadlock_states():
        logger.debug("Deadlock {}".format(d))
        logger.debug(edges_that_solve_deadlock(main_product, d))
        solver.add_constraint(enable=edges_that_solve_deadlock(main_product, d))

    if snb:
        if logger.isEnabledFor(logging.DEBUG):
            if len(main_product.strong_blocking_states(snb_messages)) > 0:
                logger.debug("Adding constraints for strong non-blockingness")
                assert len(incomplete.main_product.strong_blocking_states(snb_messages)) > 0
            else:
                logger.debug("Found no strong non-blocking violating states")
        edgess = set()
        for b in incomplete.main_product.strong_blocking_states(snb_messages):
            for edges in incomplete.edge_sets_to_solve_snb_violation(b):
                logger.debug("violating state {}".format(b))
                solver.add_constraint(enable=edges)

    # Add input enabledness constraints
    if not is_input_enabled:
        for clause in incomplete.input_enabled_constraints():
            if len(clause) > 0:
                solver.add_constraint(enable=clause)

    if (len(main_product.deadlock_states()) == 0 and
        (not snb or
         len(main_product.strong_blocking_states(snb_messages)) == 0) and
        is_input_enabled):
        for liveness_product in liveness_products:
            liveness_product = product.Product(liveness_product.automata)
            for cycle in liveness_product.strong_fair_cycles():
                if is_live:
                    logger.debug("liveness violation")
                is_live = False
                if len(cycle) == 1 or cycle[-1] != cycle[0]:
                    cycle += [cycle[0]]
                solver.add_constraint(
                    disable=[],
                    enable=liveness_product.candidates_to_make_cycle_unfair(cycle))

    logger.debug("Number of states: {0}".format(len(p.states())))
    num_iterations = 0
    num_solutions = 0
    bad_state_predicates = p.bad_state_predicates
    if not bad_state_predicates:
        violates_bad_predicates = False
    equivalent_names = p.equivalent_names
    num_candidates = len(
        set([str(v)
             for v in solver.candidates.values()]))

    while True:
        num_iterations += 1
        logger.info("starting loop, num iterations %d", num_iterations)
        new_transitions = solver.solve()
        if not new_transitions:
            logger.info("solver returned unsat")
            yield ('No solutions could be found.'
                   if num_solutions == 0
                   else 'Search finished.',
                   {'iterations': num_iterations,
                    'candidate transitions': num_candidates})
            return
        logger.info("adding transitions")
        logger.info("%s", new_transitions)
        main_product.add_automata_edges_by_name(new_transitions)

        incomplete = incomplete_product.IncompleteProduct(p.automata, snb_messages)

        safety_products = [product.Product(safety_product.automata) for safety_product in safety_products]
        for sp in safety_products:
            sp.equivalent_names = equivalent_names

        logger.debug("Computing deadlocks, local deadlocks, safety.")

        deadlocks = main_product.deadlock_states()
        is_safe = all(safety_product.is_safe() for safety_product in safety_products)
        logger.debug("# of states: %d", len(main_product.states()))
        logger.debug("# of solutions: {0}".format(num_solutions))
        logger.debug("# of deadlocks: %d", len(deadlocks))
        blocking_states = []
        if snb:
            blocking_states = main_product.strong_blocking_states(snb_messages)
            logger.debug("# of strong blocking states: %d",
                         len(blocking_states))

        removed_transitions = []
        if bad_state_predicates:
            logger.debug("Checking bad predicates.")
            bad_state_predicate_product = next((sp for sp in safety_products if any(a for a in sp.automata if hasattr(a, 'is_bad_predicate_monitor'))), main_product)

            violates_bad_predicates = any(predicate(s) for predicate in bad_state_predicates for s in bad_state_predicate_product.states())
            if violates_bad_predicates:
                logger.debug("Violates bad predicate!")
                for predicate in bad_state_predicates:
                    if any(predicate(s) for s in bad_state_predicate_product.states()):
                        bad_transitions = generalize_reachability(bad_state_predicate_product, new_transitions, predicate)
                        logger.debug("Removing: %s", bad_transitions)
                        solver.add_constraint(disable=bad_transitions)
                        for t in bad_transitions:
                            removed_transitions.append(t)

        if deadlocks != []:
            logger.debug("adding deadlock constraints")
        if not is_safe:
            logger.debug("Not safe, adding constraints")
            for safety_product in safety_products:
                if safety_product.is_safe():
                    continue
                transitions = generalize_reachability(safety_product,
                                                      new_transitions,
                                                      safety_product.is_safety_violating)
                logger.debug(transitions)
                solver.add_constraint(disable=transitions)
        for d in deadlocks:
            disable_transitions = generalize_reachability(main_product, new_transitions, lambda s: s == d)
            if all(t not in removed_transitions for t in disable_transitions):
                solver.add_constraint(enable=edges_that_solve_deadlock(main_product, d),
                                      disable=disable_transitions)

        if snb and len(blocking_states) > 0:
            logger.debug("adding blocking state constraints")
        for b in blocking_states:
            disable_transitions = generalize_reachability(main_product,
                                                          new_transitions,
                                                          lambda s: s == b)
            if all(t not in removed_transitions for t in disable_transitions):
                for edges in incomplete.edge_sets_to_solve_snb_violation(b):
                    solver.add_constraint(enable=edges, disable=disable_transitions)

        if deadlocks == [] and len(blocking_states) == 0 and is_safe and not violates_bad_predicates:
            is_live = True
            logger.debug("checking liveness")
            for liveness_product in liveness_products:
                liveness_product = product.Product(liveness_product.automata)
                cycles = liveness_product.strong_fair_cycles()
                for cycle in cycles:
                    if is_live:
                        logger.debug("liveness violation")
                    is_live = False
                    edges_to_reach_cycle = generalize_reachability(liveness_product, new_transitions, lambda state: state in cycle)
                    if len(cycle) == 1 or cycle[-1] != cycle[0]:
                        cycle += [cycle[0]]
                    edges_to_repeat_cycle = added_transitions_in_path(liveness_product, new_transitions, cycle)
                    edges_to_make_cycle_unfair = liveness_product.candidates_to_make_cycle_unfair(cycle)
                    edges_to_exclude = edges_to_reach_cycle + edges_to_repeat_cycle
                    logger.debug("edges to exclude: " + str(edges_to_exclude))
                    logger.debug("edges to enable: " + str(edges_to_make_cycle_unfair))
                    solver.add_constraint(disable=edges_to_exclude,
                                          enable=edges_to_make_cycle_unfair)
            if is_live:
                logger.info("Number of iterations: %d", num_iterations)
                num_solutions += 1
                yield (new_transitions,
                       {'iterations': num_iterations,
                        'candidate transitions': num_candidates})
                logger.info("continuing after solution")
                solver.add_constraint(disable=new_transitions)
        logger.debug("Removing transitions.")
        main_product.remove_automata_edges_by_name(new_transitions)


def added_transitions_in_path(product_automaton, added_edges, path):
    added_transitions = []
    for state1, state2 in zip(path, path[1:]):
        write_transition, read_transition = product_automaton.get_automata_edges_without_label(state1, state2)
        for transition in [read_transition, write_transition]:
            transition = (transition[0].name, transition[1][0], transition[1][1], transition[1][2])
            if transition in added_edges:
                added_transitions.append(transition)
    return added_transitions


def edges_that_solve_deadlock(p, deadlock):
    automata_states = deadlock.split(',')
    edges = []
    for i, a in enumerate(p.automata):
        if not a.is_environment:
            for start, label, end in a.candidate_edges_from_state_iter(automata_states[i]):
                message = label[:-1]
                if label.endswith('?'):
                    if any(a2.state_neighbors.get(automata_states[i2], {}).get(message + "!", []) != []
                           for i2, a2 in enumerate(p.automata) if a2.is_environment and message in a2.output_alphabet):
                        edges.append((a.name, start, label, end))
                elif label.endswith('!'):
                    if any(a2.state_neighbors.get(automata_states[i2], {}).get(message + "?", []) != []
                           for i2, a2 in enumerate(p.automata) if a2.is_environment and message in a2.input_alphabet):
                        edges.append((a.name, start, label, end))
    return edges


def edges_that_solve_local_deadlock(p, local_deadlock, a):
    automata = p.is_state_local_deadlock(local_deadlock, return_automata=True)
    # each automaton in automata here is blocked on an input transition
    # the environment automaton that would write that message is blocked
    # on writing a message that this automaton should read
    assert a in automata
    edges = []
    for start, label, end in a.candidate_edges_from_state_iter(p.automaton_state(a, local_deadlock)):
        if any(a2.state_neighbors.get(p.automaton_state(a2, local_deadlock), {}).get(label[:-1] + "!", []) != []
               for a2 in p.automata if a2.is_environment and label[:-1] in a2.output_alphabet):
            edges.append((a.name, start, label, end))
    return edges


def generalize_reachability(product_automaton, added_edges, bad_state_predicate):
    # Do a BFS to the error set
    state, predecessors = product_automaton.bfs_to_state(bad_state_predicate)
    assert state
    take_automaton_name = isinstance(added_edges[0][0], str)
    added_transitions = []
    while state != product_automaton.initial_state:
        previous_state, label = predecessors[state]
        write_transition, read_transition = product_automaton.get_automata_edges(previous_state, label, state)
        for transition in [read_transition, write_transition]:
            transition = (transition[0].name if take_automaton_name else transition[0],
                          transition[1][0], transition[1][1], transition[1][2])
            if transition in added_edges:
                added_transitions.append(transition)
        state = previous_state
    return added_transitions


def generalize_safety_violations(product_automaton, new_transitions, bad_state_predicate):
    safety_violating_states = [state for state in product_automaton.nodes_iter() if bad_state_predicate(state)]
    paths = networkx.single_source_dijkstra_path(product_automaton, product_automaton.initial_state)
    assert len([target for target in paths if target in safety_violating_states])
    min_length = float('inf')
    min_length_paths = set()
    for error_state in safety_violating_states:
        path_transitions = product_automaton.automata_new_transitions_in_path(new_transitions, paths[error_state])
        if len(path_transitions) < min_length:
            set_transitions = set(path_transitions)
            min_length = len(path_transitions)
            min_length_paths = [set_transitions]
        elif len(path_transitions) == min_length:
            set_transitions = set(path_transitions)
            if all(s != set_transitions for s in min_length_paths):
                min_length_paths.append(set_transitions)
    return min_length_paths


def new_generalize_safety_violations(product_automaton, new_transitions, solver, bad_state_predicate):
    safety_violating_states = [state for state in product_automaton.nodes_iter() if bad_state_predicate(state)]
    paths = networkx.single_source_dijkstra_path(product_automaton, product_automaton.initial_state)
    assert len([target for target in paths if target in safety_violating_states])
    min_length = float('inf')
    min_length_paths = set()
    for error_state in safety_violating_states:
        path_transitions = product_automaton.automata_new_transitions_in_path(new_transitions, paths[error_state])
        if len(path_transitions) < min_length:
            path_transitions_that_do_not_move = list(path_transitions)
            path = paths[error_state]
            for path_transition in path_transitions:
                path_transition_moves = False
                automaton_name, start, label, end = path_transition
                a_index, a = product_automaton.automaton_index_by_name(automaton_name)
                if a in product_automaton.equivalent_automata:
                    b = product_automaton.equivalent_automata[1] if a == product_automaton.equivalent_automata[0] else product_automaton.equivalent_automata[0]
                    b_index, _ = product_automaton.automaton_index_by_name(b.name)
                    start2 = util.switch_strings(start, product_automaton.equivalent_names[0], product_automaton.equivalent_names[1])
                    label2 = util.switch_strings(label, product_automaton.equivalent_names[0], product_automaton.equivalent_names[1])
                    end2 = util.switch_strings(end, product_automaton.equivalent_names[0], product_automaton.equivalent_names[1])
                else:
                    b, start2, label2, end2 = a, start, label, end
                    b_index = a_index

                for state1, state2 in zip(path, path[1:]):
                    for d in product_automaton.edge[state1][state2].values():
                        message = d['label']
                        if message in a.input_alphabet or message in a.output_alphabet or message in b.input_alphabet or message in b.output_alphabet:
                            if state1.split(',')[a_index] == end or state1.split(',')[b_index] == end2:
                                # print "path transition {0} moves: {1} -> {2}".format(path_transition, state1, state2)
                                path_transitions_that_do_not_move.remove(path_transition)
                                path_transition_moves = True
                                break
                    if path_transition_moves:
                        break
            # print 'path transitions that do not move'
            # print path_transitions_that_do_not_move
            new_path_transitions = []
            for path_transition in path_transitions:
                if path_transition in path_transitions_that_do_not_move:
                    automaton_name, start, label, end = path_transition
                    new_path_transitions.append((automaton_name, start, label, '*'))
                else:
                    new_path_transitions.append(path_transition)
            set_transitions = set(new_path_transitions)
            min_length = len(path_transitions)
            min_length_paths = [set_transitions]
        elif len(path_transitions) == min_length:

            path_transitions_that_do_not_move = list(path_transitions)
            path = paths[error_state]
            for path_transition in path_transitions:
                path_transition_moves = False
                automaton_name, start, label, end = path_transition
                a_index, a = product_automaton.automaton_index_by_name(automaton_name)
                if a in product_automaton.equivalent_automata:
                    b = product_automaton.equivalent_automata[1] if a == product_automaton.equivalent_automata[0] else product_automaton.equivalent_automata[0]
                    b_index, _ = product_automaton.automaton_index_by_name(b.name)
                    start2 = util.switch_strings(start, product_automaton.equivalent_names[0], product_automaton.equivalent_names[1])
                    label2 = util.switch_strings(label, product_automaton.equivalent_names[0], product_automaton.equivalent_names[1])
                    end2 = util.switch_strings(end, product_automaton.equivalent_names[0], product_automaton.equivalent_names[1])
                else:
                    b, start2, label2, end2 = a, start, label, end
                    b_index = a_index

                for state1, state2 in zip(path, path[1:]):
                    for d in product_automaton.edge[state1][state2].values():
                        message = d['label']
                        if message in a.input_alphabet or message in a.output_alphabet or message in b.input_alphabet or message in b.output_alphabet:
                            if state1.split(',')[a_index] == end or state1.split(',')[b_index] == end2:
                                # print "path transition {0} moves: {1} -> {2}".format(path_transition, state1, state2)
                                path_transitions_that_do_not_move.remove(path_transition)
                                path_transition_moves = True
                                break
                    if path_transition_moves:
                        break
            # print 'path transitions that do not move'
            # print path_transitions_that_do_not_move
            new_path_transitions = []
            for path_transition in path_transitions:
                if path_transition in path_transitions_that_do_not_move:
                    automaton_name, start, label, end = path_transition
                    new_path_transitions.append((automaton_name, start, label, '*'))
                else:
                    new_path_transitions.append(path_transition)
            set_transitions = set(new_path_transitions)

            if all(s != set_transitions for s in min_length_paths):
                min_length_paths.append(set_transitions)

    sets_of_transitions = min_length_paths
    new_sets_of_transitions = []
    for transitions in sets_of_transitions:
        new_unsafe_transitions = []
        for transition in transitions:
            if transition[3] == '*':
                temp = []
                for edge in solver.candidates:
                    if edge[0] == transition[0] and edge[1] == transition[1] and edge[2] == transition[2]:
                        temp.append(edge)
                new_unsafe_transitions.append(temp)
            else:
                new_unsafe_transitions.append([transition])
        for t in itertools.product(*new_unsafe_transitions):
            new_sets_of_transitions.append(t)
    return new_sets_of_transitions
