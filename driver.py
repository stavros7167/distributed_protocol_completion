#!/usr/bin/env python

import argparse
import logging
import os
import os.path
import sys
if 'Z3_PATH' in os.environ:
    sys.path.insert(0, os.environ['Z3_PATH'])

import examples.abp
import examples.abp_colors
import examples.consensus
import examples.consensus_no_test_and_set
import examples.vi
import examples.vi_data
import cegis
import cegis_solver
import util


BENCHMARK_SPECS = {
    'ABP1': {
        'system': examples.abp.system_with_one_scenario
    },
    'ABP1_without_send_follows_deliver': {
        'system': examples.abp.system_with_one_scenario_no_send_follows_deliver
    },
    'ABP1_with_infinite_sends': {
        'system': examples.abp.system_with_one_scenario_infinite_sends
    },
    'ABP2': {
        'system': examples.abp.system_with_one_scenario2,
    },
    "ABP4": {
        'system': examples.abp.system_with_four_scenarios
    },
    "ABPEmpty": {
        'system': examples.abp.system_empty
    },
    "ABPColors1": {
        'system': examples.abp_colors.system_with_one_scenario
    },
    "ABPColors2": {
        'system': examples.abp_colors.system_with_one_scenario2
    },
    "ABPColors4": {
        'system': examples.abp_colors.system_with_four_scenarios
    },
    "VI": {
        'system': examples.vi.vi
    },
    "VIData": {
        'system': examples.vi_data.vi
    },
    "consensus_fail": {
        'system': examples.consensus.consensus_from_fail_scenario
    },
    "consensus_success_no_extra": {
        'system': examples.consensus.consensus_from_success_scenario
    },
    "consensus_success_one_extra_state": {
        'system': examples.consensus.consensus_from_success_scenario_with_one_extra_state
    },
    "consensus_no_test_and_set": {
        'system': examples.consensus_no_test_and_set.consensus_prefer0read0prefer1read1
    }
}

def test(benchmark,
         solver_type,
         draw_file,
         all_solutions,
         solutions_file):
    """ benchmark is the name of the benchmark to run: it can be ABP1, ABP2, ABP4,
        ABP1_without_send_follows_deliver, or ABP1_with_infinite_sends.
        seed is the seed to be passed to the search method for ordering candidates,
        method is either explicit, heuristic, or deadlock,
        draw_file is either None or a path to a file on which all automata are printed.
    """
    assert benchmark in BENCHMARK_SPECS
    system = BENCHMARK_SPECS[benchmark]['system']()
    result = cegis.synthesize(system, solver_type, solutions_file, all=all_solutions)
    if result:
        # The search method has added the results on the system already
        for a in system.automata:
            if not a.is_environment:
                try:
                    __import__("pygraphviz")
                except ImportError:
                    print("Cannot import pygraphviz, will not draw resulting"
                          " automata")
                    return
                if draw_file is not None:
                    a.draw_to_file(draw_file, append=True)


if __name__ == '__main__':
    help_benchmark = "Choose {}".format(', '.join(BENCHMARK_SPECS.keys()))
    help_solver_type = "gurobi, z3, z3rel, z3manmin, z3minimum, z3opt"

    description = """\
Several solvers are supported to solve the constraints:
* 'gurobi' for Gurobi's ILP solver to minimize the number of added edges in
each iteration,
* 'z3' for Z3 SMT solver, with no effort to minimize the number of edges,
* 'z3rel' for Z3 but with flag for relevance propagation that seems to
approximate minimal models (not minimum),
* 'z3manmin' for Z3 and manual model trimming so that the added edges form a
minimal model,
* 'z3minimum' for Z3 and explicit minimum number of added edges in each
iteration.
* 'z3opt' for minimum models using new version of optimizing Z3, nuZ. This
requires the environment variable Z3_PATH to point to new z3 python module
path.

"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description)
    parser.add_argument("-b", "--benchmark", required=True, help=help_benchmark)
    parser.add_argument("-v", "--verbose", type=int)
    parser.add_argument("-s", "--solver", help=help_solver_type)
    parser.add_argument("-r", "--results",
                        help='File to write results to.')
    parser.add_argument("-i", "--inputs", action="store_true",
                        help="Print input automata at output file")
    parser.add_argument("-c", "--clear", action="store_true",
                        help="Clear output file.")

    default_output_file = 'figures/temp.html'
    parser.add_argument("-o", "--output",
                        help="File to output result figures.")
    parser.add_argument("-a", "--all", action='store_true', help="find all solutions")

    args = parser.parse_args()

    if args.benchmark not in BENCHMARK_SPECS:
        print help_benchmark
        sys.exit(1)

    if args.solver is None:
        solver_type = "gurobi"
    else:
        if (args.solver not in
            ["z3", "gurobi", "z3rel", "z3manualminimal", "z3minimum", "z3opt"]):
            print help_solver_type
            sys.exit(1)
        else:
            solver_type = args.solver

    benchmark = args.benchmark

    if args.verbose == 1:
        logging.getLogger("cegis").setLevel(logging.INFO)
        logging.getLogger("cegis_solver").setLevel(logging.INFO)
    elif args.verbose == 2:
        logging.getLogger("cegis").setLevel(logging.DEBUG)
        logging.getLogger("cegis_solver").setLevel(logging.DEBUG)

    if args.results is not None:
        solutions_file = open(args.results, 'w')
    else:
        solutions_file = sys.stdout

    if args.output:
        draw_file = os.path.join(util.SCENARIOS_PATH, args.output)
    else:
        draw_file = None
    if draw_file is not None and args.clear:
        open(draw_file, 'w').close()
    if draw_file is None and args.clear:
        print "You specified to clear the output file,"
        print "But you didn't specify an output file"

    if draw_file is not None:
        for automaton in BENCHMARK_SPECS[benchmark]['system']().automata:
            automaton.draw_to_file(draw_file, append=True)

    test(benchmark,
         solver_type=solver_type,
         draw_file=draw_file,
         all_solutions=args.all,
         solutions_file=solutions_file)

    if solutions_file is not None:
        solutions_file.close()
