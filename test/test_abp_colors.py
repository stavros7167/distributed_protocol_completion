import examples.abp_colors


def test_correct_is_correct():
    system = examples.abp_colors.system_correct()
    assert len(system.deadlock_states()) == 0
    assert system.is_safe()


def test_correct_solution_four_scenarios():
    system = examples.abp_colors.system_with_four_scenarios()
    assert ('q20', 'timeout?', 'q18') in system.automaton_by_name('sender').candidate_edges()
    system.add_automata_edges_by_name(examples.abp_colors.SYSTEM_WITH_FOUR_SCENARIOS_CORRECT_EDGES)
    assert system.is_safe()
    assert len(system.deadlock_states()) == 0
    cycles = system.strong_fair_cycles()
    assert len(cycles) == 0
