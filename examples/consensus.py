"""
Problem:
There are two processes; each initially chooses a preference value unknown to the other process.
The processes need to coordinate and arrive at a common decision value.

The consensus protocol consists of two processes that are symmetrical.
Each process performs the following steps:
1. chooses, non-deterministally, a preference value, 0 or 1,
2. writes its preference in a shared register,
3. test-and-sets a commmon register
4. if test-and-set is successful then the process decides on its own value
5. if test-and-set is unsuccessful, the process decides on the value of the other
shared register of the other process.

The following automata are used to implement the protocol above:
one automaton per process that models the preference value non-deterministic choice,
one automaton per process that models the shared register on which the preference value is written,
one automaton that models the test-and-set register.


Properties that need to be satsfied:
1. agreement: the decisions by the two automata have to match,
2. validity: the decisions have to equal one of the preference values,
3. wait-freedom: at any point, if only one process makes progress, it will reach a decision.

How can we check the three properties:
1. agreement, using a safety monitor that listens to the decision messages,
2. validity, using a safety monitor that listens to preference and decision messages,
3. wait-freedom, using the following two mechanisms:
a) a liveness monitor for each process, that finds cycles that do not contain
a decision message, without any fairness constraints,
b) check that for every state, for every process automaton, at least one outgoing transition
is enabled.

Notes:
A test-and-set instruction writes to a memory location and returns its old value.
More information on the protocol can be found here:
wikipedia article on Consensus, http://en.wikipedia.org/wiki/Consensus_(computer_science),
paper "Wait-free synchronization" by Maurice Herlihy http://dl.acm.org/citation.cfm?id=102808, and
Rajeev Alur's lecture notes from CIS 540, http://www.seas.upenn.edu/~cis540/Spring14/feb26.pptx .
"""
import re

import automaton
import product
import util


def test_and_set(process1='p1', process2='p2'):
    """
    In its initial state 'ts_unset', the content of the memory location is 0.
    If any of the two processes attempts to test and set at that location,
    the automaton responds with 0, and transitions to state 'ts_set'.
    At that state, if any of the processes attempts to test and set,
    the automaton responds with 1 and goes back to state q3.
    """
    return automaton.Automaton(name='test_and_set',
                               edges=[('ts_unset', '%s_test_and_set_0!' % process1, 'ts_set'),
                                      ('ts_unset', '%s_test_and_set_0!' % process2, 'ts_set'),
                                      ('ts_set', '%s_test_and_set_1!' % process1, 'ts_set'),
                                      ('ts_set', '%s_test_and_set_1!' % process2, 'ts_set')])


def preference(process):
    return automaton.Automaton(name="preference_%s" % process,
                               edges=[('pref_before_choosing_%s' % process, '%s_prefer_1!' % process, 'pref_after_choosing_1_%s' % process),
                                      ('pref_before_choosing_%s' % process, '%s_prefer_0!' % process, 'pref_after_choosing_0_%s' % process)])


SCENARIO_PATTERN1 = "initialL {process}_prefer_{value}? {process}_set_{value}! {process}_test_and_set_0? decide_{process}_{value}! finalL"


SCENARIO_PATTERN2 = "initialL {process}_prefer_{value}? {process}_set_{value}! {process}_test_and_set_1? {other_process}_read_{other_value}? decide_{process}_{other_value}! finalL"


SCENARIOS = {'p1': [SCENARIO_PATTERN1.format(process='p1', value='0'),
                    SCENARIO_PATTERN1.format(process='p1', value='1'),
                    SCENARIO_PATTERN2.format(process='p1', value='0', other_process='p2', other_value='0'),
                    SCENARIO_PATTERN2.format(process='p1', value='1', other_process='p2', other_value='0'),
                    SCENARIO_PATTERN2.format(process='p1', value='0', other_process='p2', other_value='1'),
                    SCENARIO_PATTERN2.format(process='p1', value='1', other_process='p2', other_value='1')],
             'p2': [SCENARIO_PATTERN1.format(process='p2', value='0'),
                    SCENARIO_PATTERN1.format(process='p2', value='1'),
                    SCENARIO_PATTERN2.format(process='p2', value='0', other_process='p1', other_value='0'),
                    SCENARIO_PATTERN2.format(process='p2', value='1', other_process='p1', other_value='0'),
                    SCENARIO_PATTERN2.format(process='p2', value='0', other_process='p1', other_value='1'),
                    SCENARIO_PATTERN2.format(process='p2', value='1', other_process='p1', other_value='1')]}


