import sys
sys.path.append('code/lexer')
sys.path.append('code/parser/grammar')
sys.path.append('code/parser')
from lexer import Lexer
nonzero_digits = '|'.join(str(n) for n in range(0,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))

lexer = Lexer([
    ('plus', '+'),
    ('num', f'({nonzero_digits})+'),
    ('minus', '-'),
    ('star', '\*'),
    ('div', '/'),
    ('pow', '^'),
    ('opar', '\('),
    ('cpar', '\)'),
    ('comma', ','),
    ('equals', '='),
    ('let' , 'let'),
    ('in' , 'in'), 
    ('str', f'(")({letters}|{nonzero_digits})*(")'),      
    ('id', f'({letters})({nonzero_digits})+')
], 'eof')

text = 'let    x2="a20",y=222 in (332823948*xiom304230)'
print(f'\n>>> Tokenizando: "{text}"')
tokens = lexer(text)
print(tokens)