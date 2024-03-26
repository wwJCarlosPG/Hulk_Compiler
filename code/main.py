from token_table import table
from lexer.lexer import Lexer
from parser.SLR1Parser import SLR1Parser
from grammar.hulk_grammar import get_grammar
from cmp.evaluation import evaluate_reverse_parse

G = get_grammar()

program = '''
while(x<=4){
    print(x); 
    x:=6;}
'''

print(f'Program:\n\n {program}')

print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Lexer results xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
lexer = Lexer(table, G.EOF)
tokenss = lexer(program)
# print(tokenss)
tokens = [token.token_type for token in tokenss]
print('✅ OK')

print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Parser results xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
slr1 = SLR1Parser(G)
out, oper = slr1(tokens)
# print(out)
# print(oper)
ast = evaluate_reverse_parse(out,oper,tokenss)
print('✅ OK')


