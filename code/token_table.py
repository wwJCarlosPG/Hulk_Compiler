from grammar.hulk_grammar import *


sym = [  
    ',',
    ':',
    ';',
    '<',
    '>',
    '?',
    '!',
    '%',
    '.',
    '\'',
    ' ',
    '\n',
    '\t',
    r'\\"'
    ]
print(sym)
symbols = '|'.join(str(n) for n in sym)
nonzero_digits = '|'.join(str(n) for n in range(1,10))
zero_digits = '|'.join(str(n) for n in range(0,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
letters += letters.join('|')
letters += '|'.join(chr(n) for n in range(ord('A'),ord('Z')+1))
alphanumeric = f'{letters}|{zero_digits}'+'|'+'_'
alphanumeric_with_symbols= alphanumeric+'|'+symbols

table = [
    (string_, f'((")({alphanumeric_with_symbols})*("))'),
    (plus_, '+'),
    (minus_, '-'),
    (times_, '\*'),
    (div_, '/'),
    (pow_, '^'),
    (mod_,'%'),
    (opar_, '\('),
    (cpar_, '\)'),
    (obracket_, '{'),
    (cbracket_, '}'),
    (semicolon_, ';'),
    (colon_, ':'),
    (coma_, ','),
    (dot_,'.'),
    (equals_, '='),
    (destr_assign_,':='),
    (true_,'true'),
    (false_,'false'),
    (and_logic_c_,'&'),
    (or_logic_c_,'\|'),
    (not_logic_c_,'!'),
    (doubleequals_c_,'=='),
    (different_c_,'!='),
    (lt_c_,'<'),
    (gt_c_,'>'),
    (let_c_,'<='),
    (get_c_,'>='),
    (if_,'if'),
    (else_,'else'),
    (elif_,'elif'),
    (let_ , 'let'),
    (in_ , 'in'), 
    (as_, 'as'),
    (is_, 'is'),
    (while_,'while'),
    (for_,'for'),
    (range_,'range'),
    (function_,'function'),
    (arrow_,'=>'),
    (new_,'new'),
    (type_,'type'),
    (inherits_, 'inherits'),
    (self_, 'self'),
    (base_, 'base'),
    (print_,'print'),
    (sqrt_, 'sqrt'),
    (sin_,'sin'),
    (cos_,'cos'),
    (exp_,'exp'),
    (log_,'log'),
    (rand_,'rand'),     
    (id_, f'(({letters})({alphanumeric})*)'),
    (num_, f'0|(({nonzero_digits})({zero_digits})*)'),
    (at_,'@'),
    (doubleat_,'@@')
]

