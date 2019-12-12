"""
Refactor liveness monitor and use the same with no color ABP
"""

import itertools

import automaton
import examples.common
import product
import util


sender_scenarios = [
    # no loss
    "before-sending-0L send-blue? p0blue! a0'? before-sending-1L send-red? p1red! a1'? before-sending-0L",
    # lost packet
    "before-sending-0L send-blue? p0blue! timeout? p0blue! a0'? before-sending-1L send-red? p1red! a1'? before-sending-0L",
    # lost ack
    "before-sending-0L send-blue? p0blue! a0'? before-sending-1L send-red? p1red! timeout? p1red! a1'? before-sending-0L",
    # premature timeout
    "before-sending-0L send-blue? p0blue! a0'? before-sending-1L send-red? p1red! timeout? p1red! a1'? before-sending-0L send-blue? p0blue! a1'? a0'? before-sending-1L"
]

sender_scenarios += [util.switch_strings(s, "0", "1") for s in sender_scenarios]

sender_scenarios += [util.switch_strings(s, "blue", "red") for s in sender_scenarios]

receiver_scenarios = [
    "waiting-for-0L p0blue'? deliver-blue! a0! waiting-for-1L p1red'? deliver-red! a1! waiting-for-0L p1red'? a1! waiting-for-0L",
    "waiting-for-0L p0red'? deliver-red! a0! waiting-for-1L p1blue'? deliver-blue! a1! waiting-for-0L p1blue'? a1! waiting-for-0L",
    "waiting-for-1L p1red'? deliver-red! a1! waiting-for-0L p0blue'? deliver-blue! a0! waiting-for-1L p0blue'? a0! waiting-for-1L",
    "waiting-for-0L p0blue'? deliver-blue! a0! waiting-for-1L p1red'? deliver-red! a1! waiting-for-0L",
    "waiting-for-0L p0red'? deliver-red! a0! waiting-for-1L p1blue'? deliver-blue! a1! waiting-for-0L",
    "waiting-for-0L p0blue'? deliver-blue! a0! waiting-for-1L p1red'? deliver-red! a1! waiting-for-0L",
    "waiting-for-0L p0red'? deliver-red! a0! waiting-for-1L p1blue'? deliver-blue! a1! waiting-for-0L",
    "waiting-for-0L p0blue'? deliver-blue! a0! waiting-for-1L p1red'? deliver-red! a1! waiting-for-0L",
    "waiting-for-0L p0blue'? deliver-blue! a0! waiting-for-1L p1red'? deliver-red! a1! waiting-for-0L p1red'? a1! waiting-for-0L p0blue'? deliver-blue! a0! waiting-for-1L",
    "waiting-for-0L p0red'? deliver-red! a0! waiting-for-1L p1blue'? deliver-blue! a1! waiting-for-0L p1blue'? a1! waiting-for-0L p0red'? deliver-red! a0! waiting-for-1L"
]

receiver_scenarios += [util.switch_strings(s, "0", "1") for s in receiver_scenarios]

sender_one_scenario = [
    "before-sending-0L send-blue? p0blue! a0'? before-sending-1L send-red? p1red! a1'? before-sending-0L"
]

sender_one_scenario += [util.switch_strings(s, "0", "1") for s in sender_one_scenario]

sender_one_scenario += [util.switch_strings(s, "blue", "red") for s in sender_one_scenario]

receiver_one_scenario = [
    "waiting-for-0L p0blue'? deliver-blue! a0! waiting-for-1L p1red'? deliver-red! a1! waiting-for-0L"
]

receiver_one_scenario += [util.switch_strings(s, "0", "1") for s in receiver_one_scenario]

receiver_one_scenario += [util.switch_strings(s, "blue", "red") for s in receiver_one_scenario]

sender_one_scenario2 = [
    # lost packet
    "before-sending-0L send-blue? p0blue! timeout? p0blue! a0'? before-sending-1L send-red? p1red! a1'? before-sending-0L"
]

sender_one_scenario2 += [util.switch_strings(s, "0", "1") for s in sender_one_scenario2]

sender_one_scenario2 += [util.switch_strings(s, "blue", "red") for s in sender_one_scenario2]

receiver_one_scenario2 = [
    "waiting-for-0L p0blue'? deliver-blue! a0! waiting-for-1L p1red'? deliver-red! a1! waiting-for-0L"
]

receiver_one_scenario2 += [util.switch_strings(s, "0", "1") for s in receiver_one_scenario2]

receiver_one_scenario2 += [util.switch_strings(s, "blue", "red") for s in receiver_one_scenario2]


