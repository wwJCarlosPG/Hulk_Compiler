from cmp.pycompiler import Grammar
from parser.ast_nodes import *


G = Grammar()
E = G.NonTerminal('E', True)
pipe, star, plus, opar, cpar, symbol, epsilon = G.Terminals('| * + ( ) symbol ε')

