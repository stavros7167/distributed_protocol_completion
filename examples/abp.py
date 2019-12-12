import itertools

import automaton
import examples.common
import product
import util


sender_scenario_no_loss = "before-sending-0L send? p0! a0'? before-sending-1L send? p1! a1'? before-sending-0L"

sender_scenario_lost_packet = "before-sending-0L send? p0! timeout? p0! a0'? before-sending-1L send? p1! a1'? before-sending-0L"

sender_scenario_lost_ack = "before-sending-0L send? p0! a0'? before-sending-1L send? p1! timeout? p1! a1'? before-sending-0L"

sender_scenario_premature_timeout = "before-sending-0L send? p0! a0'? before-sending-1L send? p1! timeout? p1! a1'? before-sending-0L send? p0! a1'? a0'? before-sending-1L"

sender_scenarios = [sender_scenario_no_loss,
                    sender_scenario_lost_packet,
                    sender_scenario_lost_ack,
                    sender_scenario_premature_timeout]

sender_scenarios += [util.switch_strings(s, "0", "1") for s in sender_scenarios]

receiver_scenario_no_loss = "waiting-for-0L p0'? deliver! a0! waiting-for-1L p1'? deliver! a1! waiting-for-0L"

receiver_scenario_irregular = "waiting-for-0L p0'? deliver! a0! waiting-for-1L p1'? deliver! a1! waiting-for-0L p1'? a1! waiting-for-0L p0'? deliver! a0! waiting-for-1L"

receiver_scenarios = [receiver_scenario_no_loss,
                      receiver_scenario_irregular]

receiver_scenarios += [util.switch_strings(s, "0", "1") for s in receiver_scenarios]

sender_one_scenario = [sender_scenario_no_loss]

sender_one_scenario += [util.switch_strings(s, "0", "1") for s in sender_one_scenario]

receiver_one_scenario = [receiver_scenario_no_loss]

receiver_one_scenario += [util.switch_strings(s, "0", "1") for s in receiver_one_scenario]

sender_one_scenario2 = [sender_scenario_lost_packet]

sender_one_scenario2 += [util.switch_strings(s, "0", "1") for s in sender_one_scenario2]

receiver_one_scenario2 = [receiver_scenario_no_loss]

receiver_one_scenario2 += [util.switch_strings(s, "0", "1") for s in receiver_one_scenario2]


def sender_with_one_scenario():
    sender = automaton.Automaton(name='sender',
                                 initial_state='before-sending-0',
                                 input_alphabet=["a0'", "a1'", "timeout", "send"],
                                 output_alphabet=["p0", "p1"],
                                 is_environment=False)
    for line in sender_one_scenario:
        sender.add_string(line)
    return sender


def receiver_with_one_scenario():
    receiver = automaton.Automaton(name="receiver",
                                   initial_state='waiting-for-0',
                                   is_environment=False)
    for line in receiver_one_scenario:
        receiver.add_string(line)
    return receiver


def sender_with_one_scenario2():
    sender = automaton.Automaton(name="sender",
                                 initial_state='before-sending-0',
                                 input_alphabet=["a0'", "a1'", "timeout", "send"],
                                 output_alphabet=["p0", "p1"],
                                 is_environment=False)
    for line in sender_one_scenario2:
        sender.add_string(line)
        return sender


def receiver_with_one_scenario2():
    receiver = automaton.Automaton(name="receiver",
                                   is_environment=False,
                                   initial_state='waiting-for-0')
    for line in receiver_one_scenario2:
        receiver.add_string(line)
        return receiver


def sender_with_four_scenarios():
    sender = automaton.Automaton(name="sender",
                                 initial_state='before-sending-0',
                                 input_alphabet=["a0'", "a1'", "timeout", "send"],
                                 output_alphabet=["p0", "p1"],

                                 is_environment=False)
    for line in sender_scenarios:
        sender.add_string(line)
    return sender


def receiver_with_four_scenarios():
    receiver = automaton.Automaton(name="receiver",
                                   is_environment=False,
                                   initial_state='waiting-for-0')
    for line in receiver_scenarios:
        receiver.add_string(line)
    return receiver


def sender_correct():
    sender = automaton.Automaton(name="sender_correct",
                                 initial_state='q0',
                                 is_environment=False)
    for source, label, target in [('q0', 'send?', 'q1'),
                                  ('q1', 'p0!', 'q2'),
                                  ('q2', 'timeout?', 'q1'),
                                  ('q2', "a1'?", 'q2'),
                                  ('q2', "a0'?", 'q3'),
                                  ('q3', 'send?', 'q4'),
                                  ('q4', 'p1!', 'q5'),
                                  ('q5', 'timeout?', 'q4'),
                                  ('q5', "a0'?", 'q5'),
                                  ('q5', "a1'?", 'q0')]:
        sender.add_edge(source, target, label=label)
    return sender


