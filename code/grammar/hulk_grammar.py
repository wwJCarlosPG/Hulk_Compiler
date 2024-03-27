from cmp.pycompiler import Grammar
from parser.ast_nodes import *


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
str_exp, str_const = G.NonTerminals('<str_exp> <str_const>')

# math_func
sqrt_, sin_, cos_, exp_, log_, rand_ = G.Terminals('sqrt sin cos exp log rand')
math_func = G.NonTerminal('<math_func>')

# boolean and conditions
doubleequals_c_, different_c_, lt_c_, gt_c_, let_c_, get_c_, or_logic_c_, and_logic_c_, not_logic_c_, true_, false_ = G.Terminals('== != < > <= >= | & ! true false')
bool_exp, bool_term, bool_factor, bool_cmp, bool_const = G.NonTerminals('<bool_exp> <bool_term> <bool_factor> <bool_cmp> <bool_const>')

# if else
if_, else_, elif_ = G.Terminals('if else elif')
conditionals_exp, elif_list = G.NonTerminals('<conditionals_exp> <elif_list>')

# loops
while_, for_, range_ = G.Terminals('while for range')
loop_exp, range_exp = G.NonTerminals('<loop_exp> <range_exp>')

# expressions
print_ = G.Terminal('print')
exp = G.NonTerminal('<exp>')
base_element = G.NonTerminal('<base_element>')

# var assingnment
let_, in_, equals_, coma_, destr_assign_ = G.Terminals('let in = , :=')
var_def, var_def_list, destr_assignment = G.NonTerminals('<var_def> <var_def_list> <destr_assignment>')

# functions
function_, arrow_, semicolon_, obracket_, cbracket_ = G.Terminals('function => ; { }')
inline_func_def, exp_list, block_func_def, block_exp, block_items = G.NonTerminals('<inline_func_def> <exp_list> <block_func_def> <block_exp> <block_items>')

# types
type_def, type_header_def, type_body, type_body_statements, type_body_item, type_body_prop, type_body_func, type_instance = G.NonTerminals('<type_def> <type_header_def> <type_body> <type_body_statements> <type_body_item> <type_body_prop> <type_body_func> <type_instance>')
type_, inherits_, new_, dot_ = G.Terminals('type inherits new .')





# ~~~~~~~~~~~~~~~~ PRODUCTIONS ~~~~~~~~~~~~~~~~~~~
program %= statement_seq + exp, lambda _, s: ProgramNode(s[1], s[2])
program %= exp, lambda _, s: ProgramNode([],s[1]) 

statement_seq %= statement, lambda _, s: [s[1]]
statement_seq %= statement + statement_seq, lambda _, s: [s[1]] + s[2] 


statement %= inline_func_def, lambda _, s: s[1] 
statement %= block_func_def, lambda _, s: s[1] 
statement %= type_def, lambda _, s: s[1] 

# Function definitions
inline_func_def %= function_ + id_ + opar_ + exp_list + cpar_ + arrow_ + exp + semicolon_, lambda _, s: FuncDefNode(s[2], s[4], s[7], s[1])
inline_func_def %= function_ + id_ + opar_ + cpar_ + arrow_ + exp + semicolon_, lambda _, s: FuncDefNode(s[2], [], s[6], s[1])

block_func_def %= function_ + id_ + opar_ + exp_list + cpar_ + block_exp, lambda _, s: FuncDefNode(s[2], s[4], s[6], s[1])
block_func_def %= function_ + id_ + opar_ + cpar_ + block_exp, lambda _, s: FuncDefNode(s[2], [], s[5], s[1])


# Expression block
block_exp %= obracket_ + block_items + cbracket_, lambda _, s: BlockNode(s[2], s[1])

block_items %= exp + semicolon_, lambda _, s: [s[1]]
block_items %= exp + semicolon_ + block_items, lambda _, s: [s[1]] + s[3]



# Expression list
exp_list %= exp, lambda _, s: [s[1]]
exp_list %= exp + coma_ + exp_list, lambda _, s: [s[1]] + s[3]



# Variable definition
var_def %= let_ + var_def_list + in_ + exp, lambda _, s: LetNode(s[2], s[4], s[1])

var_def_list %= id_ + equals_ + exp, lambda _, s: [AssignationNode(s[1], s[3], s[2])]
var_def_list %= id_ + equals_ + exp + coma_ + var_def_list, lambda _, s: [AssignationNode(s[1], s[3], s[2])] + s[5]

