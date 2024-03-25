from lexer.automata_work import DFA
from cmp.utils import DisjointSet
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