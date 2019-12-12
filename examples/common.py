"""
TODO: make all channels emit monitor messages
TODO: What is the difference between one duplication and lossy one duplication channels?

When is a channel fair?
We say that the channel loses a message if it is not full, and the message is lost.
We say that a message is dropped if the channel is full and the message is lost.
We say that the channel receives a message if it is not lost or dropped.
If the channel is lossy, what is an unfair infinite execution?
An infinite execution is unfair if a message is lost infinitely often by a channel and
and the channel does not receive a message infinitely often.
"""

import itertools

import automaton


def really_lossless_channel(name, inputs, state_prefix=None, translate_message=None):
    """ This is used in VI. """
    if translate_message is None:
        translate_message = lambda s: s + "'"
    if state_prefix is None:
        state_prefix = name
    outputs = [i + "'" for i in inputs]
    a = automaton.Automaton(name=name,
                            input_alphabet=inputs,
                            output_alphabet=outputs,
                            initial_state=state_prefix + "_empty",
                            is_environment=True,
                            is_channel=True)
    for index, message in enumerate(inputs, 1):
        state = "%s_%s" % (state_prefix, message)
        a.add_edge(a.initial_state, state, label=("%s?" % message))
        a.add_edge(state, a.initial_state, label=("%s!" % translate_message(message)))
    a.strong_fairness_transitions = ([('{}_{}'.format(state_prefix, message),
                                       '{}\'!'.format(message),
                                       '{}_empty'.format(state_prefix)) for message in inputs] +
                                     [('{}_empty'.format(state_prefix),
                                       '{}?'.format(message),
                                       '{}_{}'.format(state_prefix, message)) for message in inputs])
    return a


def lossless_channel(name, inputs, state_prefix=None, translate_message=None):
    if translate_message is None:
        translate_message = lambda s: s + "'"
    if state_prefix is None:
        state_prefix = name
    a = really_lossless_channel(name, inputs, state_prefix, translate_message)
    for message in inputs:
        state = "%s_%s" % (state_prefix, message)
        for message2 in inputs:
            a.add_edge(state, state, label='%s?' % message2)
    return a


def lossy_one_duplication_channel(name, inputs, state_prefix=None, translate_message=None):
    """ Makes at most one duplication of a message. """
    if translate_message is None:
        translate_message = lambda s: s + "'"
    if state_prefix is None:
        state_prefix = name
    outputs = [translate_message(i) for i in inputs]
    a = automaton.Automaton(name=name,
                            input_alphabet=inputs,
                            output_alphabet=outputs,
                            initial_state=state_prefix + "_empty",
                            is_environment=True,
                            is_channel=True)
    # delivery
    for index, message in enumerate(inputs, 1):
        state = "%s_%s" % (state_prefix, message)
        one_duplication_state = "%s_%s_dup" % (state_prefix, message)
        a.add_edge(a.initial_state, state, label=("%s?" % message), monitor_label=(name + "_receive!"))
        a.add_edge(one_duplication_state, a.initial_state, label=("%s!" % translate_message(message)), monitor_label=(name + "_deliver!"))
        a.add_edge(state, a.initial_state, label=("%s!" % translate_message(message)), monitor_label=(name + "_deliver!"))

    # overflow
    for message in inputs:
        for state in ["%s_%s" % (state_prefix, message), "%s_%s_dup" % (state_prefix, message)]:
            for message2 in inputs:
                a.add_edge(state, state, label='%s?' % message2)
    # duplication
    for index, message in enumerate(inputs, 1):
        state = "%s_%s" % (state_prefix, message)
        one_duplication_state = "%s_%s_dup" % (state_prefix, message)
        a.add_edge(state, one_duplication_state, label=("%s!" % translate_message(message)), monitor_label=(name + "_duplicate!"))
    # message loss
    for message in inputs:
        a.add_edge("%s_empty" % state_prefix, "%s_empty" % state_prefix, label=("%s?" % message), monitor_label=(name + "_lose!"))
    return a


def lossy_duplicating_channel(name, inputs, state_prefix=None):
    translate_message = lambda s: s + "'"
    if state_prefix is None:
        state_prefix = name
    outputs = [translate_message(i) for i in inputs]
    a = automaton.Automaton(name=name,
                            input_alphabet=inputs,
                            output_alphabet=outputs,
                            initial_state=state_prefix + "_empty",
                            is_environment=True,
                            is_channel=True)
    # delivery
    for index, message in enumerate(inputs, 1):
        state = "%s_%s" % (state_prefix, message)
        a.add_edge(a.initial_state, state, label=("%s?" % message))
        a.add_edge(state, a.initial_state, label=("%s!" % translate_message(message)))
    # overflow
    for message in inputs:
        state = "{}_{}".format(state_prefix, message)
        for message2 in inputs:
            a.add_edge(state, state, label='%s?' % message2)
    # duplication
    for index, message in enumerate(inputs, 1):
        state = "%s_%s" % (state_prefix, message)
        a.add_edge(state, state, label=("%s!" % translate_message(message)))
    # message loss
    for message in inputs:
        a.add_edge("%s_empty" % state_prefix, "%s_empty" % state_prefix, label=("%s?" % message))
    a.strong_fairness_transitions = ([('{}_{}'.format(state_prefix, message),
                                       '{}\'!'.format(message),
                                       '{}_empty'.format(state_prefix))
                                      for message in inputs] +
                                     [('{}_empty'.format(state_prefix),
                                       '{}?'.format(message),
                                       '{}_{}'.format(state_prefix, message))
                                      for message in inputs])
    return a


