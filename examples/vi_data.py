import automaton
import common
import product
import util


cache1_lines_d0 = [
    # request flow 1
    "invalid_c1L req_client_c1? req_c1_dir! rsp_dir_c1_d0'? req_ack_c1_dir! req_client_ack_c1! valid_c1_d0L",
    # write back flow
    "valid_c1_d0L wb_client_c1? wb_c1_dir_d0! wbackc1L wb_ack_dir_c1'? wb_client_ack_c1! invalid_c1L",
    # request flow 2
    "invalid_c1L req_client_c1? req_c1_dir! rsp_dir_c1_d0'? req_ack_c1_dir! req_client_ack_c1! valid_c1_d0L",
    "valid_c1_d0L inv_dir_c1'? inv_ack_c1_dir_d0! invalid_c1L",
    # havoc flow
    "valid_c1_d0L c1_havoc_to_d1? valid_c1_d1L"
    # write back flow 2
    # this is the one to synthesize:
    # "valid_c1L wb_client_c1! wb_c1_dir! inv_dir_c1'? wb_ack_dir_c1'? invalid_c1L"
]


cache1_lines_d1 = [util.switch_strings(line, "d0", "d1") for line in cache1_lines_d0]


cache1_lines = cache1_lines_d0 + cache1_lines_d1


cache2_lines_d0 = [util.switch_strings(line, "c1", "c2") for line in cache1_lines_d0]


cache2_lines_d1 = [util.switch_strings(line, "d0", "d1") for line in cache2_lines_d0]


cache2_lines = cache2_lines_d0 + cache2_lines_d1


directory_lines_d0 = [
    # request flow 1
    "invalid_dir_d0L req_c1_dir'? rsp_dir_c1_d0! req_ack_c1_dir'? valid_dir_owner_c1L",
    # write back flow
    "valid_dir_owner_c1L wb_c1_dir_d0'? wb_ack_dir_c1! invalid_dir_d0L",
    # request flow 2
    "valid_dir_owner_c2L req_c1_dir'? inv_dir_c2! inv_ack_c2_dir_d0'? rsp_dir_c1_d0! req_ack_c1_dir'? valid_dir_owner_c1L",
    # write back flow 2
    # "valid_dir_owner_c1L req_c2_dir'? inv_dir_c1! wb_c1_dir'? wb_ack_dir_c1! rsp_dir_c2! req_ack_c2_dir'? valid_dir_owner_c2L"
]


directory_lines_d1 = [util.switch_strings(line, "d0", "d1") for line in directory_lines_d0]


directory_lines_1 = directory_lines_d0 + directory_lines_d1


directory_lines = directory_lines_1 + [util.switch_strings(line, "c1", "c2") for line in directory_lines_1]


def cache1():
    c = automaton.Automaton(name="cache1", is_environment=False, initial_state="invalid_c1")
    for line in cache1_lines:
        c.add_string(line)
    c.initial_state = "invalid_c1"
    return c


def cache2():
    c = automaton.Automaton(name="cache2", is_environment=False, initial_state="invalid_c2")
    for line in cache2_lines:
        c.add_string(line)
    c.initial_state = "invalid_c2"
    return c


def directory():
    d = automaton.Automaton(name="directory", is_environment=False)
    for line in directory_lines:
        d.add_string(line)
    d.initial_state = "invalid_dir_d0"
    return d


def client():
    dummy = common.dummy_client(['req_client_c1!', 'req_client_c2!', 'wb_client_c1!', 'wb_client_c2!',
                                 'c1_havoc_to_d0!', 'c1_havoc_to_d1!', 'c2_havoc_to_d0!', 'c2_havoc_to_d1!',
                                 'req_client_ack_c1?', 'req_client_ack_c2?', 'wb_client_ack_c1?', 'wb_client_ack_c2?'])
    dummy.strong_fairness_transitions = [('q0', 'wb_client_ack_c1?', 'q0'),
                                     ('q0', 'wb_client_ack_c2?', 'q0')]

    return dummy

def coherence_monitor():
    """ Initially the correct value is 0,
        whenever there is a havoc,
    """
    a = automaton.Automaton(name="CoherenceMonitor", input_alphabet=['c1_havoc_to_d0?', 'c1_havoc_to_d1?', 'c2_havoc_to_d0?', 'c2_havoc_to_d1?'],
                            initial_state='q0', is_monitor=True, is_liveness=False, is_safety=True, is_environment=True, is_bad_predicate_monitor=True)
    for label in ['c1_havoc_to_d1?', 'c2_havoc_to_d1?']:
        a.add_edge('q0', 'q1', label=label)
    for label in ['c1_havoc_to_d0?', 'c2_havoc_to_d0?']:
        a.add_edge('q1', 'q0', label=label)
    return a


