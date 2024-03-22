from utils import Token

class Node:
    def __init__(self, token):
        self.token = token


class ProgramNode(Node):
    def __init__(self, statement_seq, expr):
        self.statement_seq = statement_seq
        self.expr = expr


class StatementNode(Node):
    pass


# body_exp = <exp> | <block_exp>
class FuncDefNode(StatementNode):
    def __init__(self, id, params, body_expr, token):
        self.id = id
        self.params = params
        self.body = body_expr
        self.token = token


class TypeDefNode(StatementNode):
    def __init__(self, id, body, token, params=[], parent_id=None, parent_params=[]):
        self.id = id
        self.body = body
        self.token = token
        self.parent = parent_id
        self.parent_params = parent_params

class TypeBodyItemNode(Node):
    pass

class TypePropDefNode(TypeBodyItemNode):
    def __init__(self, id, exp, token):
        self.id = id
        self.exp = exp
        self.token = token

class TypeFuncDefNode(TypeBodyItemNode):
    def __init__(self, id, params, body):
        self.id = id
        self.params = params
        self.body = body
        self.token = Token(id.lex, 'typeFuncNode')



class ExpressionNode(Node):
    pass


# Use also for <destr_assignation>
class AssignationNode(Node):
    def __init__(self, id, body, token):
        self.id = id
        self.body = body
        self.token = token


class LetNode(ExpressionNode):
    def __init__(self, assignations, body, token):
        self.assignations = assignations
        self.body = body
        self.token = token


class IfElseNode(ExpressionNode):
    def __init__(self, condition, then_expr, else_expr, token, elif_list=[]):
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr
        self.token = token
        self.elif_list = elif_list


class ElifNode(Node):
    def __init__(self, condition, then_expr, token):
        self.condition = condition
        self.then_expr = then_expr
        self.token = token


class WhileNode(ExpressionNode):
    def __init__(self, condition, body, token):
        self.condition = condition
        self.body = body
        self.token = token


class ForNode(ExpressionNode):
    def __init__(self, iterable, body, token):
        self.iterable = iterable
        self.body = body
        self.token = token


class BlockNode(ExpressionNode):
    def __init__(self, expr_list, token):
        self.expr_list = expr_list
        self.token = token


class RangeNode(ExpressionNode):
    def __init__(self, start, end, token):
        self.start = start
        self.end = end
        self.token = token


class PrintNode(ExpressionNode):
    def __init__(self, expr, token):
        self.expr = expr
        self.token = token


class InstanceNode(ExpressionNode):
    def __init__(self, id, params, token):
        self.id = id
        self.params = params
        self.token = token


class AtomicNode(ExpressionNode):
    pass


class CallNode(AtomicNode):
    def __init__(self, id, params):
        self.id = id
        self.params = params
        self.token = Token(id.lex, 'functionCall')

class TypePropCallNode(AtomicNode):
    def __init__(self, type_id, prop_id):
        self.type_id = type_id
        self.prop_id = prop_id

class TypeFuncCallNode(AtomicNode):
    def __init__(self, type_id, prop_id, params):
        self.type_id = type_id
        self.prop_id = prop_id
        self.params = params

class NumNode(AtomicNode):
    pass
class StringNode(AtomicNode):
    pass
class BoolNode(AtomicNode):
    pass
class VarNode(AtomicNode):
    pass
class RanNode(AtomicNode):
    pass


class UnaryNode(ExpressionNode):
    def __init__(self, expr, token):
        self.expr = expr
        self.token = token


class UnaryNumOperationNode(UnaryNode):
    pass
class UnaryLogicOperationNode(UnaryNode):
    pass


class SqrtNode(UnaryNumOperationNode):
    pass
class SinNode(UnaryNumOperationNode):
    pass
class CosNode(UnaryNumOperationNode):
    pass
class ExpNode(UnaryNumOperationNode):
    pass
class NotNode(UnaryLogicOperationNode):
    pass



class BinaryNode(ExpressionNode):
    def __init__(self, left, right, token):
        self.left = left
        self.right = right
        self.token = token


class BinaryNumOperationNode(BinaryNode):
    pass
class BinaryLogicOperationNode(BinaryNode):
    pass
class BinaryStringOperationNode(BinaryNode):
    pass


class PlusNode(BinaryNumOperationNode):
    pass
class MinusNode(BinaryNumOperationNode):
    pass
class StartNode(BinaryNumOperationNode):
    pass
class DivNode(BinaryNumOperationNode):
    pass
class ModNode(BinaryNumOperationNode):
    pass
class PowNode(BinaryNumOperationNode):
    pass
class LogNode(BinaryNumOperationNode):
    pass


class EqualNode(BinaryLogicOperationNode):
    pass
class DifferenceNode(BinaryLogicOperationNode):
    pass
class LessThanNode(BinaryLogicOperationNode):
    pass
class LessEqualThanNode(BinaryLogicOperationNode):
    pass
class GreaterThanNode(BinaryLogicOperationNode):
    pass
class GreaterEqualThanNode(BinaryLogicOperationNode):
    pass
class AndNode(BinaryLogicOperationNode):
    pass
class OrNode(BinaryLogicOperationNode):
    pass


class ConcatNode(BinaryStringOperationNode):
    pass
class DoubleConcatNode(BinaryStringOperationNode):
    pass