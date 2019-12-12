import itertools

import automaton


def minimize(a, distinguish_by='is_accepting'):
    """ Returns new automaton that is a minimized version of the current one.
    """
    distinguish_by = getattr(automaton.Automaton, distinguish_by)
    distinguished = set()
    non_distinguished = set()
    for s1, s2 in itertools.combinations(a.states(), 2):
        if distinguish_by(a, s1) != distinguish_by(a, s2):
            distinguished.add((s1, s2))
        else:
            non_distinguished.add((s1, s2))
    while True:
        distinguished_found = False
        non_distinguished_list = list(non_distinguished)
        for s1, s2 in non_distinguished_list:
            if set(a.outgoing_labels(s1)) != set(a.outgoing_labels(s2)):
                distinguished_found = True
                distinguished.add((s1, s2))
                non_distinguished.remove((s1, s2))
                break
            for m in a.outgoing_labels(s1):
                s1p = a.state_neighbors[s1][m][0]
                s2p = a.state_neighbors[s2][m][0]
                if (s1p, s2p) in distinguished or (s2p, s1p) in distinguished:
                    distinguished_found = True
                    distinguished.add((s1, s2))
                    non_distinguished.remove((s1, s2))
                    break
        if not distinguished_found:
            break
    block_dict = dict()
    # iterate through the state
    # if a state is distinguishable from all other states, added it in its own block
    # if it is not distinguishable from state A and A has been assingned a block then add it to that blok
    for state in a.states():
        non_distinguished_from = [s for pair in non_distinguished if state in pair for s in pair if s != state]
        found_block = False
        if len(non_distinguished_from) == 0:
            block_dict[state] = [state]
            continue
        for state2 in non_distinguished_from:
            if state2 in block_dict:
                block_dict[state2].append(state)
                block_dict[state] = block_dict[state2]
                found_block = True
                break
        if not found_block:
            block_dict[state] = [state]
    b = automaton.Automaton()
    for s in set([tuple(block) for block in block_dict.values()]):
        new_state = ','.join(s)
        state = s[0]
        for m in a.outgoing_labels(state):
            successor = a.state_neighbors[state][m][0]
            b.add_edge(new_state, ','.join(block_dict[successor]), label=m)
    return b


def test_minimization_dragon_book():
    a = automaton.Automaton()
    for start, label, end in [
            ('A', '0', 'B'),
            ('A', '1', 'F'),
            ('B', '0', 'G'),
            ('B', '1', 'C'),
            ('C', '0', 'A'),
            ('C', '1', 'C'),
            ('D', '0', 'C'),
            ('D', '1', 'G'),
            ('E', '0', 'H'),
            ('E', '1', 'F'),
            ('F', '0', 'C'),
            ('F', '1', 'G'),
            ('G', '0', 'G'),
            ('G', '1', 'E'),
            ('H', '0', 'G'),
            ('H', '1', 'C')]:
        a.add_edge(start, end, label=label)
    a.make_accepting('C')
    b = minimize(a)
    assert len(b.states()) == 5