def process_no_scenarios(process):
    other_process = util.switch_strings(process, "1", "2")
    input_message_formats = ["{process}_prefer_0", "{process}_prefer_1", "{process}_test_and_set_0", "{process}_test_and_set_1",
                             "{other_process}_read_0", "{other_process}_read_1"]
    output_message_formats = ["{process}_set_0", "{process}_set_1",
                              "decide_{process}_0", "decide_{process}_1"]
    input_alphabet = [input_message_format.format(process=process, other_process=other_process)
                      for input_message_format in input_message_formats]
    output_alphabet = [output_message_format.format(process=process, other_process=other_process)
                       for output_message_format in output_message_formats]
    p = automaton.Automaton(name=process,
                            is_environment=False,
                            input_alphabet=input_alphabet,
                            output_alphabet=output_alphabet)
    return p


def process_correct(process, other_process=None):
    if not other_process:
        other_process = util.switch_strings(process, "1", "2")
    return automaton.Automaton(name=process,
                               edges=[('%s_initial' % process, '%s_prefer_0?' % process, '%s_prefer_0' % process),
                                      ('%s_initial' % process, '%s_prefer_1?' % process, '%s_prefer_1' % process),
                                      ('%s_prefer_0' % process, '%s_set_0!' % process, '%s_after_writing_shared_0' % process),
                                      ('%s_prefer_1' % process, '%s_set_1!' % process, '%s_after_writing_shared_1' % process),
                                      ('%s_after_writing_shared_0' % process, '%s_test_and_set!' % process, '%s_after_test_and_setting_0' % process),
                                      ('%s_after_writing_shared_1' % process, '%s_test_and_set!' % process, '%s_after_test_and_setting_1' % process),
                                      ('%s_after_test_and_setting_0' % process, '%s_respond_0?' % process, '%s_before_deciding_0' % process),
                                      ('%s_after_test_and_setting_1' % process, '%s_respond_0?' % process, '%s_before_deciding_1' % process),
                                      ('%s_after_test_and_setting_0' % process, '%s_respond_1?' % process, '%s_before_deciding_on_others' % process),
                                      ('%s_after_test_and_setting_1' % process, '%s_respond_1?' % process, '%s_before_deciding_on_others' % process),
                                      ('%s_before_deciding_on_others' % process, '%s_read!' % other_process, '%s_after_asking_on_others' % process),
                                      ('%s_after_asking_on_others' % process, '%s_return_0?' % other_process, '%s_before_deciding_0' % process),
                                      ('%s_after_asking_on_others' % process, '%s_return_1?' % other_process, '%s_before_deciding_1' % process),
                                      ('%s_before_deciding_0' % process, 'decide_%s_0!' % process, '%s_final' % process),
                                      ('%s_before_deciding_1' % process, 'decide_%s_1!' % process, '%s_final' % process)])


def process(process):
    p = process_no_scenarios(process)
    for scenario in SCENARIOS[process][:2]:
        p.add_string(scenario)
    return p


def process_from_fail_scenario(process='p1'):
    p = process_no_scenarios(process)
    for scenario in SCENARIOS[process][2:]:
        p.add_string(scenario)
    return p


def process_from_success_scenario(process='p1'):
    p = process_no_scenarios(process)
    for scenario in SCENARIOS[process][:2]:
        p.add_string(scenario)
    return p


def process_from_success_and_fail_scenarios(process):
    p = process_no_scenarios(process)
    for scenario in SCENARIOS[process]:
        p.add_string(scenario)
    return p


