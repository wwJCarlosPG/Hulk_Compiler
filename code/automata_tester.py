import sys
sys.path.append('code/lexer')
sys.path.append('code/parser/grammar')
sys.path.append('code/parser')
from lexer import Lexer
nonzero_digits = '|'.join(str(n) for n in range(1,10))
zero_digits = '|'.join(str(n) for n in range(0,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
letters += letters.join('|')
letters += '|'.join(chr(n) for n in range(ord('A'),ord('Z')+1))
alphanumeric = f'({letters}|{nonzero_digits})'
print(letters)
lexer = Lexer([
    ('str', f'((")({alphanumeric})*("))'),
    ('num', f'(({nonzero_digits})(0|{nonzero_digits})*)'),
    ('plus', '+'),
    ('minus', '-'),
    ('star', '\*'),
    ('div', '/'),
    ('pow', '^'),
    ('mod','%'),
    ('opar', '\('),
    ('cpar', '\)'),
    ('ocur', '{'),
    ('ccur', '}'),
    ('semicolon', ';'),
    ('comma', ','),
    ('equals', '='),
    ('destr_eq',':='),
    ('true','true'),
    ('false','false'),
    ('and','&'),
    ('or','\|'),
    ('not','!'),
    ('eq','=='),
    ('neq','!='),
    ('lt','<'),
    ('gt','>'),
    ('le','<='),
    ('ge','>='),
    ('if','if'),
    ('else','else'),
    ('elif','elif'),
    ('let' , 'let'),
    ('in' , 'in'), 
    ('while','while'),
    ('for','for'),
    ('new','new'),
    ('type','type'),      
    ('id', f'({letters})*'),
    ('concat','@'),
    ('concatX2','@@')
], 'eof')
text = 'let    x=10,y=202 in (332823948*xiom304230)'
text = 'while(x<=new 104){ \n if (x!=136) x = @4 else x="asss5" }'
#text = 'let    xz=10,y=222 in (332823948*xiom304230)'
print(f'\n>>> Tokenizando: "{text}"')
tokens = lexer(text)
print(tokens)


# issues:
# don't recognize a one digit number
# don't recognize the strings with letters and digits
#
#
#