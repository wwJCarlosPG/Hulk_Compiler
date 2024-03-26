from lexer.ast_regex_node import *
from cmp.pycompiler import Grammar

G = Grammar()

E = G.NonTerminal('E', True)
T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')


E %= E + pipe + T, lambda _,s:UnionNode(s[1],s[3])
E %= T, lambda _,s: s[1]
T %= T + F, lambda _,s: ConcatNode(s[1], s[2])
T %= F, lambda _,s: s[1]
F %= F + star,lambda _,s:ClosureNode(s[1])
F %= A, lambda _,s:s[1]
A %= opar + E + cpar, lambda _, s: s[2]
A %= symbol,lambda _,s: SymbolNode(s[1])
A %= epsilon, lambda _,s: EpsilonNode(s[1])