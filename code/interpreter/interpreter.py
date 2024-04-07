import cmp.visitor as visitor
from parser.ast_nodes import *
from cmp.semantic import *
import math
import random
from interpreter.utils import Context, Scope

def iterabilizate(body):
    if not isinstance(body, list):
        return [body]
    else:
        return body


class Interpreter:
    def __init__(self):
        self.context: Context = Context()

    @visitor.on('node')
    def visit(self, node, scope=None):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        program_scope = self.context.scope

        statements = iterabilizate(node.statement_seq)
        for stat in statements:
            self.visit(stat, program_scope)
        
        # Evaluar la expresion final
        body = iterabilizate(node.expr)
        expr_value = None
        for exp in body:
            expr_value = self.visit(exp, program_scope)

        return expr_value


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
        child_scope = Scope(scope)

        assignations = iterabilizate(node.assignations)
        for assign in assignations:
            self.visit(assign, child_scope)

        body = iterabilizate(node.body)
        value = None
        for exp in body:
            value = self.visit(exp, child_scope)
        
        return value
    

    @visitor.when(AssignationNode)
    def visit(self, node: AssignationNode, scope: Scope):
        body = iterabilizate(node.body)
        value = None
        for exp in body:
            value = self.visit(exp, scope)
        
        scope.create_variable(node.id, value)


    
    @visitor.when(DestructiveAssignationNode)
    def visit(self, node: DestructiveAssignationNode, scope: Scope):
        # if is self assign is at the same way
        var_name = node.id

        body = iterabilizate(node.body)
        var_value = None
        for exp in body:
            var_value = self.visit(exp, scope)

        scope.edit_variable(var_name, var_value)
        

    @visitor.when(IfElseNode)
    def visit(self, node: IfElseNode, scope: Scope):
        principal_condition_value = self.visit(scope)
        if principal_condition_value:
            then_value = self.visit(node.then_expr, scope)
            return then_value
        for i in node.elif_list:
            elif_value = self.visit(node.elif_list[i], scope)
            if elif_value is not None:
                return elif_value
        else_value = self.visit(node.else_expr)
        return else_value

    

    @visitor.when(ElifNode)
    def visit(self, node: ElifNode, scope: Scope):
        elif_condition = self.visit(node.condition)
        if elif_condition:
            then_value = self.visit(node.then_expr, scope)
            return then_value
        return None
    

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        condition_value = self.visit(node.condition, scope)
        body_value = None
        while condition_value:
            body_value = self.visit(node.body, scope)
            condition_value = self.visit(node.condition, scope)
        return body_value
    

    @visitor.when(ForNode)
    def visit(self, node: ForNode, scope: Scope):
        iterable = self.visit(node.iterable, scope)
        
        body_scope = Scope(scope)

        return_value = None
        first = True
        for i in iterable:
            if first:
                body_scope.create_variable(node.id, i)
                first=False
            else:
                body_scope.edit_variable(node.id, i)

            body = iterabilizate(node.body)
            value = None
            for exp in body:
                value = self.visit(exp, body_scope)
            
            return_value = value

        return return_value


    @visitor.when(RangeNode)
    def visit(self, node: RangeNode, scope: Scope):
        return range(node.start, node.end)
     
    
    @visitor.when(PrintNode)
    def visit(self, node: PrintNode, scope: Scope):
        value = str(self.visit(node.expr, scope))
        print(value)
        return value
    

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
    def visit(self, node: SelfCallPropNode, scope: Scope):
        pass
        

    @visitor.when(SelfCallFuncNode)
    def visit(self, node: SelfCallFuncNode, scope: Scope):
        pass


    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode, scope: Scope):
        pass

    
    @visitor.when(AsNode)
    def visit(self, node: AsNode, scope: Scope):
        pass

    @visitor.when(IsNode)
    def visit(self, node: IsNode, scope: Scope):
        pass
    

    @visitor.when(NumNode)
    def visit(self, node, scope: Scope):
        # previous analysis to return correct type (idk if it's relevant)
        float_repr = float(node.token) 
        int_repr = int(node.token)
        return float_repr if float_repr - int_repr != 0 else int_repr
    
    
    @visitor.when(StringNode)
    def visit(self, node, scope: Scope):
        return str(node.token)
    

    @visitor.when(BoolNode)
    def visit(self, node, scope: Scope):
        return bool(node.token)

    @visitor.when(VarNode)
    def visit(self, node: VarNode, scope: Scope):
        return scope.get_variable(node.token)


    @visitor.when(RanNode)
    def visit(self, node, scope: Scope):
        return random.uniform(0.0,1.0)
    

    @visitor.when(UnaryNumOperationNode)
    def visit(self, node: UnaryNumOperationNode, scope: Scope):
        arg_value = self.visit(node.expr,scope)
        if node.token == 'sin':
            return math.sin(arg_value)
        elif node.token == 'cos':
            return math.cos(arg_value)
        elif node.token == 'sqrt':
            return math.sqrt(arg_value,2)
        elif node.token == 'exp':
            return math.exp(arg_value)
        else: 
            raise Exception(f'Operation {node.token} is invalid.')

    
    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope: Scope):
        value_expr = self.visit(node.expr, scope)
        return not value_expr 
    

    @visitor.when(BinaryNumOperationNode)
    def visit(self, node: BinaryNumOperationNode, scope: Scope):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
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
        elif node.token == 'log':
            return math.log(left, right)
        else:
            raise Exception(f'Operator {node.token} is invalid')
            # never raise this exception
        
    
    @visitor.when(BinaryStringOperationNode)
    def visit(self, node: BinaryStringOperationNode, scope: Scope):
        right_value = self.visit(node.right, scope)
        left_value = self.visit(node.left, scope)
        if node.token == '@':
            return str(right_value) + str(left_value)
        elif node.token == '@@':
            return str(right_value) + ' ' + str(left_value)
        else: 
            raise Exception(f'Operator {node.token} is invalid')
    

    @visitor.when(AndOrNode)
    def visit(self, node, scope: Scope):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value or right_value if node.token == '&' else left_value and right_value
    

    @visitor.when(EqualDiffNode)
    def visit(self, node, scope: Scope):
        # no me queda clara la separación esta por qué
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        if node.token == '==':
            return left_value == right_value
        elif node.token == '!=':
            return left_value != right_value
        else:
            raise Exception(f'Operator {node.token} is invalid')
    

    @visitor.when(ComparisonNode)
    def visit(self, node, scope: Scope):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
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
            


        