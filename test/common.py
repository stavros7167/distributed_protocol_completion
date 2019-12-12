import automaton

def automaton1():
    a = automaton.Automaton()
    a.add_string('label1L a? b! label2L')
    return a


def process_example():
    process = automaton.Automaton()
    process.add_edge('p0', 'p1', label='a!')
    return process


def environment_example():
    environment = automaton.Automaton()
    environment.add_edge('e0', 'e1', label='a?')
    environment.add_edge('e1', 'e0', label='b!')
    return environment
