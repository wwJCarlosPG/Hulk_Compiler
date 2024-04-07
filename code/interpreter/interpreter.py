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
        self.current_props = {}
        self.current_funcs = {}
        self.current_type: TypeDefNode = None
        self.current_func: TypeFuncDefNode = None

    @visitor.on('node')
    def visit(self, node, scope=None):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        program_scope = self.context.scope

        statements = iterabilizate(node.statement_seq)
        for stat in statements:
            self.visit(stat, program_scope)
        
        body = iterabilizate(node.expr)
        expr_value =  self.get_last_value(body, program_scope)
        return expr_value


    @visitor.when(FuncDefNode)
    def visit(self, node: FuncDefNode, scope: Scope):

        def defined_function(scope, *args):
            body_scope = Scope(scope)
            # Add variables for each param
            for i in range(len(node.params)):
                param_name = node.params[i].token
                param_value = args[i]
                body_scope.create_variable(param_name, param_value)

            body = iterabilizate(node.body)
            return_value = self.get_last_value(body, body_scope)
            return return_value

        scope.create_function(node.id, defined_function)


    @visitor.when(TypeDefNode)
    def visit(self, node: TypeDefNode, scope: Scope):
        self.current_type = node
        body_scope = Scope(scope)

        class defined_type:
            def __init__(self, interpreter, *args):
                self.props = {}
                self.funcs = {}
                self.args = list(args)
                self.parent = node.parent

                for i in range(len(node.params)):
                    param_name = node.params[i].token
                    param_value = self.args[i]
                    body_scope.create_variable(param_name, param_value)

                for item in node.body:
                    value = interpreter.visit(item, body_scope) 
                    
                    if item.token == 'typeFuncNode':
                        self.funcs[item.id] = value
                        interpreter.current_funcs[item.id] = value
                    else:
                        self.props[item.id] = value
                        interpreter.current_props[item.id] = value

        self.context.create_type(node.id, defined_type)
        self.current_props = {}
        self.current_funcs = {}
        self.current_type = None
        

    @visitor.when(TypePropDefNode)
    def visit(self, node: TypePropDefNode, scope: Scope):
        body = iterabilizate(node.exp)
        prop_value = self.get_last_value(body, scope)
        return prop_value
        

    @visitor.when(TypeFuncDefNode)
    def visit(self, node: TypeFuncDefNode, scope: Scope):
        self.current_func = node

        def defined_function(scope, *args):
            body_scope = Scope(scope)
            for i in range(len(node.params)):
                param_name = node.params[i]
                param_value = args[i]
                body_scope.create_variable(param_name, param_value)

            body = iterabilizate(node.body)
            return_value = self.get_last_value(body, body_scope)
            return return_value
        
        self.current_func = None
        return defined_function

    
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        child_scope = Scope(scope)

        assignations = iterabilizate(node.assignations)
        for assign in assignations:
            self.visit(assign, child_scope)

        body = iterabilizate(node.body)
        value = self.get_last_value(body, child_scope)
        return value
    

    @visitor.when(AssignationNode)
    def visit(self, node: AssignationNode, scope: Scope):
        body = iterabilizate(node.body)

        value = self.get_last_value(body, scope)
        
        scope.create_variable(node.id, value)


    
    @visitor.when(DestructiveAssignationNode)
    def visit(self, node: DestructiveAssignationNode, scope: Scope):
        # if is self assign is at the same way
        var_name = node.id

        body = iterabilizate(node.body)
        var_value = self.get_last_value(body, scope)

        scope.edit_variable(var_name, var_value)
        return var_value
        

    @visitor.when(IfElseNode)
    def visit(self, node: IfElseNode, scope: Scope):
        principal_condition_value = self.visit(node.condition, scope)
        principal_body = iterabilizate(node.then_expr)
        
        if principal_condition_value:
            then_scope = Scope(scope)
            then_value = self.get_last_value(principal_body, then_scope)
            return then_value
        
        for i in range(len(node.elif_list)):
            elif_value = self.visit(node.elif_list[i], scope)
            if elif_value is not None:
                return elif_value
            
        else_body = iterabilizate(node.else_expr)
        else_scope = Scope(scope)
        else_value = self.get_last_value(else_body, else_scope)
        return else_value

    

    @visitor.when(ElifNode)
    def visit(self, node: ElifNode, scope: Scope):
        elif_condition = self.visit(node.condition, scope)
        if elif_condition:
            body_scope = Scope(scope)
            then_body = iterabilizate(node.then_expr)
            then_value = self.get_last_value(then_body, body_scope)
            return then_value
        
        return None
    

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        condition_value = self.visit(node.condition, scope)
        body_value = iterabilizate(node.body)
        body_scope = Scope(scope)
        
        final_value = None
        while condition_value:
            final_value = self.get_last_value(body_value, body_scope)
            condition_value = self.visit(node.condition, scope)
        
        return final_value
    

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
            value = self.get_last_value(body, body_scope)
        
            return_value = value

        return return_value


    @visitor.when(RangeNode)
    def visit(self, node: RangeNode, scope: Scope):
        start_value = self.visit(node.start, scope)
        end_value = self.visit(node.end, scope)
        return range(start_value, end_value)
     
    
    @visitor.when(PrintNode)
    def visit(self, node: PrintNode, scope: Scope):
        body = iterabilizate(node.expr)
        value = str(self.get_last_value(body, scope))
        print(value)
        return value
    

    # instance type
    @visitor.when(InstanceNode)
    def visit(self, node: InstanceNode, scope: Scope):
        current_type = self.context.get_type(node.id)

        params = []
        for param in node.params:
            body = iterabilizate(param)
            value = self.get_last_value(body, scope)
            params.append(value)

        params = tuple(params)
        instance = current_type(self, *params)
        return instance


    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope):
        params = []
        for param in node.params:
            body = iterabilizate(param)
            value = self.get_last_value(body, scope)
            params.append(value)
            
        params = tuple(params)
        target_function = scope.get_function(node.id)
        return_value = target_function(scope, *params)
        return return_value


    @visitor.when(TypeFuncCallNode)
    def visit(self, node: TypeFuncCallNode, scope: Scope):
        var = scope.get_variable(node.instance_id)
    
        params = []
        for param in node.params:
            body = iterabilizate(param)
            value = self.get_last_value(body, scope)
            params.append(value)
            
        params = tuple(params)
        target_function = var.funcs[node.func_id]
        return target_function(scope, *params)


    @visitor.when(SelfCallPropNode)
    def visit(self, node: SelfCallPropNode, scope: Scope):
        return self.current_props[node.id]
        

    @visitor.when(SelfCallFuncNode)
    def visit(self, node: SelfCallFuncNode, scope: Scope):
        target_function = self.current_funcs[node.id]

        params = []
        for param in node.params:
            body = iterabilizate(param)
            value = self.get_last_value(body, scope)
            params.append(value)

        params = tuple(params)
        return target_function(scope, *params)


    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode, scope: Scope):
        parent_id = self.current_type.parent
        parent_type = self.context.get_type(parent_id)

        target_function = None
        while(target_function is None):
            try:
                target_function = parent_type.funcs[self.current_func.id]
            except:
                parent_id = parent_type.parent
                parent_type = self.context.get_type(parent_id)
        
        params = []
        for param in node.params:
            body = iterabilizate(param)
            value = self.get_last_value(body, scope)
            params.append(value)

        params = tuple(params)
        return target_function(*params)

    
    @visitor.when(AsNode)
    def visit(self, node: AsNode, scope: Scope):
        pass

    @visitor.when(IsNode)
    def visit(self, node: IsNode, scope: Scope):
        pass
    

    @visitor.when(NumNode)
    def visit(self, node, scope: Scope):
        # previous analysis to return correct type (idk if it's relevant)
        if node.token == 'PI':
            return math.pi
        elif node.token == 'E':
            return math.e
        else:
            float_repr = float(node.token) 
            int_repr = int(node.token)
            return float_repr if float_repr - int_repr != 0 else int_repr
    
    
    @visitor.when(StringNode)
    def visit(self, node, scope: Scope):
        result = ''
        value = node.token
        try:
            if value[0] == '"':
                value = value[1:len(value)-1]
        except:
            pass
        for c in value:
            if c == '\\':
                continue
            else:
                result += c
        return result
    

    @visitor.when(BoolNode)
    def visit(self, node, scope: Scope):
        if node.token == 'false':
            return False
        elif node.token == 'true':
            return True
        else:
            raise Exception(f"Cannot convert {node.token} to boolean type")

    @visitor.when(VarNode)
    def visit(self, node: VarNode, scope: Scope):
        return scope.get_variable(node.token)


    @visitor.when(RanNode)
    def visit(self, node, scope: Scope):
        return random.uniform(0.0,1.0)
    

    @visitor.when(UnaryNumOperationNode)
    def visit(self, node: UnaryNumOperationNode, scope: Scope):
        body = iterabilizate(node.expr)
        arg_value = self.get_last_value(body,scope)
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
        body = iterabilizate(node.expr)
        value_expr = self.get_last_value(body, scope)
        return not value_expr 
    

    @visitor.when(BinaryNumOperationNode)
    def visit(self, node: BinaryNumOperationNode, scope: Scope):
        left_body = iterabilizate(node.left)
        right_body = iterabilizate(node.right)
        
        left = self.get_last_value(left_body, scope)
        right = self.get_last_value(right_body, scope)

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
        left_body = iterabilizate(node.left)
        right_body = iterabilizate(node.right)
        
        left_value = self.get_last_value(left_body, scope)
        right_value = self.get_last_value(right_body, scope)

        if node.token == '@':
            return str(left_value) + str(right_value)
        elif node.token == '@@':
            return str(left_value) + ' ' + str(right_value)
        else: 
            raise Exception(f'Operator {node.token} is invalid')
    

    @visitor.when(AndOrNode)
    def visit(self, node, scope: Scope):
        left_body = iterabilizate(node.left)
        right_body = iterabilizate(node.right)

        left_value = self.get_last_value(left_body, scope)
        right_value = self.get_last_value(right_body, scope)
        return left_value and right_value if node.token == '&' else left_value or right_value
    

    @visitor.when(EqualDiffNode)
    def visit(self, node, scope: Scope):
        left_body = iterabilizate(node.left)
        right_body = iterabilizate(node.right)
        
        left_value = self.get_last_value(left_body, scope)
        right_value = self.get_last_value(right_body, scope)

        if node.token == '==':
            return left_value == right_value
        elif node.token == '!=':
            return left_value != right_value
        else:
            raise Exception(f'Operator {node.token} is invalid')
    

    @visitor.when(ComparisonNode)
    def visit(self, node, scope: Scope):
        left_body = iterabilizate(node.left)
        right_body = iterabilizate(node.right)
        
        left_value = self.get_last_value(left_body, scope)
        right_value = self.get_last_value(right_body, scope)
        
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
            

    # ---------------- #
    # AUXILIAR METHOD  #
    # ---------------- #  
    def get_last_value(self, body, scope):
        return_value = None
        for exp in body:
            return_value = self.visit(exp, scope)
        return return_value