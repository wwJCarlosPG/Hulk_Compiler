from Parser_Generator import Parser_Generator
from grammar.hulk_grammar import get_grammar


G = get_grammar()
print(G)

parser_generator = Parser_Generator(G)
