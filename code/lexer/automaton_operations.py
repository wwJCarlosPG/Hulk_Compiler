from automata_work import NFA
from copy import copy
from automata_work import DFA, nfa_to_dfa

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
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[d1 + origin, symbol] = [d1 + d for d in destinations]

    for (origin, symbol), destinations in a2.map.items():        
        transitions[d2 + origin, symbol] = [d2 + d for d in destinations]
    
    transitions[start, ''] = [d1,d2]
    
    transitions[d2 - 1, ''] = [final]
    transitions[final - 1, ''] = [final]
            
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
    
    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[origin, symbol] = destinations

    for (origin, symbol), destinations in a2.map.items():
        transitions[d2 + origin, symbol] = [d2 + d for d in destinations]
    
    transitions[d2 - 1, ''] = [d2]
    transitions[final - 1, ''] = [final]
            
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
    final = a1.states + d1
    

    for (origin, symbol), destinations in a1.map.items():
        transitions[d1 + origin, symbol] = [d1 + d for d in destinations]              
    
    transitions[start, ''] = [d1]
    
    transitions[final - 1, ''] = [final]
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



# automaton = DFA(states=3, finals=[2], transitions={
#     (0,'b'): 0,
#     (0,'a'): 1,
#     (1,'b'): 2,
#     (1,'a'): 0,
#     (2,'a'): 2,
#     (2,'b'): 2
# })

# automaton = DFA(states=2, finals=[1], transitions={
#     (0,'a'):  0,
#     (0,'b'):  1,
#     (1,'a'):  0,
#     (1,'b'):  1,
# })
# plus = automata_plus(automaton)
# recognize = nfa_to_dfa(plus).recognize
# # con = automata_concatenation(automaton, automaton)
# # recognize = nfa_to_dfa(con).recognize
# print(recognize('abba'))
# print(recognize('abab'))
# print(recognize('ababab'))
automaton = DFA(states=2, finals=[1], transitions={
    (0,'a'):  0,
    (0,'b'):  0,
    (0,'c'):  0,
    (0,'1'):  1,
    (0,'2'):  1,
    (0,'3'):  1,
    (0,'4'):  1,
    (0,'5'):  1,
    (1,'1'):  1,
    (1,'2'):  1,
    (1,'3'):  1,
    (1,'4'):  1,
    (1,'5'):  1
    
})
automata_plusplus = automata_plus(automaton)
recognize = nfa_to_dfa(automata_plusplus).recognize
print(recognize('a2'))
print(recognize('aa'))
print(recognize("abca12"))