def shared_register(process='p1'):
    return automaton.Automaton(name="shared_register_%s" % process,
                               edges=[('reg_set0_%s' % process, '%s_set_0?' % process, 'reg_set0_%s' % process),
                                      ('reg_set0_%s' % process, '%s_set_1?' % process, 'reg_set1_%s' % process),
                                      ('reg_set0_%s' % process, '%s_read_0!' % process, 'reg_set0_%s' % process),
                                      ('reg_set1_%s' % process, '%s_read_1!' % process, 'reg_set1_%s' % process)])


def decisions_listener(process1, process2):
    return automaton.Automaton(name='decisions_listener',
                               edges=[('both_undecided', 'decide_%s_0?' % process1, '%s_0_%s_undecided' % (process1, process2)),
                                      ('both_undecided', 'decide_%s_1?' % process1, '%s_1_%s_undecided' % (process1, process2)),
                                      ('both_undecided', 'decide_%s_0?' % process2, '%s_undecided_%s_0' % (process1, process2)),
                                      ('both_undecided', 'decide_%s_1?' % process2, '%s_undecided_%s_1' % (process1, process2)),
                                      ('%s_0_%s_undecided' % (process1, process2), 'decide_%s_0?' % process2, '%s_0_%s_0' % (process1, process2)),
                                      ('%s_0_%s_undecided' % (process1, process2), 'decide_%s_1?' % process2, '%s_0_%s_1' % (process1, process2)),
                                      ('%s_1_%s_undecided' % (process1, process2), 'decide_%s_0?' % process2, '%s_1_%s_0' % (process1, process2)),
                                      ('%s_1_%s_undecided' % (process1, process2), 'decide_%s_1?' % process2, '%s_1_%s_1' % (process1, process2)),
                                      ('%s_undecided_%s_0' % (process1, process2), 'decide_%s_0?' % process1, '%s_0_%s_0' % (process1, process2)),
                                      ('%s_undecided_%s_0' % (process1, process2), 'decide_%s_1?' % process1, '%s_1_%s_0' % (process1, process2)),
                                      ('%s_undecided_%s_1' % (process1, process2), 'decide_%s_0?' % process1, '%s_0_%s_1' % (process1, process2)),
                                      ('%s_undecided_%s_1' % (process1, process2), 'decide_%s_1?' % process1, '%s_1_%s_1' % (process1, process2))])


def deadlock_decisions(process1='p1', process2='p2'):
    return automaton.Automaton(name='decisions',
                               is_deadlock_automaton=True,
                               edges=[('q0', 'decide_{0}_0?'.format(process1), 'q1'),
                                      ('q0', 'decide_{0}_1?'.format(process1), 'q1'),
                                      ('q1', 'decide_{0}_0?'.format(process2), 'good'),
                                      ('q1', 'decide_{0}_1?'.format(process2), 'good'),
                                      ('q0', 'decide_{0}_0?'.format(process2), 'q2'),
                                      ('q0', 'decide_{0}_1?'.format(process2), 'q2'),
                                      ('q2', 'decide_{0}_0?'.format(process1), 'good'),
                                      ('q2', 'decide_{0}_1?'.format(process1), 'good')])


def consensus():
    p1 = process('p1')
    p2 = process('p2')
    p = product.Product([preference('p1'),
                         preference('p2'),
                         test_and_set("p1", "p2"),
                         shared_register("p1"),
                         shared_register("p2"),
                         p1,
                         p2,
                         deadlock_decisions(),
                         agreement_safety_monitor(),
                         wait_freedom_liveness_monitor('p1'),
                         wait_freedom_liveness_monitor('p2')])
    p.bad_state_predicates = [lambda s: (s.split(',')[5] == 'final' and
                                         s.split(',')[6] == 'final' and
                                         s.split(',')[7] != 'good')]
    p.equivalent_automata = [p1, p2]
    p.equivalent_names = ['p1', 'p2']
    return p


