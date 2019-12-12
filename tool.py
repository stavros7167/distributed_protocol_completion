#!/usr/bin/env python

import argparse
import logging
import sys

import cegis
import parser
import product

def default_input_file_parsing(args):
    print("Parsing file {}".format(args.input_filename[0]))

    automata, strong_non_blocking_messages = parser.parse(args.input_filename[0])

    system = product.Product(automata)
    return automata, system, strong_non_blocking_messages


def modelcheck(args):
    automata, _, strong_non_blocking_messages = default_input_file_parsing(args)

    deadlock_product_automata = [a for a in automata if not a.is_monitor]
    safety_monitors = [a for a in automata if a.is_safety]
    for safety_monitor in safety_monitors:
        found_error = False
        for state in safety_monitor.states():
            if state == 'error':
                found_error = True
            if safety_monitor.is_accepting(state) and state != 'error':
                print("Monitor %s has an accepting state %s that is not called \'error\'."
                      % (safety_monitor, state))
                print("Please call all accepting states \'error\' without quotes.")
                sys.exit(1)
            if not safety_monitor.is_accepting(state) and state == 'error':
                print("Monitor %s has a state called \'error\' that is not marked accepting."
                      % (safety_monitor))
                print("Please mark error states as accepting.")
                sys.exit(1)

    safety_product_automata = [deadlock_product_automata + [a]
                               for a in safety_monitors]
    liveness_monitors = [a for a in automata if a.is_liveness]
    liveness_product_automata = [deadlock_product_automata + [a]
                                 for a in liveness_monitors]
    main_product = product.Product(deadlock_product_automata)
    safety_products = [product.Product(aa)
                       for aa in safety_product_automata]
    liveness_products = [product.Product(aa)
                         for aa in liveness_product_automata]

    print("# of deadlocks: %d" % len(main_product.deadlock_states()))
    if args.c:
        for deadlock_state in main_product.deadlock_states():
            print("\nTrace to %s (note no monitor automata are included)"
                  % deadlock_state)
            main_product.print_automata_names()
            main_product.print_trace_to_state(deadlock_state)

    if args.snb:
        states = main_product.strong_blocking_states(strong_non_blocking_messages)
        if len(states) == 0:
            print("There are no strong non-blockingness violations.")
        else:
            print("There are strong non-blockingness violations.")
            if args.c:
                for state in states:
                    print("\nTrace to %s (note no monitor automata are included)" % state)
                    main_product.print_automata_names()
                    main_product.print_trace_to_state(state)
                    main_product.print_strong_blockingness_reason(
                        state, strong_non_blocking_messages)

    found_safety_violations = False
    for safety_product in safety_products:
        safety_monitor = next(a for a in safety_product.automata if a.is_monitor)
        if safety_product.is_safe():
            continue
        print("There are safety violations")
        found_safety_violations = True
        if args.c:
            for state in safety_product.nodes_iter():
                if safety_product.is_safety_violating(state):
                    print("\nTrace to %s (the only monitor included is %s)"
                          % (state, safety_monitor))
                    safety_product.print_trace_to_state(state)
                    safety_product.print_automata_names()
    if not found_safety_violations:
        print("There are no safety violations.")
    printed_liveness_violations_message = False
    for liveness_product in liveness_products:
        liveness_monitor = next(a for a in liveness_product.automata if a.is_monitor)
        cycles = liveness_product.strong_fair_cycles()
        if len(cycles) == 0:
            continue
        if not printed_liveness_violations_message:
            print("There are liveness violations")
            printed_liveness_violations_message = True
        if args.c:
            for cycle in cycles:
                print("\nCycle: (the only monitor included is %s)\n"
                      % liveness_monitor)
                print("Trace to reach cycle")
                liveness_product.print_automata_names()
                liveness_product.print_trace_to_state(cycle[0])
                if len(cycle) == 1 or cycle[-1] != cycle[0]:
                    cycle += [cycle[0]]
                print("Trace to repeat cycle")
                liveness_product.print_path(cycle)
    if not printed_liveness_violations_message:
        print("There are no liveness violations")

