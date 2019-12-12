import cegis
import examples.vi_data


def test_deadlocks():
    p = examples.vi_data.vi()
    for d in p.deadlock_states():
        assert cegis.edges_that_solve_deadlock(p, d) != []


def test_correct_completion():
    edges = [('directory', 'q20', "wb_c1_dir_d1'?", 'q26'),
             ('directory', 'q20', "wb_c1_dir_d0'?", 'q16'),
             ('directory', 'q7', "wb_c2_dir_d0'?", 'q8'),
             ('directory', 'q7', "wb_c2_dir_d1'?", 'q14'),
             ('cache1', 'wbackc1', "inv_dir_c1'?", 'q8'),
             ('cache2', 'wbackc2', "inv_dir_c2'?", 'q8')]
    vi = examples.vi_data.vi()
    vi.add_automata_edges_by_name(edges)
    violates_bad_predicates = any(examples.vi_data.is_bad_state_coherence(vi, s) for s in vi.states())
    assert not violates_bad_predicates
    assert vi.is_safe()
    cycles = vi.strong_fair_cycles()
    assert cycles == []


def test_input_output_states():
    """
    In VI all process automata states are either input or output states.
    """
    vi = examples.vi_data.vi()
    cache1 = vi.automaton_by_name('cache1')
    directory = vi.automaton_by_name('directory')
    for a in [cache1, directory]:
        for state in a.states():
            assert (a.is_output_state(state) or a.is_input_state(state))
