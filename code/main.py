from token_table import table
from lexer.lexer import Lexer
from parser.SLR1Parser import SLR1Parser
from grammar.hulk_grammar import get_grammar
from cmp.evaluation import evaluate_reverse_parse

G = get_grammar()
lexer = Lexer(table, G.EOF)
print('OK')
# text = '''while(x<=4){
#       print(x); 
#       x:=6;}'''
# tokenss = lexer(text)
# slr1 = SLR1Parser(G,verbose=True)
# print(tokenss)
# print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
# tokens = [token.token_type for token in tokenss]
# out, oper = slr1(tokens)
# # print(out)
# # print(oper)
# print()
# print('OK')
# print()
# ast = evaluate_reverse_parse(out,oper,tokenss)
# print()
