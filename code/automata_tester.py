from lexer.automata_work import NFA, nfa_to_dfa, DFA, move
from lexer.automaton_operations import automata_union
from lexer.ast_regularexp_node import *

# automaton = NFA(states=3, finals=[2], transitions={
#     (0,'a'): [ 0 ],
#     (0,'b'): [ 0, 1 ],
#     (1,'a'): [ 2 ],
#     (1,'b'): [ 2 ],
# })

# print("Reconoce el lenguaje de las cadenas formadas por a's y b's tal que el penúltimo caracter es b.")


# move(automaton, [0, 1], 'a') == {0, 2}
# move(automaton, [0, 1], 'b') == {0, 1, 2}

# dfa = nfa_to_dfa(automaton)

# print(dfa.recognize('aba'))
# print(dfa.recognize('bb'))
# print(dfa.recognize('aaaaaaaaaaaba'))

# print(not dfa.recognize('aaa'))
# print(not dfa.recognize('ab'))
# print(not dfa.recognize('b'))
# print(not dfa.recognize(''))

a = SymbolNode('a').evaluate()
dfa = nfa_to_dfa(a)
print(dfa.recognize('aa'))
b = ClosureNode(SymbolNode('a')).evaluate()
dfa = nfa_to_dfa(b)
print(dfa.recognize('aaaa'))
union = UnionNode(SymbolNode('a'),SymbolNode('b')).evaluate()
dfa = nfa_to_dfa(union)
print(dfa.recognize('b'))
concat = ConcatNode(SymbolNode('a'),SymbolNode('b')).evaluate()
dfa = nfa_to_dfa(concat)
print(dfa.recognize('ab'))
