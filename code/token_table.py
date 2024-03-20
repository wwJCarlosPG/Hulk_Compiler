nonzero_digits = '|'.join(str(n) for n in range(0,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
letters += '|'.join(chr(n) for n in range(ord('A'),ord('Z')+1))

table = [
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
    ('true','true'),
    ('false','false'),
    ('and','&'),
    ('or','|'),
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
    ('num', f'({nonzero_digits})(0|{nonzero_digits})*'),
    ('str', f'(")({letters}|0|{nonzero_digits})*(")'),      
    ('id', f'({letters})({letters}|0|{nonzero_digits})*'),
    ('while','while'),
    ('for','for'),
    ('new','new')
    ('type','type'),
    ('concat','@'),
    ('concatX2','@@')
    
]

