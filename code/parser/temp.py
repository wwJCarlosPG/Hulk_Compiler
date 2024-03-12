from grammar.anbn_grammar import get_grammar as get_anbn
from SLR1Parser import SLR1Parser


G = get_anbn()
print(G)


slr1_parser = SLR1Parser(G, verbose=True)
# Ahora se puede evaluar el parser en array de tokens de la gramatica y se obtiene como resultado la secuencia de producciones