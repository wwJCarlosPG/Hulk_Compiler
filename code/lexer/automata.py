from cmp.utils import ContainerSet, DisjointSet

class NFA:
    def __init__(self, states, finals, transitions, start=0):
        """
        Initializes a Non-Deterministic Finite Automaton (NFA) with the given states, final states, transitions, and optional start state.

        Parameters:
        - states: Total number of states in the NFA.
        - finals: Set of final states in the NFA.
        - transitions: Dictionary representing the transitions of the NFA in the form {(origin, symbol): destinations}.
        - start: Initial state of the NFA (default is 0).
        """
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = { state: {} for state in range(states) }
        
        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')
        
    def epsilon_transitions(self, state):
        """
        Returns the epsilon transitions from a given state in the NFA.

        Parameters:
        - state: The state for which epsilon transitions are required.

        Returns:
        - Tuple of states reachable from the given state using epsilon transitions.
        """
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()
        
class DFA(NFA):
    
    def __init__(self, states, finals, transitions, start=0):
        """
        Initializes a Deterministic Finite Automaton (DFA) based on the provided states, final states, transitions, and optional start state.
        
        Parameters:
        - states: Total number of states in the DFA.
        - finals: Set of final states in the DFA.
        - transitions: Dictionary representing the transitions of the DFA in the form {(origin, symbol): destination}.
        - start: Initial state of the DFA (default is 0).
        """
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):
        try:
            self.current = self.transitions[self.current][symbol][0]
        except KeyError:
            self.current = None
    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):
        self._reset()
        for symbol in string:
            self._move(symbol)
        return self.current in self.finals
    

def move(automaton, states, symbol):
     """
        Moves the DFA to the next state based on the given input symbol.

        Parameters:
        - symbol: Input symbol to process the transition.
        """
     moves = set()
     for state in states:
        try:
            moves.update(automaton.map[(state,symbol)])
        except KeyError:
            pass
     return moves

def epsilon_closure(automaton, states):
    """
    Computes the epsilon closure of a set of states in the automaton.

    Parameters:
    - automaton: The automaton for which epsilon closure is to be computed.
    - states: Set of states for which epsilon closure is required.

    Returns:
    - ContainerSet representing the epsilon closure of the input states.
    """
    pending = [ s for s in states ]
    closure = { s for s in states }
    
    while pending:
        state = pending.pop()
        try:
            new_states = automaton.map[(state,'')]
            closure.update(new_states)
            closure.update(epsilon_closure(automaton,new_states).set)
        except KeyError:
            pass

    return ContainerSet(*closure)


def nfa_to_dfa(automaton):
    """
    Converts a Non-Deterministic Finite Automaton (NFA) to a Deterministic Finite Automaton (DFA).

    Parameters:
    - automaton: The NFA to be converted to a DFA.

    Returns:
    - DFA representing the converted automaton.
    """
    transitions = {}
    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]
    state_sets = [ start.set ]

    pending = [ start ]
    index = 0
    while pending:
        state = pending.pop()
        
        for symbol in automaton.vocabulary:
            next_state_set = epsilon_closure(automaton, move(automaton, list(state.set), symbol)).set

            if not next_state_set:    # comment out these lines to get a fully specified automata
                continue              
                        
            try:
                i = state_sets.index(next_state_set)
                next_state = states[i]
            except ValueError:                
                next_state = ContainerSet(*next_state_set)
                index += 1
                next_state.id = index
                next_state.is_final = any(s in automaton.finals for s in next_state)
                           
                states.append(next_state)
                state_sets.append(next_state_set)
                pending.append(next_state)          

            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                transitions[state.id,symbol] = next_state.id
    
    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa


def automata_minimization(automaton):
    partition = state_minimization(automaton)
    
    states = [s for s in partition.representatives]
    
    transitions = {}
    for i, state in enumerate(states):
        origin = state.value
        for symbol, destinations in automaton.transitions[origin].items():            
            new_destination = states.index(partition[destinations[0]].representative)

            try:
                transitions[i,symbol]
                assert False
            except KeyError:
                transitions[i,symbol] = new_destination
    
    start = states.index(partition[automaton.start].representative)
    finals = set([i for i in range(len(states)) if states[i].value in automaton.finals])
    
    return DFA(len(states), finals, transitions, start) 


def state_minimization(automaton):
    partition = DisjointSet(*range(automaton.states))
    
    finals = automaton.finals
    non_finals = [state for state in range(automaton.states) if state not in finals]
    partition.merge(finals)
    partition.merge(non_finals)
    
    while True:
        new_partition = DisjointSet(*range(automaton.states))
        
        for group in partition.groups:
            new_groups = distinguish_states(group,automaton,partition)
            for new_group in new_groups:                
                new_partition.merge(new_group)        

        if len(new_partition) == len(partition):
            break

        partition = new_partition
        
    return partition


def distinguish_states(group, automaton, partition):        
    split = {}
    vocabulary = tuple(automaton.vocabulary)
    
    transition = automaton.transitions

    for member in group:
        for item in split.keys():
            for symbol in vocabulary:
                q1 = None
                q2 = None
                try:
                    q1 = partition[transition[item][symbol][0]].representative
                except KeyError:
                    q1 = None
                try:
                    q2 = partition[transition[member.value][symbol][0]].representative
                except KeyError:
                    q2 = None
                if q1 != q2:
                    break
            else:
                split[item].append(member.value)
                break
        else:
            split[member.value] = [member.value]
                    

    return [ group for group in split.values()]