def receiver_correct():
    receiver = automaton.Automaton(name="receiver_correct",
                                   is_environment=False,
                                   initial_state='q0')
    for source, label, target in [('q0', "p0'?", 'q1'),
                                  ('q1', 'deliver!', 'q2'),
                                  ('q0', "p1'?", 'q3'),
                                  ('q3', 'a1!', 'q0'),
                                  ('q2', 'a0!', 'q4'),
                                  ('q4', "p0'?", 'q2'),
                                  ('q4', "p1'?", 'q5'),
                                  ('q5', 'deliver!', 'q3')]:
        receiver.add_edge(source, target, label=label)
    return receiver


def empty_sender():
    a = automaton.Automaton(name="empty_sender",
                            input_alphabet=["a0'", "a1'", "timeout", "send"],
                            output_alphabet=["p0", "p1"],
                            is_environment=False,
                            initial_state='q0')
    for i in range(6):
        a.add_node('q%d' % i)
    return a


def empty_receiver():
    a = automaton.Automaton(name="empty_receiver",
                            input_alphabet=["p0'", "p1'"],
                            output_alphabet=["a0", "a1", "deliver"],
                            is_environment=False,
                            initial_state='q0')
    for i in range(6):
        a.add_node('q%d' % i)
    return a


def forward_channel():
    return examples.common.lossy_duplicating_channel("ForwardChannel", ['p0', 'p1'], state_prefix="f")


def backward_channel():
    return examples.common.lossy_duplicating_channel("BackwardChannel", ['a0', 'a1'], state_prefix="b")


def safety_monitor():
    monitor = automaton.Automaton(name="safety_monitor",
                                  input_alphabet=["send", "deliver"],
                                  output_alphabet=[],
                                  is_environment=True,
                                  is_monitor=True,
                                  is_safety=True,
                                  initial_state='q0')
    monitor.add_edge('q0', 'q1', label='send?')
    monitor.add_edge('q1', 'q0', label='deliver?')
    monitor.input_complete('error')
    for message in monitor.input_alphabet:
        monitor.add_edge('error', 'error', label='%s?' % message)
    return monitor


def liveness_monitor_deliver_send():
    return examples.common.liveness_monitor("deliver", "send")


def liveness_monitor_send_deliver():
    return examples.common.liveness_monitor("send", "deliver")


system_common_automata = [
    forward_channel(),
    backward_channel(),
    examples.common.dummy_client(['send!', 'deliver?', 'timeout!'], ['deliver?']),
    safety_monitor(),
    liveness_monitor_deliver_send(),
    liveness_monitor_send_deliver()]


def system_with_four_scenarios(include_safety_monitors=True, include_liveness_monitors=True):
    automata = ([sender_with_four_scenarios(),
                 receiver_with_four_scenarios()] +
                system_common_automata)
    if not include_liveness_monitors:
        automata = [a for a in automata if not a.is_liveness]
    if not include_safety_monitors:
        automata = [a for a in automata if not a.is_safety]
    return product.Product(automata)


def system_with_one_scenario(include_safety_monitors=True, include_liveness_monitors=True):
    automata = [sender_with_one_scenario(), receiver_with_one_scenario()] + system_common_automata
    if not include_liveness_monitors:
        automata = [a for a in automata if not a.is_liveness]
    if not include_safety_monitors:
        automata = [a for a in automata if not a.is_safety]
    return product.Product(automata)


def system_with_one_scenario_no_send_follows_deliver():
    automata = [sender_with_one_scenario(), receiver_with_one_scenario(),
                forward_channel(),
                backward_channel(),
                examples.common.dummy_client(['send!', 'deliver?', 'timeout!'], ['deliver?']),
                safety_monitor(),
                liveness_monitor_send_deliver()]
    return product.Product(automata)


def system_with_one_scenario_infinite_sends():
    automata = [sender_with_one_scenario(), receiver_with_one_scenario(),
                forward_channel(),
                backward_channel(),
                examples.common.dummy_client(['send!', 'deliver?', 'timeout!'], ['deliver?']),
                safety_monitor(),
                liveness_monitor_send_deliver(),
                examples.common.liveness_monitor_infinitely_often('send', ['deliver', 'timeout', "a0'", 'a0', "p0'", 'p0', "p1'", 'p1', "a1'", 'a1'])]
    return product.Product(automata)


SYSTEM_WITH_ONE_SCENARIO_CORRECT_EDGES = [('sender', 'q2', 'timeout?', 'q1'),
                                          ('sender', 'q2', "a0'?", 'q2'),
                                          ('sender', 'q5', 'timeout?', 'q4'),
                                          ('sender', 'q5', "a1'?", 'q5'),
                                          ('receiver', 'q0', "p1'?", 'q5'),
                                          ('receiver', 'q3', "p0'?", 'q2')]


def system_with_one_scenario2():
    automata = [sender_with_one_scenario2(), receiver_with_one_scenario2()] + system_common_automata
    return product.Product(automata)


def system_empty():
    automata = ([empty_sender(), empty_receiver(), liveness_monitor_see_a_message("send")] +
                system_common_automata)
    return product.Product(automata)
