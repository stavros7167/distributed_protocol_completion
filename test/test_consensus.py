"""
TODO When I disable transitions from initial state I get a solution that
     does not appear when I enumerate all solutions
"""

import cegis
import examples.consensus


def test_correct_consensus():
    consensus = examples.consensus.consensus_correct()
    assert consensus.deadlock_states() == []
    assert not consensus.cycle()
    assert consensus.is_safe()
    assert consensus.cycle() == []


def test_consensus_with_success_and_fail_scenarios():
    consensus = examples.consensus.consensus_from_success_and_fail_scenarios()
    assert consensus.deadlock_states() == []
    assert not consensus.cycle()
    assert consensus.is_safe()
    assert consensus.cycle() == []


def test_completion_for_consensus_from_fail_scenario():
    consensus = examples.consensus.consensus_from_fail_scenario()
    completion = [('p1', 'q1', 'p1_test_and_set_0?', 'q3'),
                  ('p1', 'q5', 'p1_test_and_set_0?', 'q8'),
                  ('p2', 'q1', 'p2_test_and_set_0?', 'q3'),
                  ('p2', 'q5', 'p2_test_and_set_0?', 'q8')]
    consensus.add_automata_edges_by_name(completion)
    assert consensus.real_deadlock_states() == []
    assert not consensus.cycle()
    assert consensus.is_safe()


def test_non_wait_free_solution1():
    edges = [('p1', 'q1', 'p1_test_and_set_0?', 'q3'), ('p2', 'q1', 'p2_test_and_set_0?', 'q3'), ('p1', 'q5', 'p2_read_1?', 'q6'), ('p2', 'q5', 'p1_read_1?', 'q6')]
    consensus = examples.consensus.consensus_from_fail_scenario()
    consensus.add_automata_edges_by_name(edges)
    for state in consensus.states():
        outgoing_process_automata = []
        for _, _, data_dict in consensus.out_edges(state, data=True):
            print data_dict
            message = data_dict['label']
            for p in consensus.process_automata:
                if message in p.input_alphabet or message in p.output_alphabet:
                    outgoing_process_automata.append(p)
        assert set(outgoing_process_automata) == set(consensus.process_automata)


def test_complete_with_fail_scenario():
    consensus = examples.consensus.consensus_from_fail_scenario()
    result = cegis.synthesize(consensus, verbose=1, wait_freedom=True, solver='gurobi')
    edges = result[0]
    assert len(edges) == 4
    assert (('p1', 'q1', 'p1_test_and_set_0?', 'q3') in edges or
            ('p1', 'q1', 'p1_test_and_set_0?', 'q7') in edges)
    assert (('p1', 'q5', 'p1_test_and_set_0?', 'q8') in edges or
            ('p1', 'q5', 'p1_test_and_set_0?', 'q9') in edges)
    consensus.add_automata_edges_by_name(edges)
    assert consensus.deadlock_states() == []
    assert not consensus.cycle()
    assert consensus.is_safe()
    assert consensus.cycle() == []
    p1 = consensus.automaton_by_name('p1')
    p1.draw_to_file(filename='/Users/stergiou/scenarios_app/consensus_completed_automaton_from_fail_scenario.pdf', pdf=True)


def test_complete_with_success_scenario_with_no_extra_states():
    consensus = examples.consensus.consensus_from_success_scenario()
    result = cegis.synthesize(consensus, verbose=1, wait_freedom=True)
    assert not result


def test_completion_for_consensus_from_success_scenario_with_extra_states():
    consensus = examples.consensus.consensus_from_success_scenario()
    p1 = consensus.automaton_by_name('p1')
    p2 = consensus.automaton_by_name('p2')
    new_state_p1 = p1.add_state()
    new_state_p2 = p2.add_state()
    completion = [('p1', 'q1', 'p1_test_and_set_1?', new_state_p1),
                  ('p1', 'q4', 'p1_test_and_set_1?', new_state_p1),
                  ('p1', new_state_p1, 'p2_read_1?', 'q5'),
                  ('p1', new_state_p1, 'p2_read_0?', 'q2'),
                  ('p2', 'q1', 'p2_test_and_set_1?', new_state_p2),
                  ('p2', 'q4', 'p2_test_and_set_1?', new_state_p2),
                  ('p2', new_state_p2, 'p1_read_1?', 'q5'),
                  ('p2', new_state_p2, 'p1_read_0?', 'q2')]
    consensus.add_automata_edges_by_name(completion)
    assert consensus.deadlock_states() == []
    assert not consensus.cycle()
    assert consensus.is_safe()
    assert consensus.is_locally_wait_free()