def is_bad_state_coherence(vi, state):
    automata_states = state.split(',')
    automata_names = ["cache1", "directory", "cache2", "CoherenceMonitor"]
    (cache1_index, cache1), (directory_index, directory), (cache2_index, cache2), (coherence_index, coherence) = [vi.automaton_index_by_name(name)
                                                                                                                  for name in automata_names]
    coherence_state = automata_states[coherence_index]
    cache1_state = automata_states[cache1_index]
    cache2_state = automata_states[cache2_index]
    directory_state = automata_states[directory_index]
    cache1_d0_state = 'valid_c1_d0'
    cache1_d1_state = 'valid_c1_d1'
    cache2_d0_state = 'valid_c2_d0'
    cache2_d1_state = 'valid_c2_d1'
    directory_d0_state = 'invalid_dir_d0'
    directory_d1_state = 'invalid_dir_d1'
    return ((cache1_state == cache1_d0_state and coherence_state == 'q1') or
            (cache1_state == cache1_d1_state and coherence_state == 'q0') or
            (cache2_state == cache2_d0_state and coherence_state == 'q1') or
            (cache2_state == cache2_d1_state and coherence_state == 'q0') or
            (directory_state == directory_d0_state and coherence_state == 'q1') or
            (directory_state == directory_d1_state and coherence_state == 'q0'))


def safety_monitor1():
    abpmonitor = automaton.Automaton(name="safety_monitor",
                                     input_alphabet=["req_client_c1", "wb_client_c1", "req_client_ack_c1", "wb_client_ack_c1"],
                                     output_alphabet=[],
                                     is_environment=True,
                                     is_monitor=True,
                                     is_safety=True,
                                     initial_state='q0')
    abpmonitor.add_edge('q0', 'q1', label='req_client_c1?')
    abpmonitor.add_edge('q1', 'q0', label='req_client_ack_c1?')
    abpmonitor.add_edge('q0', 'q2', label='wb_client_c1?')
    abpmonitor.add_edge('q2', 'q0', label='wb_client_ack_c1?')
    abpmonitor.input_complete('error')
    for message in ['c1_havoc_to_d0', 'c1_havoc_to_d1']:
        abpmonitor.add_edge('q1', 'error', label=message + '?')
        abpmonitor.add_edge('q2', 'error', label=message + '?')
        abpmonitor.add_edge('q0', 'q0', label=message + '?')
    for message in abpmonitor.input_alphabet:
        abpmonitor.add_edge('error', 'error', label='%s?' % message)
    return abpmonitor


def safety_monitor2():
    abpmonitor = automaton.Automaton(name="safety_monitor",
                                     input_alphabet=["req_client_c2", "wb_client_c2", "req_client_ack_c2", "wb_client_ack_c2"],
                                     output_alphabet=[],
                                     is_environment=True,
                                     is_monitor=True,
                                     is_safety=True,
                                     initial_state='q0')
    abpmonitor.add_edge('q0', 'q1', label='req_client_c2?')
    abpmonitor.add_edge('q1', 'q0', label='req_client_ack_c2?')
    abpmonitor.add_edge('q0', 'q2', label='wb_client_c2?')
    abpmonitor.add_edge('q2', 'q0', label='wb_client_ack_c2?')
    abpmonitor.input_complete('error')
    for message in ['c2_havoc_to_d0', 'c2_havoc_to_d1']:
        abpmonitor.add_edge('q1', 'error', label=message + '?')
        abpmonitor.add_edge('q2', 'error', label=message + '?')
        abpmonitor.add_edge('q0', 'q0', label=message + '?')
    for message in abpmonitor.input_alphabet:
        abpmonitor.add_edge('error', 'error', label='%s?' % message)
    return abpmonitor


def req_client(c='c1'):
    return automaton.Automaton(name="req_client_{0}".format(c),
                               is_environment=True,
                               initial_state='q0',
                               edges=[('q0', 'req_client_{0}!'.format(c), 'q0'),
                                      ('q0', 'req_client_ack_{0}?'.format(c), 'q0')])


def wb_client(c='c1'):
    return automaton.Automaton(name="wb_client_{0}".format(c),
                               is_environment=True,
                               initial_state='q0',
                               edges=[('q0', 'wb_client_{0}!'.format(c), 'q0'),
                                      ('q0', 'wb_client_ack_{0}?'.format(c), 'q0')])


def havoc_client(c='c1'):
    return automaton.Automaton(name="havoc_client_{0}".format(c),
                               is_environment=True,
                               initial_state='q0',
                               edges=[('q0', '{}_havoc_to_d1!'.format(c), 'q0'),
                                      ('q0', '{}_havoc_to_d2!'.format(c), 'q0')])