def synthesize(args):
    automata, system, strong_non_blocking_messages = default_input_file_parsing(args)
    if args.solver is None:
        solver_type = "z3minimum"
    else:
        solvers = ["z3", "gurobi", "z3rel", "z3manualminimal", "z3minimum",
                   "z3opt", "crypto"]
        if args.solver not in solvers:
            print "Invalid solver type."
            print("Choose one in %s" % ', '.join(solvers))
            sys.exit(1)
        solver_type = args.solver
    if args.debug:
        logging.getLogger("cegis").setLevel(logging.DEBUG)
        logging.getLogger("cegis_solver").setLevel(logging.DEBUG)
        logging.getLogger("incomplete_product").setLevel(logging.DEBUG)

    result = cegis.synthesize(system, solver_type, sys.stdout, args.seed,
                              args.dead, snb=args.snb,
                              snb_messages=strong_non_blocking_messages,
                              all=args.all)
    if args.pa:
        print("When one solution is requested, and one is found, this prints"
              " the automata. Otherwise ignore this.")

        for a in automata:
            if a.is_environment or a.is_monitor:
                continue
            print('process %s {' % a.name)
            print('  inputs [%s]' % ', '.join(a.input_alphabet))
            print('  outputs [%s]' % ', '.join(a.output_alphabet))
            print('  initial %s' % a.initial_state)
            for state in sorted(a.states()):
                for label, other_states in a.state_neighbors[state].items():
                    for other_state in other_states:
                        sys.stdout.write('  %s %s %s' % (state, label, other_state))
                        if (state, label, other_state) in a.strong_fairness_transitions:
                            sys.stdout.write(' strong_fairness')
                        sys.stdout.write('\n')
            print('}')
    for a in automata:
        a.draw_to_file('temp.html', append=True)

def printcandidates(args):
    automata, _, _ = default_input_file_parsing(args)
    for a in automata:
        print a.name
        print a.candidate_edges()

def print_dead_transitions(args):
    automata, system, _ = default_input_file_parsing(args)
    for automaton, transitions in system.dead_automata_transitions().items():
        print('Dead transitions for automaton: {}'.format(automaton))
        for transition in transitions:
            print(transition)

def main():
    main_arg_parser = argparse.ArgumentParser(prog='tool.py')
    subparsers = main_arg_parser.add_subparsers()


    modelcheck_parser = subparsers.add_parser(
        'modelcheck',
        help="Model check protocol given in input file.")
    modelcheck_parser.add_argument(
        'input_filename', nargs=1,
        help="File with automata spec.")
    modelcheck_parser.add_argument("-c",
                                   action='store_true',
                                   help="When added it prints counter example traces.")
    modelcheck_parser.add_argument("-snb",
                                   action='store_true',
                                   help="When added it additionally checks strong non-blockingness.")

    modelcheck_parser.set_defaults(func=modelcheck)

    synthesize_parser = subparsers.add_parser(
        'synthesize',
        help="Synthesize incomplete protocol given in input file.")
    synthesize_parser.add_argument(
        'input_filename', nargs=1,
        help="File with automata spec.")
    synthesize_parser.add_argument("-snb",
                                   action='store_true',
                                   help="Add as a requirement that the result is strongly non-blocking.")
    synthesize_parser.add_argument("-all",
                                   action='store_true',
                                   help="Add to produce all solutions.")

    synthesize_parser.add_argument("-pa",
                                   action='store_true',
                                   help=('Add to print complete process automata'
                                         'in the end, when asking for one solution.'))
    synthesize_parser.add_argument('-debug',
                                   action='store_true',
                                   help=('Add to enable debug logging.'))
    synthesize_parser.add_argument('-seed', type=int, default=0,
                                   help=('Random seed used by the z3 solver. '
                                         'Default is 0.'))
    synthesize_parser.add_argument('-dead', action='store_true',
                                   help=('Check if transitions are taken in '
                                         'product or are "dead code".'))

    help_solver_type = ("Default solver is z3minimum. Other options are "
                        "gurobi, z3, z3rel, z3manmin, z3opt, crypto")
    synthesize_parser.add_argument("-s", "--solver", help=help_solver_type)
    synthesize_parser.set_defaults(func=synthesize)

    printcandidates_parser = subparsers.add_parser(
        'printcandidates',
        help="Print candidates of incompletet protocol given in input file.")
    printcandidates_parser.add_argument(
        'input_filename', nargs=1,
        help="File with automata spec.")
    printcandidates_parser.set_defaults(func=printcandidates)

    print_dead_transitions_parser = subparsers.add_parser(
        'printdeadtransitions',
        help="Print dead transitions of automata when in product given in input file.")
    print_dead_transitions_parser.add_argument(
        'input_filename', nargs=1,
        help="File with automata spec.")
    print_dead_transitions_parser.set_defaults(func=print_dead_transitions)

    args = main_arg_parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
