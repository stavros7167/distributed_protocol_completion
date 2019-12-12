import automaton
import common
import examples.abp
import examples.consensus


def test_add_edge():
    a = automaton.Automaton()
    a.add_edge('q0', 'q1', label='hello!')
    assert a.get_edge_data('q0', 'q1')
    assert 'hello!' in a.state_neighbors['q0']
    assert a.state_neighbors['q0']['hello!'] == ['q1']
    a.remove_edge_with_label('q0', 'q1', 'hello!')
    assert a.get_edge_data('q0', 'q1') is None
    assert 'hello!' not in a.state_neighbors['q0']
    a.add_edge('q0', 'q1', label='hello!')
    a.add_edge('q0', 'q1', label='world!')
    a.remove_edge_with_label('q0', 'q1', 'hello!')
    assert 'world!' in a.state_neighbors['q0']


def test_add_string():
    a1 = common.automaton1()
    assert 'label1' in a1.nodes()
    assert 'label2' in a1.nodes()
    a = automaton.Automaton()
    a.add_string('label1L a? b! label1L')
    assert len(a.nodes()) == 2
    a = automaton.Automaton()
    a.add_string("before-sending-0L a1'?")
    assert len(a.nodes()) == 2
    a = automaton.Automaton()
    a.add_string('l1L a?')
    a.add_string('l1L b?')
    assert len(a.nodes()) == 3


def test_outgoing_labels():
    ee = common.environment_example()
    pe = common.process_example()
    assert ee.outgoing_labels('e0') == ['a?']
    assert pe.outgoing_labels('p0') == ['a!']
    assert pe.outgoing_labels('p1') == []
    ee.add_edge('e0', 'e1', label='b?')
    assert set(ee.outgoing_labels('e0')) == set(['b?', 'a?'])


def test_input_output_state():
    pe = common.process_example()
    assert pe.is_output_state('p0')
    assert not pe.is_input_state('p0')
    assert not pe.is_output_state('p1')
    assert not pe.is_input_state('p1')


def test_remove_edge_with_label():
    g = automaton.Automaton()
    g.add_edge("q0", "q1", label="a")
    g.add_edge("q0", "q1", label="b")
    g.add_edge("q0", "q1", label="c")
    g.remove_edge_with_label("q0", "q1", "b")
    assert g.state_neighbors['q0'] == {'a': ['q1'], 'c': ['q1']}


def test_input_output_alphabet():
    a = automaton.Automaton()
    assert a.input_alphabet == []
    a = automaton.Automaton(input_alphabet=['b'])
    assert a.input_alphabet == ['b']
    a.add_edge('s1', 's2', label='a?')
    assert set(a.input_alphabet) == set(['a', 'b'])


def test_consensus_final_labels():
    scenario = examples.consensus.SCENARIOS['p1'][2]
    parsed_scenario = automaton.Automaton._parse_string(scenario)
    a = automaton.Automaton()
    a.add_string(scenario)
    assert 'initial' in a.node['initial']
    assert 'final' in a.node['final']
