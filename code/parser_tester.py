from grammar.anbn_grammar import get_grammar as get_anbn
from grammar.simple_expression import get_grammar as get_exp
from grammar.hulk_grammar import get_grammar as get_hulk
from parser.SLR1Parser import SLR1Parser
from cmp.tools.parsing import LR1Parser

selector = 3

match selector:
    case 1:
        G = get_anbn()
        print(G)
        tokenized_string = [G['a'], G['a'], G['a'], G['b'], G['b'], G['b'], G['$']]
    case 2:
        G = get_exp()
        print(G)
        tokenized_string = [G['int'], G['*'], G['('], G['int'], G['+'], G['int'], G[')'], G['$']]
    case 3:
        G = get_hulk()
        tokenized_string = [G['num'], G['*'], G['('], G['num'], G['+'], G['num'], G[')'], G['$']]
    case _:
        raise Exception("No match case")

# lr1_parser = LR1Parser(G)
slr1_parser = SLR1Parser(G, verbose=True)
output, operations = slr1_parser(tokenized_string)
print(f'\nDerivations sequence: {output}')
print(f'\nOperations sequence: {operations}')
