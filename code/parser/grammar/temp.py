from utils import compute_firsts, compute_follows
from grammar import Grammar

# Grammar example
G = Grammar()
E = G.NonTerminal('E', True)
T,F,X,Y = G.NonTerminals('T F X Y')
plus, minus, star, div, opar, cpar, num = G.Terminals('+ - * / ( ) num')

E %= T + X
X %= plus + T + X | minus + T + X | G.Epsilon
T %= F + Y
Y %= star + F + Y | div + F + Y | G.Epsilon
F %= num | opar + E + cpar

print(G)

firsts = compute_firsts(G)
compute_follows(G, firsts)