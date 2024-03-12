from grammar.anbn_grammar import get_grammar as get_anbn
from SLR1Parser import SLR1Parser


G = get_anbn()
print(G)


slr1_parser = SLR1Parser(G, verbose=True)
string = 'aaabbb$'
tokenized_string = [G[x] for x in string]
# tokenized_string = [G['a'], G['a'], G['a'], G['b'], G['b'], G['b'], G['$']]
print(f'\nString to parse: {string}\n')

output = slr1_parser(tokenized_string)

print(f'\nDerivations sequence: {output}')