def sender_with_one_scenario():
    sender = automaton.Automaton(name="sender",
                                 initial_state='before-sending-0',
                                 input_alphabet=["a0'", "a1'", "timeout", "send-blue", "send-red"],
                                 output_alphabet=["p0blue", "p0red", "p1blue", "p1red"],
                                 is_environment=False)
    for line in sender_one_scenario:
        sender.add_string(line)
    return sender


def receiver_with_one_scenario():
    receiver = automaton.Automaton(name="receiver",
                                   input_alphabet=["p0blue'", "p0red'", "p1blue'", "p1red'"],
                                   output_alphabet=["a0", "a1", "deliver-blue", "deliver-red"],
                                   is_environment=False,
                                   initial_state='waiting-for-0')
    for line in receiver_one_scenario:
        receiver.add_string(line)
    return receiver


def sender_with_one_scenario2():
    sender = automaton.Automaton(name="sender",
                                 initial_state='before-sending-0',
                                 input_alphabet=["a0'", "a1'", "timeout", "send-blue", "send-red"],
                                 output_alphabet=["p0blue", "p0red", "p1blue", "p1red"],
                                 is_environment=False)
    for line in sender_one_scenario2:
        sender.add_string(line)
    return sender


def receiver_with_one_scenario2():
    receiver = automaton.Automaton(name="receiver",
                                   input_alphabet=["p0blue'", "p0red'", "p1blue'", "p1red'"],
                                   output_alphabet=["a0", "a1", "deliver-blue", "deliver-red"],
                                   is_environment=False,
                                   initial_state='waiting-for-0')
    for line in receiver_one_scenario2:
        receiver.add_string(line)
    return receiver


def sender_with_four_scenarios():
    sender = automaton.Automaton(name="sender",
                                 initial_state='before-sending-0',
                                 input_alphabet=["a0'", "a1'", "timeout", "send-blue", 'send-red'],
                                 output_alphabet=["p0blue", "p1blue", "p0red", "p1red"],
                                 is_environment=False)
    for line in sender_scenarios:
        sender.add_string(line)
    return sender


def receiver_with_four_scenarios():
    receiver = automaton.Automaton(name="receiver",
                                   input_alphabet=["p0blue'", "p0red'", "p1blue'", "p1red'"],
                                   output_alphabet=["a0", "a1", "deliver-blue", "deliver-red"],
                                   is_environment=False,
                                   initial_state='waiting-for-0')
    for line in receiver_scenarios:
        receiver.add_string(line)
    return receiver


def sender_correct():
    sender = automaton.Automaton(name="sender_correct",
                                 initial_state='q0',
                                 input_alphabet=["a0'", "a1'", "timeout", "send-blue", "send-red"],
                                 output_alphabet=["p0blue", "p0red", "p1blue", "p1red"],
                                 is_environment=False,
                                 is_monitor=False)
    for source, label, target in [('q0', 'send-blue?', 'q1'),
                                  ('q1', 'p0blue!', 'q2'),
                                  ('q2', 'timeout?', 'q1'),
                                  ('q2', "a1'?", 'q2'),
                                  ('q2', "a0'?", 'q3'),
                                  ('q3', 'send-red?', 'q4'),
                                  ('q4', 'p1red!', 'q5'),
                                  ('q5', 'timeout?', 'q4'),
                                  ('q5', "a0'?", 'q5'),
                                  ('q5', "a1'?", 'q0'),
                                  ('q0', 'send-red?', 'q8'),
                                  ('q8', 'p0red!', 'q9'),
                                  ('q9', 'timeout?', 'q8'),
                                  ('q9', "a1'?", 'q9'),
                                  ('q9', "a0'?", 'q3'),
                                  ('q3', 'send-blue?', 'q6'),
                                  ('q6', 'p1blue!', 'q7'),
                                  ('q7', 'timeout?', 'q6'),
                                  ('q7', "a0'?", 'q7'),
                                  ('q7', "a1'?", 'q0')]:
        sender.add_edge(source, target, label=label)
    return sender


def receiver_correct():
    receiver = automaton.Automaton(name="receiver_correct",
                                   input_alphabet=["p0blue'", "p0red'", "p1blue'", "p1red'"],
                                   output_alphabet=["a0", "a1", "deliver-blue", "deliver-red"],
                                   is_environment=False,
                                   initial_state='q0')
    for source, label, target in [('q0', "p0blue'?", 'q1'),
                                  ('q1', 'deliver-blue!', 'q2'),
                                  ('q0', "p0red'?", 'q3'),
                                  ('q3', 'deliver-red!', 'q2'),
                                  ('q0', "p1blue'?", 'q4'),
                                  ('q0', "p1red'?", 'q4'),
                                  ('q4', 'a1!', 'q0'),
                                  ('q2', 'a0!', 'q5'),
                                  ('q5', "p0red'?", 'q2'),
                                  ('q5', "p0blue'?", 'q2'),
                                  ('q5', "p1blue'?", 'q6'),
                                  ('q6', 'deliver-blue!', 'q4'),
                                  ('q5', "p1red'?", 'q7'),
                                  ('q7', 'deliver-red!', 'q4')]:
        receiver.add_edge(source, target, label=label)
    return receiver


