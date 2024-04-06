import cmp.visitor as visitor
from parser.ast_nodes import *
from cmp.semantic import Context, Scope
from cmp.semantic import *
import math
import random

def iterabilizate(body):
    if not isinstance(body, list):
        return [body]
    else:
        return body

class Interpreter:
    def __init__(self, context):
        self.context: Context = context

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, scope=None):
        pass


    @visitor.when(FuncDefNode)
    def visit(self, node: FuncDefNode, scope: Scope):
        pass


    @visitor.when(TypeDefNode)
    def visit(self, node: TypeDefNode, scope: Scope):
        pass
        

    @visitor.when(TypePropDefNode)
    def visit(self, node: TypePropDefNode, scope: Scope):
        pass
        

    @visitor.when(TypeFuncDefNode)
    def visit(self, node: TypeFuncDefNode, scope: Scope):
        pass

    
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
       pass
    

    @visitor.when(AssignationNode)
    def visit(self, node: AssignationNode, scope: Scope):
        pass


    
    @visitor.when(DestructiveAssignationNode)
    def visit(self, node: DestructiveAssignationNode, scope: Scope):
        pass
        

    @visitor.when(IfElseNode)
    def visit(self, node: IfElseNode, scope: Scope):
        pass
    

    @visitor.when(ElifNode)
    def visit(self, node: ElifNode, scope: Scope):
        pass
    

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        pass
    

    @visitor.when(ForNode)
    def visit(self, node: ForNode, scope: Scope):
        pass


    @visitor.when(RangeNode)
    def visit(self, node: RangeNode, scope: Scope):
        pass      
     
    
    @visitor.when(PrintNode)
    def visit(self, node: PrintNode, scope: Scope):
        pass
    

    # instance type
    @visitor.when(InstanceNode)
    def visit(self, node: InstanceNode, scope: Scope):
        pass


    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope):
        pass


    @visitor.when(TypeFuncCallNode)
    def visit(self, node: TypeFuncCallNode, scope: Scope):
        pass


    @visitor.when(SelfCallPropNode)
    def visit(self, node: SelfCallPropNode, scope:Scope):
        pass
        

    @visitor.when(SelfCallFuncNode)
    def visit(self, node: SelfCallFuncNode, scope:Scope):
        pass


    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode, scope):
        pass

    
    @visitor.when(AsNode)
    def visit(self, node: AsNode, scope: Scope):
        pass

    @visitor.when(IsNode)
    def visit(self, node: IsNode, scope: Scope):
        pass
    

    @visitor.when(NumNode)
    def visit(self, node, scope):
        # previous analysis to return correct type (idk if it's relevant)
        float_repr = float(node.token) 
        int_repr = int(node.token)
        return float_repr if float_repr - int_repr != 0 else int_repr
    

    @visitor.when(StringNode)
    def visit(self, node, scope):
        return str(node.token)
    

    @visitor.when(BoolNode)
    def visit(self, node, scope):
        return bool(node.token)

    @visitor.when(VarNode)
    def visit(self, node: VarNode, scope: Scope):
        pass


    @visitor.when(RanNode)
    def visit(self, node, scope):
        return random.uniform(0.0,1.0)
    

    @visitor.when(UnaryNumOperationNode)
    def visit(self, node: UnaryNumOperationNode, scope: Scope):
        pass

    
    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope: Scope):
        value_expr = self.visit(node.expr)
        return not value_expr 
    

    @visitor.when(BinaryNumOperationNode)
    def visit(self, node: BinaryNumOperationNode, scope: Scope):
        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
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
    def visit(self, node: BinaryStringOperationNode, scope: Scope):
        pass
    

    @visitor.when(AndOrNode)
    def visit(self, node, scope):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right,scope)
        return left_value or right_value if node.token == '&' else left_value and right_value
    

    @visitor.when(EqualDiffNode)
    def visit(self, node, scope):
        pass
    

    @visitor.when(ComparisonNode)
    def visit(self, node, scope):
        pass
            


        