destr_assignment %= id_ + destr_assign_ + exp, lambda _, s: AssignationNode(s[1], s[3], s[2])



# expression
exp %= print_ + opar_ + exp + cpar_ , lambda _, s: PrintNode(s[3], s[1]) 
exp %= var_def, lambda _, s: s[1] 
exp %= destr_assignment, lambda _, s: s[1] 
exp %= conditionals_exp, lambda _, s: s[1] 
exp %= loop_exp, lambda _, s: s[1] 
exp %= type_instance, lambda _, s: s[1] 
exp %= block_exp, lambda _, s: s[1] 
exp %= bool_exp, lambda _, s: s[1] 



# Types definition
type_def %= type_header_def + semicolon_, lambda _, s: s[1]
type_def %= type_ + id_ + inherits_ + id_ + type_body + semicolon_, lambda _, s: TypeDefNode(s[2], s[5], s[1], [], s[4], [])
type_def %= type_ + id_ + opar_ + exp_list + cpar_ + inherits_ + id_ + opar_ + exp_list + cpar_ + type_body + semicolon_, lambda _, s: TypeDefNode(s[2], s[11], s[1], s[4], s[7], s[9])

type_header_def %= type_ + id_ + opar_ + exp_list + cpar_ + type_body, lambda _, s: TypeDefNode(s[2], s[6], s[1], s[4], None, [])
type_header_def %= type_ + id_ + type_body, lambda _, s: TypeDefNode(s[2], s[3], s[1], [], None, [])

type_body %= obracket_ + cbracket_, lambda _, s: []
type_body %= obracket_ + type_body_statements + cbracket_, lambda _, s: s[2]

type_body_statements %= type_body_item, lambda _, s: s[1]
type_body_statements %= type_body_item + type_body_statements, lambda _, s: s[1] + s[2]

type_body_item %= type_body_prop, lambda _, s: s[1]
type_body_item %= type_body_func, lambda _, s: s[1]

type_body_prop %= id_ + equals_ + exp + semicolon_, lambda _, s: [TypePropDefNode(s[1], s[3], s[2])]

type_body_func %= id_ + opar_ + exp_list + cpar_ + arrow_ + exp, lambda _, s: [TypeFuncDefNode(s[1], s[3], s[6])]
type_body_func %= id_ + opar_ + cpar_ + arrow_ + exp, lambda _, s: [TypeFuncDefNode(s[1], [], s[5])]
type_body_func %= id_ + opar_ + exp_list + cpar_ + block_exp , lambda _, s: [TypeFuncDefNode(s[1], s[3], s[5])]
type_body_func %= id_ + opar_ + cpar_ + block_exp, lambda _, s: [TypeFuncDefNode(s[1], [], s[4])]

type_instance %= new_ + id_ + opar_ + exp_list + cpar_, lambda _, s: InstanceNode(s[2], s[4], s[1])
type_instance %= new_ + id_ + opar_ + cpar_, lambda _, s: InstanceNode(s[2], [], s[1])



# Conditionals
conditionals_exp %= if_ + opar_ + bool_exp + cpar_ + exp + else_ + exp, lambda _, s: IfElseNode(s[3], s[5], s[7], s[1])
conditionals_exp %= if_ + opar_ + bool_exp + cpar_ + exp + elif_list + else_ + exp, lambda _, s: IfElseNode(s[3], s[5], s[8], s[1], s[6])

elif_list %= elif_ + opar_ + bool_exp + cpar_ + exp, lambda _, s: [ElifNode(s[3], s[5], s[1])]
elif_list %= elif_ + opar_ + bool_exp + cpar_ + exp + elif_list, lambda _, s: [ElifNode(s[3], s[5], s[1])] + s[6]


# Loops
loop_exp %= while_ + opar_ + bool_exp + cpar_ + exp, lambda _, s: WhileNode(s[3], s[5], s[1]) 
loop_exp %= for_ + opar_ + id_ + in_ + range_exp + cpar_ + exp, lambda _, s: ForNode(s[5], s[7], s[1])
range_exp %= range_ + opar_ + num_exp + coma_ + num_exp + cpar_, lambda _, s: RangeNode(s[3], s[5], s[1])



# boolean
bool_exp %= bool_exp + or_logic_c_ + bool_term, lambda _, s: OrNode(s[1], s[3], s[2])
bool_exp %= bool_term, lambda _, s: s[1]

