from token_table import table
from lexer.lexer import Lexer
from parser.SLR1Parser import SLR1Parser
from grammar.hulk_grammar import get_grammar
from cmp.evaluation import evaluate_reverse_parse
from semantic_check.TypeCollector import TypeCollector
from semantic_check.TypeBuilder import TypeBuilder

G = get_grammar()

program0 = '''
print("Hello, World")
'''
program1 = '''
while(x<=4){
    print(x); 
    x:="6";}
'''
program2 = '''
type Point(x, y) {
    x_prop = x;
    y_prop = y;
};
function AbsoluteMove(x, steps) => x + steps;
print("OK")
'''
program3 = '''
type Animal(name){
    name = name;
    sound() => "Make Sound";
};
type Dog(name) {
    name = name;
};
type Cat(name, skin) {
    name = name;
    skin = skin;
};
print("OK")
'''

selector = 3
match selector:
    case 0:
        program = program0
    case 1:
        program = program1
    case 2:
        program = program2
    case 3:
        program = program3
    case _:
        raise Exception("Selector error: selector out of range")



print(f'Program:\n\n {program}')

print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Lexer results xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
lexer = Lexer(table, G.EOF)
tokenss = lexer(program)
print(tokenss)
tokens = [token.token_type for token in tokenss]
print('✅ OK')

print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Parser results xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
slr1 = SLR1Parser(G)
out, oper = slr1(tokens)
# print(out)
# print(oper)
ast = evaluate_reverse_parse(out,oper,tokenss)
print('✅ OK')

print("\nxxxxxxxxxxxxxxxxxxxxxxxxx Semantic-Checker results xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
errors = []

print("\nCollecting types...")
collector = TypeCollector(errors)
collector.visit(ast)

context = collector.context

collector_errors = len(errors)
print(f"Found {collector_errors} errors")
print()

print("\nBuilding types...")
builder = TypeBuilder(context, errors)
builder.visit(ast)

builder_errors = len(errors) - collector_errors
print(f"Found {builder_errors} errors")

print('\nContext:')
print(context)

print('✅ OK')
