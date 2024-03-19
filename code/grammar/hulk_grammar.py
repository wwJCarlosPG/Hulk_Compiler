from grammar.Grammar import Grammar


# Grammar hulk
G = Grammar()

# ~~~~~~~~~~~~~~~~~ SYMBOLS ~~~~~~~~~~~~~~~~~~
program = G.NonTerminal('<program>', startSymbol=True)
exp, statement_seq, statement, inline_func_def, block_func_def = G.NonTerminals('<exp> <statement_seq> <statement> <inline_func_def> <block_func_def>')

# num
plus_, minus_, times_, div_, mod_, pow_, opar_, cpar_, num_, E_const_, PI_const_, id_ = G.Terminals('+ - * / % ^ ( ) num E PI id')
num_exp, term, factor, const, math_func, func_call, type_prop_func_call = G.NonTerminals('<num_exp> <term> <factor> <const> <math_func> <func_call> <type_prop_func_call>')

# string
at_, doubleat_, string_ = G.Terminals('@ @@ string')
str_exp = G.NonTerminals('<str_exp>')

# math_func
sqrt_, sin_, cos_, exp_, log_, rand_ = G.Terminals('sqrt sin cos exp log rand')
math_func = G.NonTerminals('<math_func>')

# boolean and conditions
doubleequals_c_, different_c_, lt_c_, gt_c_, let_c_, get_c_, or_logic_c_, and_logic_c_, not_logic_c_, true_, false_ = G.Terminals('== != < > <= >= | & ! true false')
bool_exp, bool_const = G.NonTerminals('<bool_exp> <bool_const>')

# if else
if_, else_, elif_ = G.Terminals('if else elif')
conditionals_exp, elif_list = G.NonTerminals('<conditionals_exp> <elif_list>')

# loops
while_, for_, range_ = G.Terminals('while for range')
loop_exp, range_exp = G.NonTerminals('<loop_exp> <range_exp>')

# expressions
print_ = G.Terminals('print')
exp = G.NonTerminals('<exp>')

# var assingnment
let_, in_, equals_, coma_, destr_assign_ = G.Terminals('let in = , :=')
var_def, var_def_list, destr_assignment = G.NonTerminals('<var_def> <var_def_list> <destr_assignment>')

# functions
function_, arrow_, semicolon_, obracket_, cbracket_ = G.Terminals('function => ; { }')
inline_func_def, exp_list, block_func_def, block_exp, block_items = G.NonTerminals('<inline_func_def> <exp_list> <block_func_def> <block_exp> <block_items>')

# types
type_def, type_header_def, type_body, type_body_items, type_body_props, type_body_funcs, type_instance = G.NonTerminals('<type_def> <type_header_def> <type_body> <type_body_items> <type_body_props> <type_body_funcs> <type_instance>')
type_, inherits_, new_, dot_ = G.Terminals('type inherits new .')


# ~~~~~~~~~~~~~~~~ PRODUCTIONS ~~~~~~~~~~~~~~~~~~~
program %= statement_seq + exp | exp

statement_seq %= statement | statement + statement_seq
statement %= inline_func_def | block_func_def | type_def

# functions
inline_func_def %= function_ + id_ + opar_ + exp_list + cpar_ + arrow_ + exp + semicolon_ | function_ + id_ + opar_ + cpar_ + arrow_ + exp + semicolon_
block_func_def %= function_ + id_ + opar_ + exp_list + cpar_ + block_exp | function_ + id_ + opar_ + cpar_ + block_exp
block_exp %= obracket_ + block_items + cbracket_
block_items %= exp + semicolon_ | exp + semicolon_ + block_items
exp_list %= exp | exp + coma_ + exp_list

func_call %= id_ + opar_ + exp_list + cpar_

# variable assignment
var_def %= let_ + var_def_list + in_ + exp
var_def_list %= id_ + equals_ + exp | id_ + equals_ + exp + coma_ + var_def_list
destr_assignment %= id_ + destr_assign_ + exp

# expression
exp %= num_exp | str_exp | bool_exp | print_ + opar_ + exp + cpar_ | var_def | destr_assignment | conditionals_exp | range_exp | loop_exp | type_instance | block_exp | opar_ + exp + cpar_

# types
type_def %= type_header_def | type_ + id_ + inherits_ + id_ + type_body | type_ + id_ + opar_ + exp_list + cpar_ + inherits_ + id_ + opar_ + exp_list + cpar_ + type_body
type_header_def %= type_ + id_ + opar_ + exp_list + cpar_ + type_body | type_ + id_ + type_body
type_body %= obracket_ + type_body_items + cbracket_
type_body_items %= type_body_props + type_body_funcs | type_body_props + type_body_funcs + type_body_items
type_body_props %= id_ + equals_ + exp + semicolon_ | id_ + equals_ + exp + semicolon_ + type_body_props | G.Epsilon
type_body_funcs %= id_ + opar_ + exp_list + cpar_ + arrow_ + exp | id_ + opar_ + cpar_ + arrow_ + exp | id_ + opar_ + exp_list + cpar_ + block_exp | id_ + opar_ + cpar_ + block_exp | G.Epsilon
type_instance %= new_ + id_ + opar_ + exp_list + cpar_ | new_ + id_ + opar_ + cpar_
type_prop_func_call %= id_ + dot_ + id_ + opar_ + cpar_ | id_ + dot_ + id_ + opar_ + exp_list + cpar_ | id_ + dot_ + id_

# boolean and conditions
bool_exp %= bool_const | exp + doubleequals_c_ + exp | exp + different_c_ + exp | exp + lt_c_ + exp | exp + gt_c_ + exp | exp + get_c_ + exp | exp + let_c_ + exp | bool_exp + or_logic_c_ + bool_exp | bool_exp + and_logic_c_ + bool_exp | not_logic_c_ + bool_exp
bool_const %= true_ | false_ | id_ | func_call | type_prop_func_call

conditionals_exp %= if_ + opar_ + bool_exp + cpar_ + exp + else_ + exp | if_ + opar_ + bool_exp + cpar_ + exp + elif_list + else_ + exp
elif_list %= elif_ + opar_ + bool_exp + cpar_ + exp | elif_ + opar_ + bool_exp + cpar_ + exp + elif_list

# loops
loop_exp %= while_ + opar_ + bool_exp + cpar_ + exp | for_ + opar_ + id_ + in_ + range_exp + cpar_ + exp
range_exp %= range_ + opar_ + num_exp + coma_ + num_exp + cpar_

# num
num_exp %= num_exp + plus_ + term | num_exp + minus_ + term | term
term %= term + times_ + factor | term + div_ + factor | term + mod_ + factor | factor
factor %= factor + pow_ + const | const
const %= opar_ + num_exp + cpar_ | num_ | E_const_ | PI_const_ | math_func | id_ | func_call | type_prop_func_call

math_func %= sqrt_ + opar_ + num_exp + cpar_ | sin_ + opar_ + num_exp + cpar_ | cos_ + opar_ + num_exp + cpar_ | exp_ + opar_ + num_exp + cpar_ | log_ + opar_ + num_exp + coma_ + num_exp + cpar_ | rand_ + opar_ + cpar_

# str
str_exp %= string_ | str_exp + at_ + string_ | str_exp + at_ + term | id_ | func_call | type_prop_func_call | str_exp + doubleat_ + string_ | str_exp + doubleat_ + term




def get_grammar():
    return G