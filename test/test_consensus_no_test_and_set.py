import cegis
import examples.consensus_no_test_and_set


def test_complete_consensus_prefer0read0prefer1read1_with_wait_freedom():
    consensus = examples.consensus_no_test_and_set.consensus_prefer0read0prefer1read1()
    solution, _ = cegis.synthesize(consensus, wait_freedom=True, check_local_deadlocks=True)
    assert not solution


def test_complete_consensus_prefer0read0prefer1read1_without_wait_freedom():
    consensus = examples.consensus_no_test_and_set.consensus_prefer0read0prefer1read1()
    solution, _ = cegis.synthesize(consensus, fairness='process', wait_freedom=False, check_local_deadlocks=True)
    c = examples.consensus_no_test_and_set.consensus_prefer0read0prefer1read1()
    c.add_automata_edges_by_name(solution)
    assert not c.is_locally_wait_free()
