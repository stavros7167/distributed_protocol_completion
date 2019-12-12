import cegis
import examples.abp
import product


def test_correct_completions():
    p = product.Product(examples.abp.system_common_automata +
                        [examples.abp.sender_correct(), examples.abp.receiver_correct()])
    assert p.is_safe()
    fair_cycles = p.strong_fair_cycles_iter()
    assert len(list(fair_cycles)) == 0


def test_synthesize_with_one_scenario():
    system = examples.abp.system_with_one_scenario()
    result = cegis.synthesize_all(examples.abp.system_with_one_scenario(), verbose=0)
    assert result.next()[0] is not None


def test_wrong_completion():
    edges = [('sender', 'q2', 'timeout?', 'q1'),
             ('sender', 'q5', 'timeout?', 'q4')]
    system = examples.abp.system_with_one_scenario()
    system.add_automata_edges_by_name(edges)
    assert system.is_safe()
    assert system.strong_fair_cycles() != []


def test_completion_liveness_send_follows_deliver_is_missing():
    edges = [('sender', 'q2', 'timeout?', 'q1'),
             ('sender', 'q5', 'timeout?', 'q4')]
    system = examples.abp.system_with_one_scenario()
    system.add_automata_edges_by_name(edges)
    assert system.is_safe()
    assert system.strong_fair_cycles() != []