def consensus_correct():
    p1 = process_correct('p1')
    p2 = process_correct('p2')
    p = product.Product([preference('p1'),
                         preference('p2'),
                         test_and_set("p1", "p2"),
                         shared_register("p1"),
                         shared_register("p2"),
                         p1,
                         p2,
                         deadlock_decisions(),
                         agreement_safety_monitor(),
                         validity_safety_monitor(),
                         wait_freedom_liveness_monitor('p1'),
                         wait_freedom_liveness_monitor('p2')])
    p.equivalent_automata = [p1, p2]
    p.equivalent_names = ['p1', 'p2']
    return p


def consensus_from_fail_scenario():
    p1 = process_from_fail_scenario('p1')
    p2 = process_from_fail_scenario('p2')
    p = product.Product([preference('p1'),
                         preference('p2'),
                         test_and_set("p1", "p2"),
                         shared_register("p1"),
                         shared_register("p2"),
                         p1,
                         p2,
                         deadlock_decisions(),
                         agreement_safety_monitor(),
                         validity_safety_monitor(),
                         wait_freedom_liveness_monitor('p1'),
                         wait_freedom_liveness_monitor('p2')])
    p.bad_state_predicates = [lambda s: (s.split(',')[5] == 'final' and
                                         s.split(',')[6] == 'final' and
                                         s.split(',')[7] != 'good')]
    p.equivalent_automata = [p1, p2]
    p.equivalent_names = ['p1', 'p2']
    return p


def consensus_from_success_scenario():
    p1 = process_from_success_scenario('p1')
    p2 = process_from_success_scenario('p2')
    p = product.Product([preference('p1'),
                         preference('p2'),
                         test_and_set("p1", "p2"),
                         shared_register("p1"),
                         shared_register("p2"),
                         p1,
                         p2,
                         deadlock_decisions(),
                         agreement_safety_monitor(),
                         validity_safety_monitor(),
                         wait_freedom_liveness_monitor('p1'),
                         wait_freedom_liveness_monitor('p2')])
    p.bad_state_predicates = [lambda s: (s.split(',')[5] == 'final' and
                                         s.split(',')[6] == 'final' and
                                         s.split(',')[7] != 'good')]
    p.equivalent_automata = [p1, p2]
    p.equivalent_names = ['p1', 'p2']
    return p


def consensus_from_success_scenario_with_one_extra_state():
    consensus = consensus_from_success_scenario()
    p1 = consensus.automaton_by_name('p1')
    p2 = consensus.automaton_by_name('p2')
    p1.add_state()
    p2.add_state()
    return consensus


def consensus_from_success_and_fail_scenarios():
    p1 = process_from_success_and_fail_scenarios('p1')
    p2 = process_from_success_and_fail_scenarios('p2')
    p = product.Product([preference('p1'),
                         preference('p2'),
                         test_and_set("p1", "p2"),
                         shared_register("p1"),
                         shared_register("p2"),
                         p1,
                         p2,
                         deadlock_decisions(),
                         agreement_safety_monitor(),
                         validity_safety_monitor(),
                         wait_freedom_liveness_monitor('p1'),
                         wait_freedom_liveness_monitor('p2')
                     ])
    p.equivalent_automata = [p1, p2]
    p.equivalent_names = ['p1', 'p2']
    return p


def is_good_deadlock(consensus, state, process1='p1', process2='p2'):
    """
    A good deadlock must satisfy the following properties:
    agreement, the two processes have decided on the same value, and
    validity, the decision should equal one of the two preference values.
    """
    decision_state = consensus.automaton_state("decisions_listener", state)
    if decision_state.find('undecided') >= 0:
        return False
    match = re.match('%s_(\d)_%s_(\d)' % (process1, process2), decision_state)
    assert match
    decision1 = match.group(1)
    decision2 = match.group(2)
    if decision1 != decision2:
        return False
    preference_process1 = consensus.automaton_state("preference_%s" % process1, state)
    if preference_process1 == 'pref_after_choosing_0_%s' % process1:
        preference1 = '0'
    elif preference_process1 == 'pref_after_choosing_1_%s' % process1:
        preference1 = '1'
    preference_process2 = consensus.automaton_state("preference_%s" % process2, state)
    if preference_process2 == 'pref_after_choosing_0_%s' % process2:
        preference2 = '0'
    elif preference_process2 == 'pref_after_choosing_1_%s' % process2:
        preference2 = '1'
    # we know here that the decisions are the same
    return decision1 == preference1 or decision1 == preference2


