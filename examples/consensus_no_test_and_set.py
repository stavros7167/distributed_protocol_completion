import automaton
import consensus
import util
import product


def shared_register_with_null(process='p1'):
    return automaton.Automaton(name="shared_register_%s" % process,
                               edges=[('reg_null_%s' % process, '%s_set_0?' % process, 'reg_0_%s' % process),
                                      ('reg_null_%s' % process, '%s_set_1?' % process, 'reg_1_%s' % process),
                                      ('reg_null_%s' % process, '%s_set_null?' % process, 'reg_null_%s' % process),
                                      ('reg_0_%s' % process, '%s_set_1?' % process, 'reg_1_%s' % process),
                                      ('reg_0_%s' % process, '%s_set_0?' % process, 'reg_0_%s' % process),
                                      ('reg_0_%s' % process, '%s_set_null?' % process, 'reg_null_%s' % process),
                                      ('reg_1_%s' % process, '%s_set_1?' % process, 'reg_1_%s' % process),
                                      ('reg_1_%s' % process, '%s_set_0?' % process, 'reg_0_%s' % process),
                                      ('reg_1_%s' % process, '%s_set_null?' % process, 'reg_null_%s' % process),
                                      ('reg_null_%s' % process, '%s_read_null!' % process, 'reg_null_%s' % process),
                                      ('reg_0_%s' % process, '%s_read_0!' % process, 'reg_0_%s' % process),
                                      ('reg_1_%s' % process, '%s_read_1!' % process, 'reg_1_%s' % process)])


SCENARIO_PATTERN_PREFER_0_READ_0 = "initialL {process}_prefer_0? {process}_set_0! {other_process}_read_0? decide_{process}_0! finalL"
SCENARIO_PATTERN_PREFER_1_READ_0 = "initialL {process}_prefer_1? {process}_set_1! {other_process}_read_0? decide_{process}_1! finalL"
SCENARIO_PATTERN_PREFER_0_READ_1 = "initialL {process}_prefer_0? {process}_set_0! {other_process}_read_1? decide_{process}_1! finalL"
SCENARIO_PATTERN_PREFER_1_READ_1 = "initialL {process}_prefer_1? {process}_set_1! {other_process}_read_1? decide_{process}_1! finalL"

SCENARIOS = {'p1': [SCENARIO_PATTERN_PREFER_0_READ_0.format(process='p1', other_process='p2'),
                    SCENARIO_PATTERN_PREFER_1_READ_1.format(process='p1', other_process='p2')],
             'p2': [SCENARIO_PATTERN_PREFER_0_READ_0.format(process='p2', other_process='p1'),
                    SCENARIO_PATTERN_PREFER_1_READ_1.format(process='p2', other_process='p1')]}


def process_no_scenarios(process):
    other_process = util.switch_strings(process, "1", "2")
    input_message_formats = ["{process}_prefer_0", "{process}_prefer_1",
                             "{other_process}_read_0", "{other_process}_read_1", "{other_process}_read_null"]
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


def process_prefer0read0prefer1read1(process='p1'):
    p = process_no_scenarios(process)
    for scenario in SCENARIOS[process]:
        p.add_string(scenario)
    return p


def liveness_monitor(process):
    """
    The liveness monitor guarantees that in all executions one of the following messages will appear:
    decide_process_0, decide_process_1
    """
    a = automaton.Automaton(name="liveness_monitor_{0}".format(process),
                            is_monitor=True,
                            is_liveness=True,
                            edges=[('live_havenotseen', 'decide_%s_0?' % process, 'live_seen'),
                                   ('live_havenotseen', 'decide_%s_1?' % process, 'live_seen')])
    a.make_accepting('live_havenotseen')
    return a


def consensus_prefer0read0prefer1read1():
    p1 = process_prefer0read0prefer1read1('p1')
    p2 = process_prefer0read0prefer1read1('p2')
    p = product.Product([consensus.preference('p1'),
                         consensus.preference('p2'),
                         shared_register_with_null("p1"),
                         shared_register_with_null("p2"),
                         p1,
                         p2,
                         consensus.deadlock_decisions(),
                         liveness_monitor('p1'),
                         liveness_monitor('p2'),
                         consensus.agreement_safety_monitor(),
                         consensus.validity_safety_monitor()])
    p.bad_state_predicates = [lambda s: (s.split(',')[4] == 'final' and
                                         s.split(',')[5] == 'final' and
                                         s.split(',')[6] != 'good')]
    p.equivalent_automata = [p1, p2]
    p.equivalent_names = ['p1', 'p2']
    return p
