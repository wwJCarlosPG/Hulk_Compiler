from parser.grammar.Grammar import Grammar


# Grammar 
G = Grammar()
E = G.NonTerminal('E', startSymbol=True)
T = G.NonTerminal('T')
plus, times, integer, opar, cpar = G.Terminals('+ * int ( )')

E %= T + plus + E | T
T %= integer + times + T | integer | opar + E + cpar



def get_grammar():
    return G