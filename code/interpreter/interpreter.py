import cmp.visitor as visitor
from parser.ast_nodes import *
from cmp.semantic import Context, context
from cmp.semantic import *
import math
import random
from interpreter.interpreter_context import Interpreter_Context

def iterabilizate(body):
    if not isinstance(body, list):
        return [body]
    else:
        return body

class Interpreter:
    def __init__(self, context):
        self.context: Interpreter_Context  = context

    @visitor.on('node')
    def visit(self, node, context):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, context=None):
        pass


    @visitor.when(FuncDefNode)
    def visit(self, node: FuncDefNode, context: Interpreter_Context):
        pass


    @visitor.when(TypeDefNode)
    def visit(self, node: TypeDefNode, context: Interpreter_Context):
        pass
        

    @visitor.when(TypePropDefNode)
    def visit(self, node: TypePropDefNode, context: Interpreter_Context):
        pass
        

    @visitor.when(TypeFuncDefNode)
    def visit(self, node: TypeFuncDefNode, context: Interpreter_Context):
        pass

    
    @visitor.when(LetNode)
    def visit(self, node: LetNode, context: Interpreter_Context):
       pass
    

    @visitor.when(AssignationNode)
    def visit(self, node: AssignationNode, context: Interpreter_Context):
        pass


    
    @visitor.when(DestructiveAssignationNode)
    def visit(self, node: DestructiveAssignationNode, context: Interpreter_Context):
        pass
        

    @visitor.when(IfElseNode)
    def visit(self, node: IfElseNode, context: Interpreter_Context):
        pass
    

    @visitor.when(ElifNode)
    def visit(self, node: ElifNode, context: Interpreter_Context):
        pass
    

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, context: Interpreter_Context):
        pass
    

    @visitor.when(ForNode)
    def visit(self, node: ForNode, context: Interpreter_Context):
        pass


    @visitor.when(RangeNode)
    def visit(self, node: RangeNode, context: Interpreter_Context):
        pass      
     
    
    @visitor.when(PrintNode)
    def visit(self, node: PrintNode, context: Interpreter_Context):
        pass
    

    # instance type
    @visitor.when(InstanceNode)
    def visit(self, node: InstanceNode, context: Interpreter_Context):
        pass


    @visitor.when(CallNode)
    def visit(self, node: CallNode, context: Interpreter_Context):
        pass


    @visitor.when(TypeFuncCallNode)
    def visit(self, node: TypeFuncCallNode, context: Interpreter_Context):
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
    def visit(self, node: AsNode, context: Interpreter_Context):
        pass

    @visitor.when(IsNode)
    def visit(self, node: IsNode, context: Interpreter_Context):
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
    def visit(self, node: VarNode, context: Interpreter_Context):
        pass


    @visitor.when(RanNode)
    def visit(self, node, context):
        return random.uniform(0.0,1.0)
    

    @visitor.when(UnaryNumOperationNode)
    def visit(self, node: UnaryNumOperationNode, context: Interpreter_Context):
        pass

    
    @visitor.when(NotNode)
    def visit(self, node: NotNode, context: Interpreter_Context):
        value_expr = self.visit(node.expr, context)
        return not value_expr 
    

    @visitor.when(BinaryNumOperationNode)
    def visit(self, node: BinaryNumOperationNode, context: Interpreter_Context):
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
            raise Exception(f'Operation {node.token} is invalid')
            # never raise this exception
        
    
    @visitor.when(BinaryStringOperationNode)
    def visit(self, node: BinaryStringOperationNode, context: Interpreter_Context):
        pass
    

    @visitor.when(AndOrNode)
    def visit(self, node, context):
        left_value = self.visit(node.left, context)
        right_value = self.visit(node.right,context)
        return left_value or right_value if node.token == '&' else left_value and right_value
    

    @visitor.when(EqualDiffNode)
    def visit(self, node, context):
        pass
    

    @visitor.when(ComparisonNode)
    def visit(self, node, context):
        pass
            


        