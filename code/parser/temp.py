from grammar.grammar import Grammar
from Parser_Generator import Parser_Generator

# Grammar a^{n}b^{n}
G = Grammar()
S = G.NonTerminal('S', True)
a, b = G.Terminals('a b')

S %= a + S + b | a + b

print(G)

parser_generator = Parser_Generator(G)
