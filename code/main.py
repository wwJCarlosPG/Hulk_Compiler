from token_table import table
from lexer.lexer import Lexer
from parser.SLR1Parser import SLR1Parser
from grammar.hulk_grammar import get_grammar
from cmp.evaluation import evaluate_reverse_parse
from semantic_check.TypeCollector import TypeCollector
from semantic_check.TypeBuilder import TypeBuilder

G = get_grammar()

program0 = '''
print("Hello, World, \\"dear\\" Mr. while")
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
}
type Dog inherits Animal{
    name = name;
}
type Cat(name, skin) {
    name = name;
    skin = skin;
};
print("OK")
'''

program4 = '''
    let a  = 10 in while (b<=0){   
        print(a);
        a:=a-1;
    
    }
'''

program5 = '''
    function gcd(a, b) {
        while (a > 0){
            let m = a % b in {
                b := a;
                a := m;
            };
        };
    }
    for (x in range(0, 10)) print(x)
'''
program6 = '''
    function gcd(a, b) {
        while (a > 0){
            let m = a % b in {
                b := a;
                a := m;
            };
        };
    }
    print(5)
'''
program7 = '''
    function A() => let x=5 in {print(5);};
    print(5)
'''
program8 ='''
    function A(){
        let x=5 in print(5);
    }
    print(5);
'''
selector = 8
match selector:
    case 0:
        program = program0
    case 1:
        program = program1
    case 2:
        program = program2
    case 3:
        program = program3
    case 4:
        program= program4
    case 5:
        program= program5
    case 6:
        program= program6
    case 7:
        program= program7
    case 8:
        program= program8
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
slr1 = SLR1Parser(G, verbose=True)
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
