from parser.grammar.Grammar import Grammar


# Grammar a^{n}b^{n}
G = Grammar()
S = G.NonTerminal('S', True)
a, b = G.Terminals('a b')

S %= a + S + b | a + b



def get_grammar():
    return G