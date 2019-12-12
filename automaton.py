"""
TODO Rename state_neighbors to labels
TODO make labels be the keys in the transitions
TODO make monitors actually be input complete
TODO replace dfs to state and bfs to state with networkx algorithms
"""

import StringIO
import copy

import networkx as nx
import util


class Automaton(nx.MultiDiGraph):
    def __init__(self, **kwargs):
        super(Automaton, self).__init__()
        self.initial_state = None
        self.is_product = False
        self.is_monitor = False
        self.is_liveness = False
        self.is_safety = False
        self.is_channel = False
        self.is_environment = True
        self.state_neighbors = dict()
        if 'input_alphabet' not in kwargs.keys():
            self.input_alphabet = []
        if 'output_alphabet' not in kwargs.keys():
            self.output_alphabet = []
        if 'initial_state' in kwargs:
            initial_state = kwargs['initial_state']
            self.add_node(initial_state)
            self.state_neighbors[initial_state] = dict()
        if 'edges' in kwargs:
            for source, label, target in kwargs['edges']:
                self.add_edge(source, target, label=label)
            del kwargs['edges']
        for k, v in kwargs.items():
            setattr(self, k, v)
        # Messages that have to be read from every state of the automaton.
        self.input_enabled = []
        self._input_states = set()
        self._output_states = set()

    @staticmethod
    def _parse_string(string):
        last_index = 0
        messages_and_labels = []
        for i, char in enumerate(string, 1):
            if char == '?' or char == '!' or char == 'L':
                messages_and_labels.append(string[last_index:i])
                last_index = i
        return [m.strip() for m in messages_and_labels]

    def add_state(self, name=None):
        new_state = 'q%d' % len(self) if name is None else name
        if new_state not in self.states():
            self.add_node(new_state)
        return new_state

    def candidate_edges(self):
        return list(self.candidate_edges_iter())

    def candidate_edges_iter(self):
        for state in self.nodes_iter():
            for candidate in self.candidate_edges_from_state_iter(state):
                yield candidate

    def candidate_edges_from_state(self, state):
        return list(self.candidate_edges_from_state_iter(state))

    def candidate_edges_from_state_iter(self, state):
        if 'final' in self.node[state]:
            return
        if self.is_output_state(state) and len(self.outgoing_labels(state)) > 0:
            return

        candidate_messages = []
        if not self.is_input_state(state):
            candidate_messages += list(self.output_alphabet)
        if not self.is_output_state(state):
            candidate_messages += list(self.input_alphabet)

        for label in self.outgoing_labels_iter(state):
            if label[:-1] in candidate_messages:
                candidate_messages.remove(label[:-1])
        for state2 in self.nodes_iter():
            for message in candidate_messages:
                yield (state,
                       message +
                       ("?" if message in self.input_alphabet else "!"),
                       state2)

    def draw_to_file(self, filename=util.TEMP_FILE_PATH, append=True, pdf=False):
        output = open(filename, 'a' if append else 'w')
        if not pdf:
            output.write("<h1>%s</h1>" % self.name)
            output.write(self.to_file())
        else:
            result = self.to_file(pdf=True)
            output.write(result)

    def make_accepting(self, state):
        self.node[state]['accepting'] = True

    def is_accepting(self, state):
        return 'accepting' in self.node[state]

    def outgoing_labels(self, state):
        return list(self.outgoing_labels_iter(state))

    def outgoing_labels_iter(self, state):
        for successor in self.successors(state):
            for d in self.get_edge_data(state, successor).values():
                yield d['label']

    def is_output_state(self, state):
        """Returns true if there is an output edge leaving the state, or if the
           state is listed in the automaton "_output_states"
        """
        return (state in self._output_states or
                any(label[-1] == '!' for label in self.outgoing_labels(state)))

    def is_input_state(self, state):
        """Returns true if there is an input edge leaving the state, or if the
           state is listed in the automaton "_input_states"
        """
        return (state in self._input_states or
                any(label[-1] == '?' for label in self.outgoing_labels(state)))

    def set_input_state(self, state):
        if self.is_output_state(state):
            raise ValueError('State {} is an output state, cannot be declared '
                             'input'.format(state))
        self._input_states.add(state)

    def set_output_state(self, state):
        if self.is_input_state(state):
            raise ValueError('State {} is an input state, cannot be declared '
                             'output'.format(state))
        self._output_states.add(state)

    def to_file(self, draw_empty_nodes=True, pdf=False):
        G = self.copy()
        G.add_node('initial_node_state', attr_dict={'shape': 'none'})
        if not draw_empty_nodes:
            for node in G:
                if G.predecesors(node) == [] and G.successors(node) == []:
                    G.remove_node(node)
        G.node['initial_node_state']['label'] = ""
        A = nx.drawing.nx_agraph.to_agraph(G)

        subgraph = A.add_subgraph()
        subgraph.add_node(G.initial_state)
        subgraph.add_node('initial_node_state')
        subgraph.graph_attr.update(rank='min')
        subgraph.add_edge('initial_node_state', G.initial_state)

        A.graph_attr['rankdir'] = 'LR'
        output = StringIO.StringIO()

        A.layout(prog='dot')
        if not pdf:
            A.draw(output, format='svg')
        else:
            A.draw(output, format='pdf')
        result = ''.join(output.getvalue())
        output.close()
        return result

    def deadlock_states(self):
        return list(self.deadlock_states_iter())

    def deadlock_states_iter(self):
        for state in self.nodes_iter():
            if self.outgoing_labels(state) == []:
                yield state

    def add_edge(self, state1, state2, **kwargs):
        """ Intercept the calls to add_edge that have a label keyword argument. """
        if not self.initial_state:
            self.initial_state = state1
            self.add_node(state1)
            self.node[state1]['initial'] = True
        if state2 not in self.state_neighbors:
            self.state_neighbors[state2] = dict()
        if 'label' in kwargs:
            label = kwargs['label']
            if state1 in self.state_neighbors:
                if label in self.state_neighbors[state1]:
                    if state2 in self.state_neighbors[state1][label]:
                        return
                else:
                    self.state_neighbors[state1][label] = []
            else:
                self.state_neighbors[state1] = dict()
                self.state_neighbors[state1][label] = []
            self.state_neighbors[state1][label].append(state2)
            # Cannot assert the following, product automata have edges with no read/write labels
            # assert label[-1] == '?' or label[-1] == '!'
            if label[-1] == '?' and label[:-1] not in self.input_alphabet:
                self.input_alphabet.append(label[:-1])
            elif label[-1] == '!' and label[:-1] not in self.output_alphabet:
                self.output_alphabet.append(label[:-1])
        if 'monitor_label' in kwargs:
            monitor_label = kwargs['monitor_label']
            # Since monitors only read, monitor-labels should only write
            assert monitor_label[-1] == '!'
            self.output_alphabet.append(monitor_label[:-1])
        return super(Automaton, self).add_edge(state1, state2, **kwargs)

    def remove_edge_with_label(self, state1, state2, label):
        edge_data = self.get_edge_data(state1, state2)
        labels = [d['label'] for d in edge_data.values()]
        if label not in labels:
            return
        self.state_neighbors[state1][label].remove(state2)
        if len(self.state_neighbors[state1][label]) == 0:
            self.state_neighbors[state1].pop(label)

        for i in range(len(labels)):
            self.remove_edge(state1, state2)
        labels.remove(label)
        for label in labels:
            super(Automaton, self).add_edge(state1, state2, label=label)

    def states(self):
        return list(self.nodes_iter())

    def bfs_to_state(self, state_predicate, initial_state=None, return_path=False):
        """ Returns a pair (state, predecessors) where state is the state
            that satisfies the predicate and predecessors is a dictionary of links to parents for each state visited
            and (None, predecessors) if no state is found.
        """
        initial_state = self.initial_state if not initial_state else initial_state
        queue = [initial_state] if initial_state else [self.initial_state]
        node_predecessors = dict()
        visited = set([])
        while True:
            s = queue.pop(0)
            visited.add(s)
            if state_predicate(s):
                if not return_path:
                    return (s, node_predecessors)
                else:
                    state = s
                    path = [s]
                    while state != initial_state:
                        state = node_predecessors[state][0]
                        path.append(state)
                    return list(reversed(path))
            for st in self.successors(s):
                label = None
                for d in self.get_edge_data(s, st).values():
                    label = d['label']
                if st not in visited:
                    queue.append(st)
                    node_predecessors[st] = (s, label)
                    visited.add(st)
            if queue == []:
                break
        return (None, node_predecessors)

    def __repr__(self):
        if hasattr(self, "name"):
            return self.name
        else:
            super(Automaton, self).__repr__()


def get_monitors(automata):
    monitors_indices_pairs = [(i, a) for i, a in enumerate(automata)
                              if a.is_monitor]
    if len(monitors_indices_pairs) == 0:
        return ([], [])
    else:
        return zip(*monitors_indices_pairs)
