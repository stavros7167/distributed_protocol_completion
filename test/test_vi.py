import os.path
import networkx

import cegis
import examples.vi
import examples.common
import product
import util


def test_equivalent_automata():
    vi = examples.vi.vi()
    assert len(vi.equivalent_automata) == 2


def test_correct_completion():
    vi = examples.vi.vi()
    (cache1_index, cache1), (directory_index, directory), (cache2_index, cache2) = [vi.automaton_index_by_name(name)
                                                                                    for name in ["cache1", "directory", "cache2"]]
    edges = examples.vi.CORRECT_EDGES
    vi.add_automata_edges_by_name(edges)
    assert list(vi.strong_fair_cycles()) == []


def test_unsafe_completion():
    edges = [('directory', 'q1', "wb_c1_dir'?", 'q2'),
             ('directory', 'q4', "wb_c2_dir'?", 'q0'),
             ('directory', 'invalid_dir', "wb_c1_dir'?", 'q0'),
             ('directory', 'invalid_dir', "wb_c2_dir'?", 'q9'),
             ('directory', 'q11', "wb_c1_dir'?", 'q7'),
             ('cache1', 'q5', 'wb_client_c1?', 'q7'),
             ('cache2', 'q5', 'wb_client_c2?', 'q7'),
             ('cache1', 'q5', "rsp_dir_c1'?", 'q4'),
             ('cache2', 'q5', "rsp_dir_c2'?", 'q4'),
             ('cache1', 'valid_c1', 'req_client_c1?', 'q5'),
             ('cache2', 'valid_c2', 'req_client_c2?', 'q5'),
             ('cache1', 'invalid_c1', 'wb_client_c1?', 'q4'),
             ('cache2', 'invalid_c2', 'wb_client_c2?', 'q4')]
    vi = examples.vi.vi()
    vi.add_automata_edges_by_name(edges)
    assert not vi.is_safe()
    bad_transitions = cegis.generalize_reachability(vi, edges, vi.is_safety_violating)
    vi = examples.vi.vi()
    vi.add_automata_edges_by_name(bad_transitions)
    assert not vi.is_safe()

