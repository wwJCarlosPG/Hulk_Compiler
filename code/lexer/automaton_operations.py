from lexer.automata import NFA
from copy import copy

def automata_union(a1, a2):
    """
    Perform the union of two non-deterministic finite automata (NFA).

    Parameters:
    - a1: First automaton to be united.
    - a2: Second automaton to be united.

    Returns:
    - NFA representing the union of the two input automata.
    """
    transitions = {}
    start = 0
    d1 = 1
    finals_a1 = {f+d1 for f in a1.finals}
    finals_a2 = {f+a1.states+d1 for f in a2.finals}
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[d1 + origin, symbol] = [d1 + d for d in destinations]

    for (origin, symbol), destinations in a2.map.items():        
        transitions[d2 + origin, symbol] = [d2 + d for d in destinations]
    
    transitions[start, ''] = [d1,d2]
    for f1 in finals_a1:
        transitions[f1, ''] = [final]
    for f2 in finals_a2:
        transitions[f2, ''] = [final]
            
    states = a1.states + a2.states + 2
    finals = { final }  
    
    return NFA(states, finals, transitions, start)

def automata_concatenation(a1, a2):
    """
    Concatenate two non-deterministic finite automata (NFA).

    Parameters:
    - a1: First automaton to be concatenated.
    - a2: Second automaton to be concatenated.

    Returns:
    - NFA representing the concatenation of the two input automata.
    """
    transitions = {}
    finals_a1 = {f for f in a1.finals}
    finals_a2 = {f+a1.states for f in a2.finals}
    finals = finals_a2
    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[origin, symbol] = destinations

    for (origin, symbol), destinations in a2.map.items():
        transitions[d2 + origin, symbol] = [d2 + d for d in destinations]
    for f1 in finals_a1:
        transitions[f1, ''] = [d2]
    for f2 in finals_a2:
        try:
            transitions[f2, ''] = transitions[f2,'']+[final]
        except: 
             transitions[f2,''] = [final] 

    states = a1.states + a2.states + 1
    finals = { final }
    return NFA(states, finals, transitions, start)

def automata_closure(a1):
    """
    Compute the Kleene closure of a non-deterministic finite automaton (NFA).

    Parameters:
    - a1: Automaton to apply the Kleene closure to.

    Returns:
    - NFA representing the Kleene closure of the input automaton.
    """
    transitions = {}
    start = 0
    d1 = 1
    finals = {f+d1 for f in a1.finals}
    final = a1.states + d1
    

    for (origin, symbol), destinations in a1.map.items():
        transitions[d1 + origin, symbol] = [d1 + d for d in destinations]              
    for f in finals:
        transitions[f, ''] = [final]
    transitions[start, ''] = [d1]

    transitions[final,''] = [start]  
            
    states = a1.states +  2
    finals = {start,final}
    return NFA(states, finals, transitions, start)

def automata_complement(a1):
    """
    Compute the complement of a non-deterministic finite automaton (NFA).

    Parameters:
    - a1: Automaton to apply the complement to.

    Returns:
    - NFA representing the complement of the input automaton.
    """
    complement = copy(a1)

    complement.finals = [i for i in range(a1.states) if i not in a1.finals]   

    return complement

def automata_plus(a1):
    """
    Constructs an NFA that recognizes the language represented by the given automaton,
    and includes the Kleene Plus operation.

    Args:
        a1: The original automaton that recognizes a language.

    Returns:
        NFA: An NFA that recognizes the language of one or more occurrences of the language recognized by a1.
    """
    transitions = {}
    start = 0
    final = a1.states
    for (origin, symbol), destinations in a1.map.items():
         transitions[origin, symbol] = [d for d in destinations]
    transitions[final - 1, ''] = [final]
    states = a1.states + 1
    finals = {final}
    return NFA(states, finals, transitions, start)



