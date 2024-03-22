from automata_work import DFA
import os
import sys
current_route = os.path.dirname(os.path.abspath(__file__))
prev_route = os.path.join(current_route, "..", "parser")
sys.path.append(prev_route)
from code.utils.utils import DisjointSet
def distinguish_states(group, automaton, partition):
    """
    Distinguish states within a group based on transitions and a given partition.

    Parameters:
    - group: A group of states to distinguish within.
    - automaton: The automaton under consideration.
    - partition: The current partition of states.

    Returns:
    - A list of distinguished groups based on transitions and the partition.
    """
    split = {}
    vocabulary = tuple(automaton.vocabulary)

    for member in group:
        state = member.value
        destinations = []
        for char in vocabulary:            
            destinations.append(partition[automaton.transitions[state][char][0]].representative)
        destinations = tuple(destinations)
        
        try:
            split[destinations].append(state)    
        except KeyError:
            split[destinations] = [state]     

    return [ group for group in split.values()]
            
def state_minimization(automaton):
     """
    Perform state minimization on the given automaton.

    Parameters:
    - automaton: The automaton to minimize.

    Returns:
    - A DisjointSet representing the minimized states.
    """
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

def automata_minimization(automaton):
     """
    Minimize the given automaton by merging equivalent states.

    Parameters:
    - automaton: The automaton to minimize.

    Returns:
    - A deterministic finite automaton (DFA) representing the minimized automaton.
    """
     
     partition = state_minimization(automaton)
    
     states = [s.value for s in partition.representatives]
    
     transitions = {}
     for i, state in enumerate(states):
        origin = state

        for symbol, destinations in automaton.transitions[origin].items():
            destination = destinations[0]
            new_destination = partition[destination].representative.value
            new_destination = states.index(new_destination)
            
            try:
                transitions[i,symbol]
                assert False
            except KeyError:
                transitions[i,symbol] = new_destination

     finals = [states.index(state) for state in states if state in automaton.finals]
     for group in partition.groups:
        for member in group:
            if automaton.start == member.value:
                start = states.index(partition[member.value].representative.value)  
                break         
     return DFA(len(states), finals, transitions, start)