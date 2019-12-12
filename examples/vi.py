import automaton
import common
import product
import util


cache1_lines = [
    # request flow 1
    "invalid_c1L req_client_c1? req_c1_dir! rsp_dir_c1'? req_ack_c1_dir! req_client_ack_c1! valid_c1L",
    # write back flow
    "valid_c1L wb_client_c1? wb_c1_dir! wb_ack_dir_c1'? wb_client_ack_c1! invalid_c1L",
    # request flow 2
    "invalid_c1L req_client_c1? req_c1_dir! rsp_dir_c1'? req_ack_c1_dir! req_client_ack_c1! valid_c1L",
    "valid_c1L inv_dir_c1'? inv_ack_c1_dir! invalid_c1L",
    # write back flow 2
    # this is the one to synthesize:
    # "valid_c1L wb_client_c1! wb_c1_dir! inv_dir_c1'? wb_ack_dir_c1'? invalid_c1L"
]


cache2_lines = [util.switch_strings(line, "1", "2") for line in cache1_lines]


directory_lines_1 = [
    # request flow 1
    "invalid_dirL req_c1_dir'? rsp_dir_c1! req_ack_c1_dir'? valid_dir_owner_c1L",
    # write back flow
    "valid_dir_owner_c1L wb_c1_dir'? wb_ack_dir_c1! invalid_dirL",
    # request flow 2
    "valid_dir_owner_c2L req_c1_dir'? inv_dir_c2! inv_ack_c2_dir'? rsp_dir_c1! req_ack_c1_dir'? valid_dir_owner_c1L",
    # write back flow 2
    # "valid_dir_owner_c1L req_c2_dir'? inv_dir_c1! wb_c1_dir'? wb_ack_dir_c1! rsp_dir_c2! req_ack_c2_dir'? valid_dir_owner_c2L"
]


directory_lines = directory_lines_1 + [util.switch_strings(line, "1", "2") for line in directory_lines_1]


def cache1():
    c = automaton.Automaton(name="cache1", is_environment=False, initial_state="invalid_c1")
    for line in cache1_lines:
        c.add_string(line)
    c.initial_state = "valid_c1"
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
    d.initial_state = "valid_dir_owner_c1"
    return d


def req_client(c='c1'):
    return automaton.Automaton(name="req_client_{0}".format(c),
                               is_environment=True,
                               initial_state='q0',
                               edges=[('q0', 'req_client_{0}!'.format(c), 'q0'),
                                      ('q0', 'req_client_ack_{0}?'.format(c), 'q0')])


def wb_client(c='c1'):
    a = automaton.Automaton(name="wb_client_{0}".format(c),
                            is_environment=True,
                            initial_state='q0',
                            edges=[('q0', 'wb_client_{0}!'.format(c), 'q0'),
                                   ('q0', 'wb_client_ack_{0}?'.format(c), 'q0')])
    a.strong_fairness_transitions = [('q0','wb_client_ack_{}?'.format(c), 'q0')]
    return a

def safety_monitor1():
    abpmonitor = automaton.Automaton(name="safety_monitor1",
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
    for message in abpmonitor.input_alphabet:
        abpmonitor.add_edge('error', 'error', label='%s?' % message)
    return abpmonitor


def safety_monitor2():
    abpmonitor = automaton.Automaton(name="safety_monitor2",
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
    for message in abpmonitor.input_alphabet:
        abpmonitor.add_edge('error', 'error', label='%s?' % message)
    return abpmonitor


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
    response_channel1 = common.really_lossless_channel("DirC1", inputs=[output for output in d.output_alphabet if output.find("1") >= 0])
    response_channel2 = common.really_lossless_channel("DirC2", inputs=[output for output in d.output_alphabet if output.find("2") >= 0])

    all_automata = [req_client('c1'), req_client('c2'), wb_client('c1'), wb_client('c2'), c1, response_channel1, request_channel1, d, request_channel2, response_channel2, c2, safety_monitor1(), safety_monitor2(), wb_liveness_monitor("c1"), wb_liveness_monitor("c2"), req_liveness_monitor("c1"), req_liveness_monitor("c2")]
    if not include_liveness_monitors:
        all_automata = [a for a in all_automata if not a.is_liveness]
    p = product.Product(all_automata)
    p.equivalent_automata = [c1, c2]
    p.equivalent_names = ["c1", "c2"]
    return p


CORRECT_EDGES = [('cache1', 'q7', "inv_dir_c1'?", 'q8'),
                 ('cache2', 'q7', "inv_dir_c2'?", 'q8'),
                 ('directory', 'q7', "wb_c2_dir'?", 'q8'),
                 ('directory', 'q14', "wb_c1_dir'?", 'q15')]


def wb_liveness_monitor(cache):
    request = 'wb_client_%s' % cache
    ack = 'wb_client_ack_%s' % cache
    a = automaton.Automaton(name='wb_client_liveness_monitor',
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


def req_liveness_monitor(cache):
    request = 'req_client_%s' % cache
    ack = 'req_client_ack_%s' % cache
    a = automaton.Automaton(name='req_client_liveness_monitor',
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