def channel_with_loss_one_duplication(inputs,
                                      name=None,
                                      state_prefix=None,
                                      translate_message=None):
    """ Makes at most one duplication of a message. """
    if translate_message is None:
        translate_message = lambda s: s + "'"
    if state_prefix is None:
        state_prefix = name
    lose_message = name + "_lose"
    receive_message = name + "_receive"
    outputs = [translate_message(i) for i in inputs]
    empty_state = state_prefix + "_empty"
    a = automaton.Automaton(name=('channel' if name is None else name),
                            input_alphabet=inputs,
                            output_alphabet=outputs,
                            initial_state=empty_state,
                            is_environment=True,
                            is_channel=True)
    a.add_edge(state_prefix + "_empty", "lose", label=lose_message + "!")
    a.add_edge(state_prefix + "_empty", "receive", label=receive_message + "!")

    for message in inputs:
        a.add_edge("lose", empty_state, label=message + "?")

    for message in inputs:
        state = "{}_{}".format(state_prefix, message)
        duplication_state = state + "_dup"
        a.add_edge("receive", state, label=message + "?")
        a.add_edge(state, empty_state, label=translate_message(message) + "!")
        a.add_edge(state, duplication_state, label=translate_message(message) + "!")
        a.add_edge(duplication_state, empty_state, label=translate_message(message) + "!")
        for dropped_message in inputs:
            a.add_edge(state, state, label=dropped_message + "?")
            a.add_edge(duplication_state, duplication_state, label=dropped_message + "?")
    return a


def liveness_monitor(send, deliver):
    a = automaton.Automaton(name="liveness_monitor_%s_%s" % (send, deliver),
                            input_alphabet=[send, deliver],
                            output_alphabet=[],
                            initial_state='q0',
                            is_monitor=True,
                            is_liveness=True,
                            is_environment=True)
    a.add_edge('q0', 'q0', label=send + '?')
    a.add_edge('q0', 'q0', label=deliver + '?')
    a.add_edge('q0', 'q1', label=send + '?')
    a.add_edge('q1', 'q1', label=send + '?')
    a.add_edge('q1', 'q2', label=deliver + '?')
    a.add_edge('q2', 'q2', label=send + '?')
    a.add_edge('q2', 'q2', label=deliver + '?')

    a.make_accepting('q1')
    return a


def liveness_monitor_infinitely_often(event, other_inputs):
    a = automaton.Automaton(name="liveness_monitor_%s_%s" % (event, other_inputs),
                            input_alphabet=[event] + other_inputs,
                            output_alphabet=[],
                            initial_state='q0',
                            is_monitor=True,
                            is_liveness=True,
                            is_environment=True)
    for input in [event] + other_inputs:
        a.add_edge('q0', 'q0', label=input + '?')
        a.add_edge('q2', 'q2', label=input + '?')
        a.add_edge('q0', 'q1', label=input + '?')
    a.add_edge('q1', 'q2', label=event + '?')
    for input in other_inputs:
        a.add_edge('q1', 'q1', label=input + '?')
    a.make_accepting('q1')
    return a


def liveness_monitor_many_next_events(send, delivers):
    assert type(delivers) == list
    a = automaton.Automaton(name='liveness_monitor_{}_{}'.format(send, str(delivers)),
                            input_alphabet=[send] + delivers,
                            output_alphabet=[],
                            initial_state='q0',
                            is_monitor=True,
                            is_liveness=True,
                            is_environment=True)
    a.add_edge('q0', 'q0', label=send + '?')
    for deliver in delivers:
        a.add_edge('q0', 'q0', label=deliver + '?')
        a.add_edge('q1', 'q2', label=deliver + '?')
        a.add_edge('q2', 'q2', label=deliver + '?')
    a.add_edge('q0', 'q1', label=send + '?')
    a.add_edge('q1', 'q1', label=send + '?')
    a.add_edge('q2', 'q2', label=send + '?')

    a.make_accepting('q1')
    return a


def dummy_client(labels_or_label, strong_fairness_labels=None):
    a = automaton.Automaton(name="DummyClient",
                            is_environment=True,
                            initial_state='q0')
    if type(labels_or_label) == list:
        labels = labels_or_label
    else:
        labels = [labels_or_label]

    for label in labels:
        a.add_edge(a.initial_state, a.initial_state, label=label)
    if strong_fairness_labels is not None:
        a.strong_fairness_transitions = [('q0', label, 'q0') for label in strong_fairness_labels]
    return a
