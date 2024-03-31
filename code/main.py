from token_table import table
from lexer.lexer import Lexer
from parser.SLR1Parser import SLR1Parser
from grammar.hulk_grammar import get_grammar
from cmp.evaluation import evaluate_reverse_parse
from semantic_check.TypeCollector import TypeCollector
from semantic_check.TypeBuilder import TypeBuilder
from semantic_check.TypeChecker import TypeChecker

def check_errors(errors: list, name: str):
    try:
        assert len(errors) == 0
    except:
        print(f"\n\n ⚠⚠⚠⚠⚠⚠ Semantic errors in {name} ⚠⚠⚠⚠⚠⚠")
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')


G = get_grammar()

program0 = '''
type Animal(name){
    name = name;
    sound() => "Make Sound";
}
type Dog(name,color) inherits Animal(name, apsasp){
    name = name;
}
type Cat(name, skin) {
    name = name;
    skin = skin;
};
if (x == 5)print("4") elif(x<5) {print(6);} else{7;}
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
type Dog(name,color) inherits Animal(name, apsasp){
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
    for (x in range(gcd(6,2), 10)) print(x)
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

program9 = '''
type Animal(name) inherits Firulai(name){
    name = name;
    sound() => "Make Sound";
}
type Dog(name) inherits Animal(name){
    name = name;
}
type Firulai(name) inherits Dog(name) {
    name = name;
    skin = skin;
};
print("CYCLEEE")
'''
program10 ='''
    type Animal(name){
        name = name;
        sound() => "Make Sound";
    }
    type Dog(name) inherits Animal(name){
        name = name;
    }
    function A(a: number, b: number): number{
        let x: Dog = new Dog("Pep") in {
            let y = x as Animal in 2;
        };
    }
    print(5);
'''
program11 = '''
    type Bird {
    }

    type Plane {
    }

    type Superman {
    }

    let x = new Superman() in
        print(
            if (x is Bird) "It's bird!"
            elif (x is Plane) "It's a plane!"
            else "No, it's Superman!"
        );
'''

selector = 0
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
    case 9:
        program= program9
    case 10:
        program= program10
    case 11:
        program= program11
    case _:
        raise Exception("Selector error: selector out of range")




# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
slr1 = SLR1Parser(G)
lexer = Lexer(table, G.EOF)
for i in range(1):
    selector = i
    selector = 11

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
        case 9:
            program= program9
        case 10:
            program= program10
        case 11:
            program= program11
        case _:
            raise Exception("Selector error: selector out of range")

    print("\nxxxxxxxxxxxxxxxxxxxxxxxxx NEW PROGRAM xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
    print(f'Program:\n\n {program}')


    tokenss = lexer(program)
    print(tokenss)
    tokens = [token.token_type for token in tokenss]
    out, oper = slr1(tokens)
    # print(out)
    # print(oper)
    ast = evaluate_reverse_parse(out,oper,tokenss)
    errors = []

    print("\nCollecting types...") #----------------------------------
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    check_errors(errors, "Type Collector")
    

    print("\nBuilding types...") #------------------------------------
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    check_errors(errors, "Type Builder")


    print("\nChecking types...") #------------------------------------
    checker = TypeChecker(context, errors)
    exp_type = checker.visit(ast)
    check_errors(errors, "Type Checker")

    print('✅ OK')
# SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS



# print(f'Program:\n\n {program}')

# print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Lexer results xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
# lexer = Lexer(table, G.EOF)
# tokenss = lexer(program)
# print(tokenss)
# tokens = [token.token_type for token in tokenss]
# print('✅ OK')

# print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Parser results xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
# slr1 = SLR1Parser(G, verbose=True)
# out, oper = slr1(tokens)
# # print(out)
# # print(oper)
# ast = evaluate_reverse_parse(out,oper,tokenss)
# print('✅ OK')



# print("\nxxxxxxxxxxxxxxxxxxxxxxxxx Semantic-Checker results xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
# errors = []

# print("\nCollecting types...") #----------------------------------
# collector = TypeCollector(errors)
# collector.visit(ast)
# context = collector.context
# check_errors(errors, "Type Collector")


# print("\nBuilding types...") #------------------------------------
# builder = TypeBuilder(context, errors)
# builder.visit(ast)
# check_errors(errors, "Type Builder")
# print('\nContext:')
# print(context)


# print("\nChecking types...") #------------------------------------
# checker = TypeChecker(context, errors)
# exp_type = checker.visit(ast)
# check_errors(errors, "Type Checker")

# print('✅ OK')

