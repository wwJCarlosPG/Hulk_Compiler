from lexer.ast_node import *
from cmp.pycompiler import Grammar

G = Grammar()

E = G.NonTerminal('E', True)
T, F, A, X, Y, Z, S = G.NonTerminals('T F A X Y Z, S')
pipe, star, plus, minus, quest, obrack, cbrack, opar, cpar, symbol, epsilon = G.Terminals('| * + - ? [ ] ( ) symbol ε')


E %= E + pipe + T, lambda _,s:UnionNode(s[1],s[3])
E %= T, lambda _,s: s[1]
T %= T + F, lambda _,s: ConcatNode(s[1], s[2])
T %= F, lambda _,s: s[1]
F %= F + star,lambda _,s:ClosureNode(s[1])
F %= F + plus,lambda _,s:PositiveClosureNode(s[1])
F %= F + quest,lambda _,s:ZeroOrOneNode(s[1])
F %= A, lambda _,s:s[1]
A %= opar + E + cpar, lambda _, s: s[2]
A %= symbol,lambda _,s: SymbolNode(s[1])
A %= epsilon, lambda _,s: EpsilonNode(s[1])
A %= obrack + S + cbrack, lambda h,s: SymbolSetNode(s[2])
S %= symbol, lambda h,s: [SymbolNode(s[1])]
S %= symbol + S, lambda h,s: [SymbolNode(s[1])] + s[2]
S %= symbol + minus + symbol, lambda h,s: RangeNode(SymbolNode(s[1]),SymbolNode(s[3])).evaluate()
S %= symbol + minus + symbol + S, lambda h,s: RangeNode(SymbolNode(s[1]),SymbolNode(s[3])).evaluate() + s[4]