bool_term %= bool_term + and_logic_c_ + bool_factor, lambda _, s: AndNode(s[1], s[3], s[2])
bool_term %= bool_factor, lambda _, s: s[1]

bool_factor %= not_logic_c_ + bool_factor, lambda _, s: NotNode(s[2], s[1])
bool_factor %= bool_cmp, lambda _, s: s[1]

bool_cmp %= bool_cmp + doubleequals_c_ + bool_const, lambda _, s: EqualNode(s[1], s[3], s[2])
bool_cmp %= bool_cmp + different_c_ + bool_const, lambda _, s: DifferenceNode(s[1], s[3], s[2])
bool_cmp %= bool_cmp + lt_c_ + bool_const, lambda _, s: LessThanNode(s[1], s[3], s[2])
bool_cmp %= bool_cmp + gt_c_ + bool_const, lambda _, s: GreaterThanNode(s[1], s[3], s[2])
bool_cmp %= bool_cmp + get_c_ + bool_const, lambda _, s: GreaterEqualThanNode(s[1], s[3], s[2])
bool_cmp %= bool_cmp + let_c_ + bool_const, lambda _, s: LessEqualThanNode(s[1], s[3], s[2])
bool_cmp %= bool_const, lambda _, s: s[1]

bool_const %= str_exp, lambda _, s: s[1]



# str
str_exp %= str_exp + at_ + str_const, lambda _, s: ConcatNode(s[1], s[3], s[2])
str_exp %= str_exp + doubleat_ + str_const, lambda _, s: DoubleConcatNode(s[1], s[3], s[2])
str_exp %= str_const, lambda _, s: s[1]

str_const %= num_exp, lambda _, s: s[1]



# num
num_exp %= num_exp + plus_ + term, lambda _, s: PlusNode(s[1], s[3], s[2])
num_exp %= num_exp + minus_ + term, lambda _, s: MinusNode(s[1], s[3], s[2])
num_exp %= term, lambda _, s: s[1]

term %= term + times_ + factor, lambda _, s: StartNode(s[1], s[3], s[2]) 
term %= term + div_ + factor, lambda _, s: DivNode(s[1], s[3], s[2]) 
term %= term + mod_ + factor, lambda _, s: ModNode(s[1], s[3], s[2]) 
term %= factor, lambda _, s: s[1]

factor %= factor + pow_ + const, lambda _, s: PowNode(s[1], s[3], s[2]) 
factor %= const, lambda _, s: s[1]

const %= opar_ + num_exp + cpar_, lambda _, s: s[2]
const %= num_, lambda _, s: NumNode(s[1])
const %= E_const_, lambda _, s: NumNode(s[1])
const %= PI_const_, lambda _, s: NumNode(s[1])
const %= math_func, lambda _, s: s[1]
const %= base_element, lambda _, s: s[1]


# Base elements
base_element %= string_, lambda _, s: StringNode(s[1])
base_element %= true_, lambda _, s: BoolNode(s[1])
base_element %= false_, lambda _, s: BoolNode(s[1])
base_element %= id_ , lambda _, s: VarNode(s[1])
base_element %= func_call, lambda _, s: s[1]
base_element %= type_prop_func_call, lambda _, s: s[1]



# Calls
func_call %= id_ + opar_ + exp_list + cpar_, lambda _, s: CallNode(s[1], s[3])

type_prop_func_call %= id_ + dot_ + id_ + opar_ + cpar_, lambda _, s: TypeFuncCallNode(s[1], s[3], [])
type_prop_func_call %= id_ + dot_ + id_ + opar_ + exp_list + cpar_, lambda _, s: TypeFuncCallNode(s[1], s[3], s[5])
type_prop_func_call %= id_ + dot_ + id_, lambda _, s: TypePropCallNode(s[1], s[3])


# Built-in functions
math_func %= sqrt_ + opar_ + num_exp + cpar_, lambda _, s: SqrtNode(s[3], s[1])
math_func %= sin_ + opar_ + num_exp + cpar_, lambda _, s: SinNode(s[3], s[1]) 
math_func %= cos_ + opar_ + num_exp + cpar_, lambda _, s: CosNode(s[3], s[1])
math_func %= exp_ + opar_ + num_exp + cpar_, lambda _, s: ExpNode(s[3], s[1])
math_func %= log_ + opar_ + num_exp + coma_ + num_exp + cpar_ , lambda _, s: LogNode(s[3], s[5], s[1])
math_func %= rand_ + opar_ + cpar_, lambda _, s: RanNode(s[1])



def get_grammar():
    return G