# MONITORS


def agreement_safety_monitor(process1='p1', process2='p2'):
    """
    Listens to the decision messages emitted by the process automata and transitions to error if they disagree.
    """
    return automaton.Automaton(name='agreement_safety_monitor',
                               is_monitor=True, is_safety=True,
                               edges=[('both_undecided', 'decide_%s_0?' % process1, '%s_0_%s_undecided' % (process1, process2)),
                                      ('both_undecided', 'decide_%s_1?' % process1, '%s_1_%s_undecided' % (process1, process2)),
                                      ('both_undecided', 'decide_%s_0?' % process2, '%s_undecided_%s_0' % (process1, process2)),
                                      ('both_undecided', 'decide_%s_1?' % process2, '%s_undecided_%s_1' % (process1, process2)),
                                      ('%s_0_%s_undecided' % (process1, process2), 'decide_%s_0?' % process2, 'ok'),
                                      ('%s_0_%s_undecided' % (process1, process2), 'decide_%s_1?' % process2, 'error'),
                                      ('%s_1_%s_undecided' % (process1, process2), 'decide_%s_0?' % process2, 'error'),
                                      ('%s_1_%s_undecided' % (process1, process2), 'decide_%s_1?' % process2, 'ok'),
                                      ('%s_undecided_%s_0' % (process1, process2), 'decide_%s_0?' % process1, 'ok'),
                                      ('%s_undecided_%s_0' % (process1, process2), 'decide_%s_1?' % process1, 'error'),
                                      ('%s_undecided_%s_1' % (process1, process2), 'decide_%s_0?' % process1, 'error'),
                                      ('%s_undecided_%s_1' % (process1, process2), 'decide_%s_1?' % process1, 'ok')])


def validity_safety_monitor(process1='p1', process2='p2'):
    """
    Listens to preference messages and decision messages and transitions to the error state if the decided value
    is not one of the preference values.
    """
    return automaton.Automaton(name='validity_safety_monitor',
                               is_monitor=True, is_safety=True,
                               edges=[('no_value_preferred', '%s_prefer_0?' % process1, '0_has_been_preferred'),
                                      ('no_value_preferred', '%s_prefer_0?' % process2, '0_has_been_preferred'),
                                      ('no_value_preferred', '%s_prefer_1?' % process1, '1_has_been_preferred'),
                                      ('no_value_preferred', '%s_prefer_1?' % process2, '1_has_been_preferred'),
                                      ('0_has_been_preferred', '%s_prefer_1?' % process1, 'all_preferred'),
                                      ('0_has_been_preferred', '%s_prefer_1?' % process2, 'all_preferred'),
                                      ('1_has_been_preferred', '%s_prefer_0?' % process1, 'all_preferred'),
                                      ('1_has_been_preferred', '%s_prefer_0?' % process2, 'all_preferred'),
                                      ('0_has_been_preferred', 'decide_%s_1?' % process1, 'error'),
                                      ('0_has_been_preferred', 'decide_%s_1?' % process2, 'error'),
                                      ('1_has_been_preferred', 'decide_%s_0?' % process1, 'error'),
                                      ('1_has_been_preferred', 'decide_%s_0?' % process2, 'error')])


def wait_freedom_liveness_monitor(process):
    """
    The liveness monitor guarantees that in all executions one of the following messages will appear:
    decide_process_0, decide_process_1
    """
    a = automaton.Automaton(name="wait_freedom_liveness_monitor",
                            is_monitor=True,
                            is_liveness=True,
                            edges=[('live_havenotseen', 'decide_%s_0?' % process, 'live_seen'),
                                   ('live_havenotseen', 'decide_%s_1?' % process, 'live_seen')])
    a.make_accepting('live_havenotseen')
    return a
