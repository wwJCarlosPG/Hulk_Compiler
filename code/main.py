from token_table import table
from lexer.lexer import Lexer
from parser.SLR1Parser import SLR1Parser
from grammar.hulk_grammar import get_grammar
from cmp.evaluation import evaluate_reverse_parse
from semantic_check.TypeCollector import TypeCollector
from semantic_check.TypeBuilder import TypeBuilder
from semantic_check.TypeChecker import TypeChecker
from cases import get_cases

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
for program in get_cases(1):
    print(f'Program:\n\n {program}')

    print("\n|---------- Lexer results -----------|\n")
    lexer = Lexer(table, G.EOF)
    tokenss = lexer(program)
    # print(tokenss)
    tokens = [token.token_type for token in tokenss]
    print('✅ OK')
    
    print("\n|---------- Parser results ----------|\n")
    slr1 = SLR1Parser(G)
    out, oper = slr1(tokens)
    # print(out)
    # print(oper)
    ast = evaluate_reverse_parse(out,oper,tokenss)
    print('✅ OK')


    print("\n|----- Semantic-Checker results -----|\n")
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
    print('\nContext:')
    print(context)


    print("\nChecking types...") #------------------------------------
    checker = TypeChecker(context, errors)
    exp_type = checker.visit(ast)
    check_errors(errors, "Type Checker")

    print('✅ OK')

