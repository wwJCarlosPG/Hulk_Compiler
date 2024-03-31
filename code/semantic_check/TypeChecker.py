import cmp.visitor as visitor
from parser.ast_nodes import *
from cmp.semantic import SemanticError, Context, VariableInfo, Type, Scope, Method, Attribute
from cmp.semantic import *
from semantic_check.utils import pseudo_graph, Temp, get_graph
WRONG_SIGNATURE = 'Method or Function "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED_PROP = 'Property "%s" is already defined in method "%s".'
LOCAL_ALREADY_DEFINED_FUNC = 'Function "%s" is already defined in scope.'
SCOPE_ALREADY_DEFINED = 'Variable "%s" is already defined in scope.'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
FUNCTION_NOT_DEFINED = 'Function "%s" is not defined in "%s".'
INVALID_OPERATION = 'Operation "%s" is not defined between "%s" and "%s".'

def iterabilizate(body):
    if not isinstance(body, list):
        return [body]
    else:
        return body

class TypeChecker:
    def __init__(self, context, errors=[]):
        self.context: Context = context
        self.current_type: Type = None
        self.current_method: Method = None
        self.errors: list = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, scope=None):
        scope = Scope()
        for statement in node.statement_seq:
            # define functions as variables
            if isinstance(statement, FuncDefNode):
                if not scope.is_local(statement.id):
                    scope.define_variable(statement.id, statement.return_type, is_func=True, params=[x.id for x in statement.params] , params_types=[x.type for x in statement.params])
                else:
                    self.errors.append(SemanticError(LOCAL_ALREADY_DEFINED_FUNC %statement.id))

        for statement in node.statement_seq:
            self.visit(statement, scope)
        
        expr = iterabilizate(node.expr)
        expr_type_name = None
        for item in expr:
            expr_type_name = self.visit(item, scope)

        return expr_type_name


    @visitor.when(FuncDefNode)
    def visit(self, node: FuncDefNode, scope: Scope):
        child_scope = scope.create_child()

        for param in node.params:
            # define params variables
            if not child_scope.is_local(param.id):
                child_scope.define_variable(param.id, param.type)
            else:
                self.errors.append(SemanticError(SCOPE_ALREADY_DEFINED %param.id))
        
        body = iterabilizate(node.body)
        exp_type_name = None

        for exp in body:
           exp_type_name = self.visit(exp, child_scope)
        
        exp_type : Type = self.context.get_type(exp_type_name)

        try:
            node_type = self.context.get_type(node.return_type)
        except SemanticError as e:
            self.errors.append(e)

        if not exp_type.conforms_to(node_type):
            self.errors.append(SemanticError(INCOMPATIBLE_TYPES % (exp_type_name, node.return_type)))


    @visitor.when(TypeDefNode)
    def visit(self, node: TypeDefNode, scope: Scope):
        self.current_type = self.context.get_type(node.id)
        child_scope = scope.create_child()

        for param in node.params:
            # define params variables
            if not child_scope.is_local(param.id):
                child_scope.define_variable(param.id, param.type)
            else:
                self.errors.append(SemanticError(SCOPE_ALREADY_DEFINED %param.id))
        
        for item in node.body:
            self.visit(item, child_scope)

        if node.parent is not None:
            parent = node.parent
            parent_type: Type = self.context.get_type(parent)
            if len(parent_type.params) == len(node.parent_params):
                for i, param in enumerate(node.parent_params):
                    node_parent_param = iterabilizate(param)
                    node_parent_param_name = None
                    for item in node_parent_param:
                        node_parent_param_name=self.visit(item, child_scope)
                    node_parent_param_type: Type = self.context.get_type(node_parent_param_name)
                    parent_param_type: Type = self.context.get_type(parent_type.params_types[i])
                    
                    if not node_parent_param_type.conforms_to(parent_param_type):
                        self.errors.append(SemanticError(f"Types provided in {node_parent_param_type.name} type do not match with expected types"))
                        return 'error' 

            else:
                self.errors.append(SemanticError(f'({parent_type.name}) type initalization must have {len(parent_type.params)} paramaters.'))
                return 'error'

        self.current_type = None
        

    @visitor.when(TypePropDefNode)
    def visit(self, node: TypePropDefNode, scope: Scope):
        # define local properties
        # Semantic errors related to duplicate name were cleared in TypeBuilder

        body = iterabilizate(node.exp)
        exp_type_name = None

        for item in body:
            exp_type_name = self.visit(item, scope)

        exp_type : Type = self.context.get_type(exp_type_name)
        try:
            node_type = self.context.get_type(node.type)
        except SemanticError as e:
            self.errors.append(e)
        
        if not exp_type.conforms_to(node_type):
            self.errors.append(SemanticError(INCOMPATIBLE_TYPES % (exp_type_name, node.type)))
        else: 
            node.type = exp_type_name
            attr: Attribute = self.current_type.get_attribute(node.id)
            attr.type = exp_type
        

    @visitor.when(TypeFuncDefNode)
    def visit(self, node: TypeFuncDefNode, scope: Scope):
        self.current_method : Method = self.current_type.get_method(node.id)
        child_scope: Scope = scope.create_child()

        for p in node.params:
            # define params variables
            # Semantic errors related to duplicate name and method signature were cleared in TypeBuilder
            child_scope.define_variable(p.id, p.type)

        body = iterabilizate(node.body)
        exp_type_name = None

        for item in body:
           exp_type_name = self.visit(item, child_scope)

        exp_type : Type = self.context.get_type(exp_type_name)
        try:
            node_type = self.context.get_type(node.return_type)
        except SemanticError as e:
            self.errors.append(e)

        if not exp_type.conforms_to(node_type):
            self.errors.append(SemanticError(INCOMPATIBLE_TYPES % (exp_type_name, node.return_type)))
        else:
            node.return_type = exp_type_name
            self.current_method.return_type = exp_type_name


        self.current_method = None

    
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        child_scope: Scope = scope.create_child()

        for assig in node.assignations:
            self.visit(assig, child_scope)

            # Redefine variable case
            if child_scope.is_local(assig.id):
                child_scope.redefine_variable(assig.id, assig.type)
            else:
                child_scope.define_variable(assig.id, assig.type)

        body = iterabilizate(node.body)

        let_type_name = None

        for item in body:
            let_type_name = self.visit(item, child_scope)
        
        return let_type_name
    

    @visitor.when(AssignationNode)
    def visit(self, node: AssignationNode, scope: Scope):
        body = iterabilizate(node.body)
        exp_type_name = None

        for item in body:
            exp_type_name = self.visit(item, scope)

        exp_type : Type = self.context.get_type(exp_type_name)

        try:
            node_type = self.context.get_type(node.type)
        except SemanticError as e:
            self.errors.append(e)

        if not exp_type.conforms_to(node_type):
            self.errors.append(SemanticError(INCOMPATIBLE_TYPES % (exp_type_name, node.type)))
        else:
            node.type = exp_type_name

    
    @visitor.when(DestructiveAssignationNode)
    def visit(self, node: DestructiveAssignationNode, scope: Scope):
        body = iterabilizate(node.body)
        exp_type_name = None

        for item in body:
            exp_type_name = self.visit(item, scope)

        is_defined = scope.is_defined(node.id)
        if not is_defined:
            self.errors.append(SemanticError(VARIABLE_NOT_DEFINED % (node.id, 'scope')))
        else:
            scope.redefine_variable(node.id, exp_type_name)
        
        return exp_type_name
        

    @visitor.when(IfElseNode)
    def visit(self, node: IfElseNode, scope: Scope):
        condition = iterabilizate(node.condition)
        condition_type_name = None
        for item in condition:
            condition_type_name = self.visit(item, scope)
        
        if condition_type_name != 'bool':
            self.errors.append(SemanticError('Condition evaluation type must be bool'))
            return 'error'

        then_scope = scope.create_child()
        then_body = iterabilizate(node.then_expr)
        then_type_name = None
        
        for item in then_body:
            then_type_name = self.visit(item, then_scope)

        elif_type_names = []
        for item in node.elif_list:
            elif_type_names.append(self.visit(item, scope))
        
        else_scope = scope.create_child()
        else_body = iterabilizate(node.else_expr)
        else_type_name = None

        for item in else_body:
            else_type_name = self.visit(item, else_scope)
        
        # determinate return type    
        types_list = [Temp(x, self.context.types[x].parent) for x in list(self.context.types.keys())]
        graph = get_graph(types_list)
        x = pseudo_graph(graph)
        type_lca = x.find_LCA([then_type_name, *elif_type_names, else_type_name])
        return type_lca
    

    @visitor.when(ElifNode)
    def visit(self, node: ElifNode, scope: Scope):
        condition = iterabilizate(node.condition)
        condition_type_name = None
        for item in condition:
            condition_type_name = self.visit(item, scope)
        
        if condition_type_name != 'bool':
            self.errors.append(SemanticError('Condition evaluation type must be bool'))
            return 'error'

        elif_scope = scope.create_child()

        body = iterabilizate(node.then_expr)

        exp_type_name = None
        for item in body:
           exp_type_name = self.visit(item, elif_scope)

        return exp_type_name
    

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        condition = iterabilizate(node.condition)
        condition_type_name = None
        for item in condition:
            condition_type_name = self.visit(item, scope)

        if condition_type_name != 'bool':
            self.errors.append(SemanticError('Condition evaluation type must be bool'))
            return 'error'

        child_scope = scope.create_child()

        body = iterabilizate(node.body)

        exp_type_name = None
        for item in body:
            exp_type_name = self.visit(item, child_scope)

        return exp_type_name
    

    @visitor.when(ForNode)
    def visit(self, node: ForNode, scope: Scope):
        child_scope = scope.create_child()
        
        iterable_type = self.visit(node.iterable, scope)
        child_scope.define_variable(node.id, iterable_type)
        
        body = iterabilizate(node.body)

        exp_type_name = None
        for item in body:
            exp_type_name = self.visit(item, child_scope)
        
        return exp_type_name


    @visitor.when(RangeNode)
    def visit(self, node: RangeNode, scope: Scope):
        start = iterabilizate(node.start)
        start_type_name = None
        for item in start:
            start_type_name = self.visit(item, scope)

        end = iterabilizate(node.end)
        end_type_name = None
        for item in end:
            end_type_name = self.visit(item, scope)

        number_type: Type = self.context.get_type('number')
        start_type = self.context.get_type(start_type_name)
        end_type = self.context.get_type(end_type_name)

        if not start_type.conforms_to(number_type):
            self.errors.append(SemanticError(INCOMPATIBLE_TYPES % (start_type_name, 'number')))
            return 'error'

        if not end_type.conforms_to(number_type):
            self.errors.append(SemanticError(INCOMPATIBLE_TYPES % (end_type_name, 'number')))
            return 'error'

        return 'number'       
     
    
    @visitor.when(PrintNode)
    def visit(self, node: PrintNode, scope: Scope):
        body = iterabilizate(node.expr)
        return_type = None
        for item in body:
            return_type = self.visit(item, scope)

        return return_type
    

    # instance type
    @visitor.when(InstanceNode)
    def visit(self, node: InstanceNode, scope: Scope):
        try:
            type: Type = self.context.get_type(node.id)
            # check params length
            if len(node.params) == len(type.params):
                # check params types
                for i in range(len(node.params)):

                    body = iterabilizate(node.params[i])
                    node_param_type_name = None
                    for item in body:
                        node_param_type_name = self.visit(item, scope)

                    node_type: Type = self.context.get_type(node_param_type_name)
                        
                    param_type = self.context.get_type(type.params_types[i])

                    if not node_type.conforms_to(param_type):
                        self.errors.append(SemanticError(f'({type.name}) type initialization must have same types for contructor parameters.'))
                        return 'error'
                    
                return type.name
            else:
                self.errors.append(SemanticError(f'({type.name}) type initalization must have {len(type.params)} paramaters.'))
                return 'error'
        except SemanticError as e:
            self.errors.append(e)
            return 'error'


    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope):
        function_name = node.id

        # check function existence in scope
        if scope.is_defined(function_name):
            try:
                func: VariableInfo = scope.find_variable(function_name)
                if func.is_func:
                    if len(func.params) == len(node.params):
                        for i in range(len(func.params)):

                            body = iterabilizate(node.params[i])
                            node_param_type_name = None
                            for item in body:
                                node_param_type_name = self.visit(item, scope)

                            node_param_type: Type = self.context.get_type(node_param_type_name)
                            func_param_type = self.context.get_type(func.params_types[i])
                            
                            if not node_param_type.conforms_to(func_param_type):
                                self.errors.append(SemanticError(f"Types provided in {func.name} function call do not match with expected types"))
                                return 'error'
                            
                        return func.type
                    else:
                        self.errors.append(SemanticError(f"{len(func.params)} parameters expected for {node.func_id} method"))
                        return 'error'
                else:
                    self.errors.append(SemanticError(f"{function_name} object is not callable"))
                    return 'error'
            except SemanticError as e:
                self.errors.append(e)
                return 'error'
        else:
            self.errors.append(SemanticError(FUNCTION_NOT_DEFINED % (function_name, "scope")))
            return 'error'


    @visitor.when(TypeFuncCallNode)
    def visit(self, node: TypeFuncCallNode, scope: Scope):
        var_name = node.instance_id

        # check variables existence in scope
        if scope.is_defined(var_name):
            var: VariableInfo = scope.find_variable(var_name)
            try:
                # check type existence
                var_type: Type = self.context.get_type(var.type)
                try:
                    method: Method = var_type.get_method(node.func_id)
                    # check params length
                    if len(method.param_names) == len(node.params):
                        # check params types
                        for i in range(len(node.params)):

                            body = iterabilizate(node.params[i])
                            node_param_type_name = None
                            for item in body:
                                node_param_type_name = self.visit(item, scope)

                            node_param_type: Type = self.context.get_type(node_param_type_name)
                            method_param_type = method.param_types[i]


                            if not node_param_type.conforms_to(method_param_type):
                                self.errors.append(SemanticError(f"Types provided in {method.name} function call do not match with expected types"))
                                return 'error'
                            
                        return method.return_type
                        
                    else:
                        self.errors.append(SemanticError(f"{len(method.param_names)} parameters expected for {node.func_id} method"))
                        return 'error'
                except SemanticError as e:
                    self.errors.append(e)
                    return 'error'
            except SemanticError as e:
                self.errors.append(e)
                return 'error'
        else:
            self.errors.append(SemanticError(VARIABLE_NOT_DEFINED % (var_name, "scope")))
            return 'error'


    @visitor.when(SelfCallPropNode)
    def visit(self, node: SelfCallPropNode, scope:Scope):
        try:
            attr: Attribute = self.current_type.get_attribute(node.id)
            return attr.type.name
        except SemanticError as e:
            self.errors.append(e)
            return 'error'
        

    @visitor.when(SelfCallFuncNode)
    def visit(self, node: SelfCallFuncNode, scope:Scope):
        try:
            method: Method = self.current_type.get_method(node.id)
            if len(node.params) == len(method.param_names):
                for i, param in enumerate(node.params):
                    body = iterabilizate(param)
                    param_type_name = None
                    for item in body:
                        param_type_name = self.visit(item, scope)
                    
                    param_type: Type = self.context.get_type(param_type_name)
                    method_param_type = method.param_types[i]

                    if not param_type.conforms_to(method_param_type):
                        self.errors.append(SemanticError(f"Types provided in {method.name} function call do not match with expected types"))
                        return 'error'

                return method.return_type
            else:
                self.errors.append(SemanticError(f"{len(method.param_names)} parameters expected for {node.id} call."))
                
        except SemanticError as e:
            self.errors.append(e)
            return 'error'


    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode, scope):
        method_name = self.current_method.name
        parent = self.current_type.parent

        try:
            parent_method: Method = parent.get_method(method_name)
            if len(node.params) == len(parent_method.param_names):
                for i, param in enumerate(node.params):
                    body = iterabilizate(param)
                    param_type_name = None
                    for item in body:
                        param_type_name = self.visit(item, scope)
                    
                    param_type: Type = self.context.get_type(param_type_name)
                    parent_method_param_type = self.context.get_type(parent_method.param_types[i])

                    if not param_type.conforms_to(parent_method_param_type):
                        self.errors.append(SemanticError(f"Types provided in {parent_method.name} function call do not match with expected types"))
                        return 'error'
                return parent_method.return_type
            else:
                self.errors.append(SemanticError(f"{len(parent_method.param_names)} parameters expected for base method call."))
        except SemanticError as e:
            self.errors.append(e)
            return 'error'

    
    @visitor.when(AsNode)
    def visit(self, node: AsNode, scope: Scope):

        body = iterabilizate(node.expr)
        param_type_name = None
        for item in body:
            param_type_name = self.visit(item, scope)

        param_type: Type = self.context.get_type(param_type_name)
        try:
            node_type = self.context.get_type(node.type)
        except SemanticError as e:
            self.errors.append(e)
            return 'error'
        
        if not node_type.conforms_to(param_type):
            self.errors.append(SemanticError("Cannot downcast %s to %s" % (param_type_name, node.type)))
            return 'error'

        return node.type


    @visitor.when(IsNode)
    def visit(self, node: IsNode, scope: Scope):

        body = iterabilizate(node.expr)
        param_type_name = None
        for item in body:
            param_type_name = self.visit(item, scope)

        param_type: Type = self.context.get_type(param_type_name)
        try:
            node_type = self.context.get_type(node.type)
        except SemanticError as e:
            self.errors.append(e)
            return 'error'

        return 'bool'
    

    @visitor.when(NumNode)
    def visit(self, node, scope):
        return 'number'
    

    @visitor.when(StringNode)
    def visit(self, node, scope):
        return 'string'
    

    @visitor.when(BoolNode)
    def visit(self, node, scope):
        return 'bool'


    @visitor.when(VarNode)
    def visit(self, node: VarNode, scope: Scope):
        var: VariableInfo = scope.find_variable(node.token) 
        if var is None:
            self.errors.append(VARIABLE_NOT_DEFINED % (node.token, "scope"))
            return 'error'
        
        return var.type


    @visitor.when(RanNode)
    def visit(self, node, scope):
        return 'number'
    

    @visitor.when(UnaryNumOperationNode)
    def visit(self, node: UnaryNumOperationNode, scope: Scope):
        body = iterabilizate(node.expr)
        exp_type_name = None
        for item in body:
            exp_type_name = self.visit(item, scope)

        if exp_type_name != 'number':
            self.errors.append(SemanticError(INCOMPATIBLE_TYPES % (exp_type_name, "number")))
            return "error"
        
        return 'number'

    
    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope: Scope):
        body = iterabilizate(node.expr)
        exp_type_name = None
        for item in body:
            exp_type_name = self.visit(item, scope)

        if exp_type_name != 'bool':
            self.errors.append(SemanticError(INCOMPATIBLE_TYPES % (exp_type_name, "bool")))
            return "error"
        
        return 'bool'
    

    @visitor.when(BinaryNumOperationNode)
    def visit(self, node: BinaryNumOperationNode, scope: Scope):
        left_body = iterabilizate(node.left)
        left_type = None
        for item in left_body:
            left_type = self.visit(item, scope)
        
        right_body = iterabilizate(node.right)
        right_type = None
        for item in right_body:
            right_type = self.visit(item, scope)

        if left_type != 'number' or right_type != 'number':
            self.errors.append(INVALID_OPERATION % (node.token, left_type, right_type))
            return 'error'

        return 'number'
    
    @visitor.when(BinaryStringOperationNode)
    def visit(self, node: BinaryStringOperationNode, scope: Scope):
        left_body = iterabilizate(node.left)
        left_type = None
        for item in left_body:
            left_type = self.visit(item, scope)
        
        right_body = iterabilizate(node.right)
        right_type = None
        for item in right_body:
            right_type = self.visit(item, scope)

        basic_types = ['number', 'string', 'bool']
        if left_type not in basic_types or right_type not in basic_types:
            self.errors.append(INVALID_OPERATION % (node.token, left_type, right_type))
            return 'error'

        return 'string'
    

    @visitor.when(AndOrNode)
    def visit(self, node, scope):
        left_body = iterabilizate(node.left)
        left_type = None
        for item in left_body:
            left_type = self.visit(item, scope)
        
        right_body = iterabilizate(node.right)
        right_type = None
        for item in right_body:
            right_type = self.visit(item, scope)

        if left_type != 'bool' or right_type != 'bool':
            self.errors.append(INVALID_OPERATION % (node.token, left_type, right_type))
            return 'error'

        return 'bool'
    

    @visitor.when(EqualDiffNode)
    def visit(self, node, scope):
        left_body = iterabilizate(node.left)
        left_type = None
        for item in left_body:
            left_type = self.visit(item, scope)
        
        right_body = iterabilizate(node.right)
        right_type = None
        for item in right_body:
            right_type = self.visit(item, scope)

        if left_type != right_type:
            self.errors.append(INVALID_OPERATION % (node.token, left_type, right_type))
            return 'error'

        return 'bool'
    

    @visitor.when(ComparisonNode)
    def visit(self, node, scope):
        left_body = iterabilizate(node.left)
        left_type = None
        for item in left_body:
            left_type = self.visit(item, scope)
        
        right_body = iterabilizate(node.right)
        right_type = None
        for item in right_body:
            right_type = self.visit(item, scope)

        if left_type != 'number' or right_type != 'number':
            self.errors.append(INVALID_OPERATION % (node.token, left_type, right_type))
            return 'error'

        return 'bool'
            


        