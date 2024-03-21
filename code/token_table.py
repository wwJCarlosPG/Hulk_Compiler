nonzero_digits = '|'.join(str(n) for n in range(1,10))
zero_digits = '|'.join(str(n) for n in range(0,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
letters += letters.join('|')
letters += '|'.join(chr(n) for n in range(ord('A'),ord('Z')+1))
alphanumeric = f'({letters}|{nonzero_digits})'
print(letters)
table = [
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
]

