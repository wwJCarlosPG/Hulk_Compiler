try:
    import pydot
except:
    pass

class State:
    def __init__(self, state, final=False, formatter=lambda x: str(x), shape='circle'):
        """
        Initialize a state in the LR(0) automaton.

        Parameters:
        - state: The state identifier.
        - final: Whether the state is a final state or not.
        - formatter: A function for formatting the state representation.
        - shape: The shape of the state in the graphical representation.
        """
        self.state = state
        self.final = final
        self.transitions = {}
        self.epsilon_transitions = set()
        self.tag = None
        self.formatter = formatter
        self.shape = shape

    # The method name is set this way from compatibility issues.
    def set_formatter(self, value, attr='formatter', visited=None):
        """
        Set the formatter value for the state and its transitions recursively.

        Parameters:
        - value: The new formatter value.
        - attr: The attribute to be set.
        - visited: A set to keep track of visited states to avoid infinite recursion.

        Returns:
        - State: The updated state.
        """
        if visited is None:
            visited = set()
        elif self in visited:
            return

        visited.add(self)
        self.__setattr__(attr, value)
        for destinations in self.transitions.values():
            for node in destinations:
                node.set_formatter(value, attr, visited)
        for node in self.epsilon_transitions:
            node.set_formatter(value, attr, visited)
        return self

    def has_transition(self, symbol):
        """
        Check if the state has a transition for a given symbol.

        Parameters:
        - symbol: The symbol to check.

        Returns:
        - bool: True if the state has a transition for the symbol, False otherwise.
        """
        return symbol in self.transitions

    def add_transition(self, symbol, state):
        """
        Add a transition from the state to another state for the given symbol.

        Parameters:
        - symbol: The symbol triggering the transition.
        - state: The target state of the transition.

        Returns:
        - State: The updated state.
        """
        try:
            self.transitions[symbol].append(state)
        except:
            self.transitions[symbol] = [state]
        return self

    def add_epsilon_transition(self, state):
        """
        Add an epsilon transition from the state to another state.

        Parameters:
        - state: The target state of the epsilon transition.

        Returns:
        - State: The updated state.
        """
        self.epsilon_transitions.add(state)
        return self

    def recognize(self, string):
        """
        Check if the automaton recognizes the given string.

        Parameters:
        - string: The input string.

        Returns:
        - bool: True if the automaton recognizes the string, False otherwise.
        """
        states = self.epsilon_closure
        for symbol in string:
            states = self.move_by_state(symbol, *states)
            states = self.epsilon_closure_by_state(*states)
        return any(s.final for s in states)

    def to_deterministic(self, formatter=lambda x: str(x)):
        """
        Convert the LR(0) automaton to a deterministic form.

        Parameters:
        - formatter: A function for formatting the state representation.

        Returns:
        - State: The initial state of the deterministic automaton.
        """
        closure = self.epsilon_closure
        start = State(tuple(closure), any(s.final for s in closure), formatter)

        closures = [ closure ]
        states = [ start ]
        pending = [ start ]

        while pending:
            state = pending.pop()
            symbols = { symbol for s in state.state for symbol in s.transitions }

            for symbol in symbols:
                move = self.move_by_state(symbol, *state.state)
                closure = self.epsilon_closure_by_state(*move)

                if closure not in closures:
                    new_state = State(tuple(closure), any(s.final for s in closure), formatter)
                    closures.append(closure)
                    states.append(new_state)
                    pending.append(new_state)
                else:
                    index = closures.index(closure)
                    new_state = states[index]

                state.add_transition(symbol, new_state)

        return start

    @staticmethod
    def from_nfa(nfa, get_states=False):
        """
        Convert a non-deterministic finite automaton (NFA) to LR(0) states.

        Parameters:
        - nfa: The non-deterministic finite automaton.
        - get_states: Whether to return a list of all states or just the start state.

        Returns:
        - State or (State, list): The start state of the LR(0) automaton, or both the start state and a list of all states.
        """
        states = []
        for n in range(nfa.states):
            state = State(n, n in nfa.finals)
            states.append(state)

        for (origin, symbol), destinations in nfa.map.items():
            origin = states[origin]
            origin[symbol] = [ states[d] for d in destinations ]

        if get_states:
            return states[nfa.start], states
        return states[nfa.start]

    @staticmethod
    def move_by_state(symbol, *states):
        """
        Get the set of states obtained by moving by a symbol from the given set of states.

        Parameters:
        - symbol: The symbol for the move.
        - states: The set of states to move from.

        Returns:
        - set: The set of states after the move.
        """
        return { s for state in states if state.has_transition(symbol) for s in state[symbol]}

    @staticmethod
    def epsilon_closure_by_state(*states):
        """
        Get the epsilon closure of the given set of states.

        Parameters:
        - states: The set of states.

        Returns:
        - set: The epsilon closure of the set of states.
        """
        closure = { state for state in states }

        l = 0
        while l != len(closure):
            l = len(closure)
            tmp = [s for s in closure]
            for s in tmp:
                for epsilon_state in s.epsilon_transitions:
                        closure.add(epsilon_state)
        return closure

    @property
    def epsilon_closure(self):
        """
        Get the epsilon closure of the state.

        Returns:
        - set: The epsilon closure of the state.
        """
        return self.epsilon_closure_by_state(self)

    @property
    def name(self):
        """
        Get the name of the state.

        Returns:
        - str: The name of the state.
        """
        return self.formatter(self.state)

    def get(self, symbol):
        """
        Get the target state of a transition for a given symbol.

        Parameters:
        - symbol: The symbol triggering the transition.

        Returns:
        - State: The target state of the transition.
        """
        target = self.transitions[symbol]
        assert len(target) == 1
        return target[0]

    def __getitem__(self, symbol):
        if symbol == '':
            return self.epsilon_transitions
        try:
            return self.transitions[symbol]
        except KeyError:
            return None

    def __setitem__(self, symbol, value):
        if symbol == '':
            self.epsilon_transitions = value
        else:
            self.transitions[symbol] = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.state)

    def __hash__(self):
        return hash(self.state)

    def __iter__(self):
        yield from self._visit()

    def _visit(self, visited=None):
        if visited is None:
            visited = set()
        elif self in visited:
            return

        visited.add(self)
        yield self

        for destinations in self.transitions.values():
            for node in destinations:
                yield from node._visit(visited)
        for node in self.epsilon_transitions:
            yield from node._visit(visited)

    def graph(self):
        """
        Generate a Pydot graph representation of the LR(0) automaton.

        Returns:
        - pydot.Dot: The Pydot graph representation of the automaton.
        """
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        visited = set()
        def visit(start):
            ids = id(start)
            if ids not in visited:
                visited.add(ids)
                G.add_node(pydot.Node(ids, label=start.name, shape=self.shape, style='bold' if start.final else ''))
                for tran, destinations in start.transitions.items():
                    for end in destinations:
                        visit(end)
                        G.add_edge(pydot.Edge(ids, id(end), label=tran, labeldistance=2))
                for end in start.epsilon_transitions:
                    visit(end)
                    G.add_edge(pydot.Edge(ids, id(end), label='ε', labeldistance=2))

        visit(self)
        G.add_edge(pydot.Edge('start', id(self), label='', style='dashed'))

        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass

    def write_to(self, fname):
        """
        Write the SVG representation of the automaton to a file.

        Parameters:
        - fname: The filename for the output SVG file.

        Returns:
        - bool: True if writing is successful, False otherwise.
        """
        return self.graph().write_svg(fname)

def multiline_formatter(state):
    """
    Formatter function for multiline representation of LR(0) state.

    Parameters:
    - state: The LR(0) state.

    Returns:
    - str: The formatted multiline representation of the state.
    """
    return '\n'.join(str(item) for item in state)

def lr0_formatter(state):
    """
    Formatter function for LR(0) state.

    Parameters:
    - state: The LR(0) state.

    Returns:
    - str: The formatted representation of the state.
    """
    try:
        return '\n'.join(str(item)[:-4] for item in state)
    except TypeError:
        return str(state)[:-4]