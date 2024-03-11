from Item import Item
from utils import compute_firsts, compute_follows, build_LR0_automaton
from grammar import Grammar

# Grammar a^{n}b^{n}
G = Grammar()
S = G.NonTerminal('S', True)
a, b = G.Terminals('a b')

S %= a + S + b | a + b

print(G)

firsts = compute_firsts(G)
compute_follows(G, firsts)

# Extend Grammar with S'-> E
GG = G.AugmentedGrammar()

# Build NFA LR(0) automaton
NFA = build_LR0_automaton(GG)

# Write automaton
dot_graph = NFA.graph().write("nfa.dot", format='raw', encoding='utf-8')

# Convert to FDA LR(0) automaton
DFA = NFA.to_deterministic()

# Write automaton
dot_graph = DFA.graph().write("dfa.dot", format='raw', encoding='utf-8')