def vi(include_liveness_monitors=True):
    c1 = cache1()
    c2 = cache2()
    d = directory()
    inputs = list(c1.output_alphabet)
    inputs.remove('req_client_ack_c1')
    inputs.remove('wb_client_ack_c1')
    request_channel1 = common.really_lossless_channel("C1Dir", inputs=inputs)
    inputs = list(c2.output_alphabet)
    inputs.remove('req_client_ack_c2')
    inputs.remove('wb_client_ack_c2')
    request_channel2 = common.really_lossless_channel("C2Dir", inputs=inputs)
    response_channel1 = common.really_lossless_channel("DirC1", inputs=[output for output in d.output_alphabet if output.find("c1") >= 0])
    response_channel2 = common.really_lossless_channel("DirC2", inputs=[output for output in d.output_alphabet if output.find("c2") >= 0])
    all_automata = [
        # req_client('c1'), req_client('c2'), wb_client('c1'), wb_client('c2'), havoc_client('c1'), havoc_client('c2'),
        client(),
        c1, response_channel1, request_channel1, d, request_channel2, response_channel2, c2, coherence_monitor(),
        safety_monitor1(), safety_monitor2(),
        wb_liveness_monitor("c1"), wb_liveness_monitor("c2"), req_liveness_monitor("c1"), req_liveness_monitor("c2")]
    if not include_liveness_monitors:
        all_automata = [a for a in all_automata if not a.is_liveness]
    # liveness_monitor_req_wb_c2(), liveness_monitor_req_wb_c1()]
    vi = product.Product(all_automata)
    vi.bad_state_predicates = [lambda state: is_bad_state_coherence(vi, state), lambda state: is_bad_state(vi, state)]
    vi.equivalent_names = ["c1", "c2"]
    return vi


def wb_liveness_monitor(cache='c1'):
    request = 'wb_client_%s' % cache
    ack = 'wb_client_ack_%s' % cache
    a = automaton.Automaton(name='wb_liveness_monitor_{}'.format(cache),
                            input_alphabet=[request, ack],
                            initial_state='q0',
                            is_monitor=True,
                            is_liveness=True,
                            is_environment=True)
    for start, message, end in [('q0', request, 'q1'),
                                ('q0', request, 'q0'),
                                ('q0', ack, 'q0'),
                                ('q1', request, 'q1'),
                                ('q1', ack, 'q2'),
                                ('q2', request, 'q2'),
                                ('q2', ack, 'q2')]:
        a.add_edge(start, end, label=("%s?" % message))
    # any states
    a.make_accepting('q1')
    return a


def req_liveness_monitor(cache='c1'):
    request = 'req_client_%s' % cache
    ack = 'req_client_ack_%s' % cache
    a = automaton.Automaton(name='req_liveness_monitor_{}'.format(cache),
                            input_alphabet=[request, ack],
                            initial_state='q0',
                            is_monitor=True,
                            is_liveness=True,
                            is_environment=True)
    for start, message, end in [('q0', request, 'q1'),
                                ('q0', request, 'q0'),
                                ('q0', ack, 'q0'),
                                ('q1', request, 'q1'),
                                ('q1', ack, 'q2'),
                                ('q2', request, 'q2'),
                                ('q2', ack, 'q2')]:
        a.add_edge(start, end, label=("%s?" % message))
    # any states
    a.make_accepting('q1')
    return a


def is_bad_state(vi, state):
    automata_states = state.split(',')

    automata_names = ["cache1", "directory", "cache2"]

    (cache1_index, cache1), (directory_index, directory), (cache2_index, cache2) = [vi.automaton_index_by_name(name)
                                                                                    for name in automata_names]

    valid_c1_states = ['valid_c1_d0', 'valid_c1_d1']
    invalid_c1_state = 'invalid_c1'
    valid_c2_states = ['valid_c2_d0', 'valid_c2_d1']
    invalid_c2_state = 'invalid_c2'
    directory_valid_owner_c1_state = 'valid_dir_owner_c1'
    directory_valid_owner_c2_state = 'valid_dir_owner_c2'
    directory_invalid_states = ['invalid_dir_d0', 'invalid_dir_d1']

    stable_states = {'cache1': valid_c1_states + [invalid_c1_state],
                     'cache2': valid_c2_states + [invalid_c2_state],
                     'directory': [directory_valid_owner_c1_state, directory_valid_owner_c2_state] + directory_invalid_states}
    automata_indices = dict([(name, vi.automaton_index_by_name(name)[0]) for name in automata_names])

    if any(automata_states[automaton_index] not in stable_states[automaton_name]
           for automaton_name, automaton_index in automata_indices.items()):
        return False

    good_combinations = ([(invalid_c1_state, directory_invalid_state, invalid_c2_state) for directory_invalid_state in directory_invalid_states] +
                         [(valid_c1_state, directory_valid_owner_c1_state, invalid_c2_state) for valid_c1_state in valid_c1_states] +
                         [(invalid_c1_state, directory_valid_owner_c2_state, valid_c2_state) for valid_c2_state in valid_c2_states])

    process_automata_states = (automata_states[cache1_index], automata_states[directory_index], automata_states[cache2_index])

    if process_automata_states in good_combinations:
        return False
    else:
        return True
