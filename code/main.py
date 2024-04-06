from token_table import table
from lexer.lexer import Lexer
from parser.SLR1Parser import SLR1Parser
from grammar.hulk_grammar import get_grammar
from cmp.evaluation import evaluate_reverse_parse
from semantic_check.TypeCollector import TypeCollector
from semantic_check.TypeBuilder import TypeBuilder
from semantic_check.TypeChecker import TypeChecker
from cases import get_cases
from parser.utils import LexicalError

def check_errors(errors: list, name: str):
    try:
        assert len(errors) == 0
    except:
        print(f"\n\n ⚠⚠⚠⚠⚠⚠ Semantic errors in {name} ⚠⚠⚠⚠⚠⚠")
        print('Errors: [')
        for error in errors:
            print('\t ❌', error)
        print(']')
        return True


G = get_grammar()
lexer = Lexer(table, G.EOF)
slr1 = SLR1Parser(G)
for program in get_cases():
    print("\n☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎☀︎")

    print(f'Program:\n\n {program}')

    print("\n|---------- Lexer results -----------|\n")
    tokens = lexer(program)
    # print(tokens)
    #tokens = [token.token_type for token in tokenss]
    print('✅ OK')
    
    print("\n|---------- Parser results ----------|\n")
    try:
        out, oper = slr1(tokens)
    except SyntaxError as e:
        print(f'❌ ERROR: {e}')
        print('❌ Finished with errors')
        continue
    except LexicalError as e:
        print(f'❌ ERROR: {e}')
        print('❌ Finished with errors')
        continue
    # print(out)
    # print(oper)
    ast = evaluate_reverse_parse(out,oper,tokens)
    print('✅ OK')


    print("\n|----- Semantic-Checker results -----|\n")
    errors = []

    print("\n🌱 Collecting types...") #----------------------------------
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    if check_errors(errors, "Type Collector"):
        print('❌ Finished with errors')
        continue


    print("\n🏗️ Building types...") #------------------------------------
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    if check_errors(errors, "Type Builder"):
        print('❌ Finished with errors')
        continue
    print('\nContext:')
    print(context)


    print("\n👀 Checking types...") #------------------------------------
    checker = TypeChecker(context, errors)
    exp_type = checker.visit(ast)
    if check_errors(errors, "Type Checker"):
        print('❌ Finished with errors')
        continue
        

    print('✅ Finished successfully')

