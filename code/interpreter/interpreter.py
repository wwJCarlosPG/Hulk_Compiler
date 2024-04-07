import cmp.visitor as visitor
from parser.ast_nodes import *
from cmp.semantic import Context, context
from cmp.semantic import *
import math
import random
from interpreter.utils import Context

def iterabilizate(body):
    if not isinstance(body, list):
        return [body]
    else:
        return body

class Interpreter:
    def __init__(self, context):
        self.context: Context  = context

    @visitor.on('node')
    def visit(self, node, context):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, context=None):
        pass


    @visitor.when(FuncDefNode)
    def visit(self, node: FuncDefNode, context: Context):
        pass


    @visitor.when(TypeDefNode)
    def visit(self, node: TypeDefNode, context: Context):
        pass
        

    @visitor.when(TypePropDefNode)
    def visit(self, node: TypePropDefNode, context: Context):
        pass
        

    @visitor.when(TypeFuncDefNode)
    def visit(self, node: TypeFuncDefNode, context: Context):
        pass

    
    @visitor.when(LetNode)
    def visit(self, node: LetNode, context: Context):
       pass
    

    @visitor.when(AssignationNode)
    def visit(self, node: AssignationNode, context: Context):
        pass


    
    @visitor.when(DestructiveAssignationNode)
    def visit(self, node: DestructiveAssignationNode, context: Context):
        pass
        

    @visitor.when(IfElseNode)
    def visit(self, node: IfElseNode, context: Context):
        pass
    

    @visitor.when(ElifNode)
    def visit(self, node: ElifNode, context: Context):
        pass
    

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, context: Context):
        pass
    

    @visitor.when(ForNode)
    def visit(self, node: ForNode, context: Context):
        pass


    @visitor.when(RangeNode)
    def visit(self, node: RangeNode, context: Context):
        pass      
     
    
    @visitor.when(PrintNode)
    def visit(self, node: PrintNode, context: Context):
        pass
    

    # instance type
    @visitor.when(InstanceNode)
    def visit(self, node: InstanceNode, context: Context):
        pass


    @visitor.when(CallNode)
    def visit(self, node: CallNode, context: Context):
        pass


    @visitor.when(TypeFuncCallNode)
    def visit(self, node: TypeFuncCallNode, context: Context):
        pass


    @visitor.when(SelfCallPropNode)
    def visit(self, node: SelfCallPropNode, context:context):
        pass
        

    @visitor.when(SelfCallFuncNode)
    def visit(self, node: SelfCallFuncNode, context:context):
        pass


    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode, context):
        pass

    
    @visitor.when(AsNode)
    def visit(self, node: AsNode, context: Context):
        pass

    @visitor.when(IsNode)
    def visit(self, node: IsNode, context: Context):
        pass
    

    @visitor.when(NumNode)
    def visit(self, node, context):
        # previous analysis to return correct type (idk if it's relevant)
        float_repr = float(node.token) 
        int_repr = int(node.token)
        return float_repr if float_repr - int_repr != 0 else int_repr
    

    @visitor.when(StringNode)
    def visit(self, node, context):
        return str(node.token)
    

    @visitor.when(BoolNode)
    def visit(self, node, context):
        return bool(node.token)

    @visitor.when(VarNode)
    def visit(self, node: VarNode, context: Context):
        pass


    @visitor.when(RanNode)
    def visit(self, node, context):
        return random.uniform(0.0,1.0)
    

    @visitor.when(UnaryNumOperationNode)
    def visit(self, node: UnaryNumOperationNode, context: Context):
        pass

    
    @visitor.when(NotNode)
    def visit(self, node: NotNode, context: Context):
        value_expr = self.visit(node.expr, context)
        return not value_expr 
    

    @visitor.when(BinaryNumOperationNode)
    def visit(self, node: BinaryNumOperationNode, context: Context):
        left = self.visit(node.left,context)
        right = self.visit(node.right,context)
        if node.token == '+':
            return left + right
        elif node.token == '-':
            return left - right
        elif node.token == '*':
            return left*right
        elif node.token == '/':
            return left/right
        elif node.token == '**' or node.token == '^':
            return math.pow(left, right)
        else:
            raise Exception(f'Operator {node.token} is invalid')
            # never raise this exception
        
    
    @visitor.when(BinaryStringOperationNode)
    def visit(self, node: BinaryStringOperationNode, context: Context):
        right_value = self.visit(node.right, context)
        left_value = self.visit(node.left, context)
        if node.token == '@':
            return str(right_value) + str(left_value)
        elif node.token == '@@':
            return str(right_value) + ' ' + str(left_value)
        else: 
            raise Exception(f'Operator {node.token} is invalid')
    

    @visitor.when(AndOrNode)
    def visit(self, node, context):
        left_value = self.visit(node.left, context)
        right_value = self.visit(node.right,context)
        return left_value or right_value if node.token == '&' else left_value and right_value
    

    @visitor.when(EqualDiffNode)
    def visit(self, node, context):
        # no me queda clara la separación esta por qué
        left_value = self.visit(node.left, context)
        right_value = self.visit(node.right, context)
        if node.token == '==':
            return left_value == right_value
        elif node.token == '!=':
            return left_value != right_value
        else:
            raise Exception(f'Operator {node.token} is invalid')
    

    @visitor.when(ComparisonNode)
    def visit(self, node, context):
        left_value = self.visit(node.left, context)
        right_value = self.visit(node.right, context)
        if node.token == '<':
            return left_value<right_value
        elif node.token == '>':
            return left_value>right_value
        elif node.token == '>=':
            return left_value>=right_value
        elif node.token == '<=':
            return left_value<=right_value
        else:
            raise Exception(f'Operator {node.token} is invalid')
        
        pass
            


        