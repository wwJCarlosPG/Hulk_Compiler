import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
sys.path.append('code/lexer')
sys.path.append('code/parser/grammar')
sys.path.append('code/parser')
from ast_regex_node import *
from cmp.pycompiler import Grammar
G = Grammar()

E = G.NonTerminal('E', True)
T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
pipe, star, plus, opar, cpar, symbol, epsilon = G.Terminals('| * + ( ) symbol ε')

E %= T + X, lambda h,s: s[2], None, lambda h,s: s[1]

X %= pipe + T + X, lambda h,s: s[3], None, None, lambda h,s: UnionNode(h[0],s[2])                            
X %= G.Epsilon, lambda h,s: h[0]

T %= F + Y, lambda h,s: s[2], None, lambda h,s: s[1]  

Y %= F + Y, lambda h,s: s[2], None, lambda h,s: ConcatNode(h[0],s[1])                            
Y %= G.Epsilon, lambda h,s: h[0] 

F %= A + Z, lambda h,s: s[2], None, lambda h,s: s[1]

Z %= star, lambda h,s: ClosureNode(h[0]), None
Z %= plus, lambda h,s: PlusNode(h[0]), None
Z %= G.Epsilon, lambda h,s: h[0]

A %= symbol, lambda h,s: SymbolNode(s[1]), None  
A %= epsilon, lambda h,s: EpsilonNode(s[1]), None                                                  
A %= opar + E + cpar, lambda h,s: s[2], None, None, None 