def forward_channel():
    return examples.common.lossy_duplicating_channel("ForwardChannel", ['p0blue', 'p0red', 'p1blue', 'p1red'], state_prefix="f")


def backward_channel():
    return examples.common.lossy_duplicating_channel("BackwardChannel", ['a0', 'a1'], state_prefix="b")


def safety_monitor(send='send-blue', deliver='deliver-blue', other_sends=['send-red'], other_delivers=['deliver-red']):
    all_inputs = [send, deliver] + other_sends + other_delivers
    monitor = automaton.Automaton(name="safety_monitor",
                                  input_alphabet=all_inputs,
                                  output_alphabet=[],
                                  is_environment=True,
                                  is_monitor=True,
                                  is_safety=True,
                                  initial_state='q0')
    monitor.add_edge('q0', 'q1', label='{}?'.format(send))
    monitor.add_edge('q1', 'q0', label='{}?'.format(deliver))
    for other_send in other_sends:
        monitor.add_edge('q0', 'q0', label='{}?'.format(other_send))
    for any_send in [send] + other_sends:
        monitor.add_edge('q1', 'error', label='{}?'.format(any_send))
    for other_deliver in other_delivers:
        monitor.add_edge('q0', 'q0', label=other_deliver + '?')
    monitor.add_edge('q0', 'error', label='{}?'.format(deliver))
    for other_deliver in other_delivers:
        monitor.add_edge('q1', 'q1', label=other_deliver + '?')
    return monitor


system_common_automata = [
    forward_channel(),
    backward_channel(),
    safety_monitor("send-blue", "deliver-blue",
                   ['send-red'], ['deliver-red']),
    safety_monitor("send-red", "deliver-red",
                   ['send-blue'], ['deliver-blue']),
    examples.common.liveness_monitor('send-blue', 'deliver-blue'),
    examples.common.liveness_monitor_many_next_events('deliver-blue', ['send-blue', 'send-red']),
    examples.common.liveness_monitor('send-red', 'deliver-red'),
    examples.common.liveness_monitor_many_next_events('deliver-red', ['send-blue', 'send-red']),
    examples.common.dummy_client(['timeout!', 'send-blue!', 'send-red!', 'deliver-blue?', 'deliver-red?'], ['deliver-blue?', 'deliver-red?'])]


def system_correct():
    return product.Product([sender_correct(),
                            receiver_correct()] + system_common_automata)


def system_with_one_scenario():
    automata = [sender_with_one_scenario(), receiver_with_one_scenario()] + system_common_automata
    return product.Product(automata)


def system_with_one_scenario2():
    automata = [sender_with_one_scenario2(), receiver_with_one_scenario2()] + system_common_automata
    return product.Product(automata)


def system_with_four_scenarios(include_liveness_monitors=True):
    automata = [sender_with_four_scenarios(), receiver_with_four_scenarios()] + system_common_automata
    if not include_liveness_monitors:
        automata = [a for a in automata if not a.is_liveness]
    return product.Product(automata)


def liveness_monitor_see_a_message(message):
    label = '%s?' % message
    a = automaton.Automaton(name="LivenessMonitor",
                            is_monitor=True,
                            input_alphabet=[message,
                                            "p0", "p1", "a0", "a1",
                                            "p0'", "p1'", "a0'", "a1'"],
                            output_alphabet=[],
                            initial_state='q0',
                            is_liveness=True,
                            is_environment=True)
    for message in a.input_alphabet:
        a.add_edge('q0', 'q0', label="%s?" % message)

    a.add_edge('q0', 'q1', label=label)

    a.make_accepting('q0')
    return a


SYSTEM_WITH_FOUR_SCENARIOS_CORRECT_EDGES = [
    ('sender', 'q18', 'timeout?', 'q13'),
    ('sender', 'q7', 'timeout?', 'q1'),
    ('sender', 'q20', 'timeout?', 'q18'),
    ('sender', 'q10', 'timeout?', 'q7'),
    ('sender', 'q9', 'timeout?', 'q4'),
    ('sender', 'q16', 'timeout?', 'q11'),
    ('sender', 'q19', 'timeout?', 'q16'),
    ('sender', 'q21', 'timeout?', 'q9')
]
