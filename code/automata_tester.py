from lexer.lexer import Lexer
s = [ 
    '_', 
    ',',
    ':',
    ';',
    '<',
    '>',
    '?',
    '!',
    '%',
    '.',
    '\n',
    '\t'
    ]
symbols = '|'.join(str(n) for n in s)
print(symbols)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
nonzero_digits = '|'.join(str(n) for n in range(1,10))
zero_digits = '|'.join(str(n) for n in range(0,10))
print(zero_digits)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
print(letters)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
letters += letters.join('|')
print(letters)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
letters += '|'.join(chr(n) for n in range(ord('A'),ord('Z')+1))
print(letters)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
alphanumeric = f'{letters}|{zero_digits}'
alphanumeric_with_spaces = alphanumeric
alphanumeric_with_spaces+='|'+ ' '
alphanumeric_with_spaces+='|'+symbols
print(alphanumeric_with_spaces)
lexer = Lexer([
    ('str', f'((")({alphanumeric_with_spaces})*("))'),
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
    ('id', f'(({letters})({alphanumeric})*)'),
    ('num', f'(({nonzero_digits})({zero_digits})*)'),
    ('concat','@'),
    ('concatX2','@@')
], 'eof')
text = 'let    x=10,y=202 in (332823948*xiom304230)'
text = 'while(x<=new 104) "x","y" { if (x!=136) x = @4 else x="mas_ss5, mk, type j." }'
#text = 'let    xz=10,y="hello hs" in (332823948*xiom304203)'
print(f'\n>>> Tokenizando: "{text}"')
tokens = lexer(text)
print(tokens)


# issues:
# don't recognize \" within str
#
#
#