def test_complete_with_success_scenario_with_one_extra_state():
    consensus = examples.consensus.consensus_from_success_scenario()
    p1 = consensus.automaton_by_name('p1')
    p2 = consensus.automaton_by_name('p2')
    p1.add_state()
    p2.add_state()
    p1.draw_to_file()
    solutions = cegis.synthesize(consensus, verbose=1, solver='gurobi', wait_freedom=True)
    print solutions


def test_draw_all_solutions():
    solutions = [([('p1', 'q1', 'p1_test_and_set_1?', 'q4'), ('p2', 'q1', 'p2_test_and_set_1?', 'q4'), ('p1', 'q4', 'p1_test_and_set_1?', 'q6'), ('p2', 'q4', 'p2_test_and_set_1?', 'q6'), ('p1', 'q6', 'p2_read_0?', 'q2'), ('p2', 'q6', 'p1_read_0?', 'q2'), ('p1', 'q6', 'p2_read_1?', 'q5'), ('p2', 'q6', 'p1_read_1?', 'q5')], []), ([('p1', 'q1', 'p1_test_and_set_1?', 'q3'), ('p2', 'q1', 'p2_test_and_set_1?', 'q3'), ('p1', 'q4', 'p1_test_and_set_1?', 'q6'), ('p2', 'q4', 'p2_test_and_set_1?', 'q6'), ('p1', 'q6', 'p2_read_0?', 'q2'), ('p2', 'q6', 'p1_read_0?', 'q2'), ('p1', 'q6', 'p2_read_1?', 'q5'), ('p2', 'q6', 'p1_read_1?', 'q5')], []), ([('p1', 'q1', 'p1_test_and_set_1?', 'q6'), ('p2', 'q1', 'p2_test_and_set_1?', 'q6'), ('p1', 'q4', 'p1_test_and_set_1?', 'q6'), ('p2', 'q4', 'p2_test_and_set_1?', 'q6'), ('p1', 'q6', 'p2_read_0?', 'q2'), ('p2', 'q6', 'p1_read_0?', 'q2'), ('p1', 'q6', 'p2_read_1?', 'q5'), ('p2', 'q6', 'p1_read_1?', 'q5')], []), ([('p1', 'q1', 'p1_test_and_set_1?', 'q6'), ('p2', 'q1', 'p2_test_and_set_1?', 'q6'), ('p1', 'q4', 'p1_test_and_set_1?', 'q1'), ('p2', 'q4', 'p2_test_and_set_1?', 'q1'), ('p1', 'q6', 'p2_read_0?', 'q2'), ('p2', 'q6', 'p1_read_0?', 'q2'), ('p1', 'q6', 'p2_read_1?', 'q5'), ('p2', 'q6', 'p1_read_1?', 'q5')], [])]
    for solution in solutions:
        consensus = examples.consensus.consensus_from_success_scenario()
        edges = solution[0]
        consensus.add_automata_edges_by_name(edges)
        p1 = consensus.automaton_by_name('p1')
        p1.draw_to_file()


def test_complete_with_success_scenario_two_extra_states():
    consensus = examples.consensus.consensus_from_success_scenario()
    p1 = consensus.automaton_by_name('p1')
    p2 = consensus.automaton_by_name('p2')
    p1.add_state()
    p2.add_state()
    p1.add_state()
    p2.add_state()
    result = cegis.synthesize(consensus, verbose=1, solver='z3')
    assert result


def test_test_and_set():
    ts = examples.consensus.test_and_set('p1', 'p2')
    assert ts.initial_state == 'ts_unset'
