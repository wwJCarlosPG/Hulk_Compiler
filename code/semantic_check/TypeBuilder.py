import cmp.visitor as visitor
from parser.ast_nodes import ProgramNode, TypeDefNode, TypePropDefNode, TypeFuncDefNode
from cmp.semantic import SemanticError
from typing import List

class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
        self.visited = set()
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        
        # Build all types
        for statement in node.statement_seq:
            self.visit(statement)

        type_def_nodes = [node for node in node.statement_seq if isinstance(node, TypeDefNode)]

        graph, nonEmpty = build_graph(type_def_nodes)

        if nonEmpty:
            if check_cycles(graph):
                self.errors.append(SemanticError("Circular inheritance detected"))
            else:
                # check method signature
                for item in type_def_nodes:
                    current_type = self.context.get_type(item.id)

                    if item.parent:
                        parent_type = self.context.get_type(item.parent.lex)

                        # parent defined
                        if parent_type in self.visited:

                            # get methods 
                            current_type_methods = current_type.all_methods()
                            parent_type_methods = parent_type.all_methods()

                            for method_name in current_type_methods:
                                if method_name in parent_type_methods: # method inherited
                                    current_method = current_type_methods[method_name][0]
                                    parent_method = parent_type_methods[method_name][0]

                                    if len(current_method.param_types) == len(parent_method.param_types):
                                        if(current_method.return_type.name == parent_method.return_type.name):
                                            for i in range(len(current_method.param_types)):
                                                current_param_type = current_method.param_types[i]
                                                parent_param_type = parent_method.param_types[i]

                                                if(current_param_type.name != parent_param_type.name):
                                                    self.errors.append(SemanticError(f'{method_name} method must have same types for parameters in parent ({parent_type.name}) and inheritor ({current_type.name}) types.'))
                                        else:
                                            self.errors.append(SemanticError(f'{method_name} method must have same return type in parent ({parent_type.name}) and inheritor ({current_type.name}) types.'))
                                    else:
                                        self.errors.append(SemanticError(f'Inheritor type ({current_type.name}) must have {len(parent_method.param_types)} paramaters.'))
                        else:
                            self.errors.append(SemanticError(f'Type ({current_type.name}) cannot inherit from a type ({parent_type.name}) that has not been defined yet.'))


    @visitor.when(TypeDefNode)
    def visit(self, node: TypeDefNode):
        self.current_type = self.context.get_type(node.id)
        self.visited.add(self.current_type)

        # Set inheritance
        if node.parent:
            try:
                parent_type = self.context.get_type(node.parent.lex)
                self.current_type.set_parent(parent_type)
            except SemanticError as ex:
                self.errors.append(ex.text)
        else:
            parent_type = self.context.get_type('object')
            self.current_type.set_parent(parent_type)

        for body_item in node.body:
            self.visit(body_item)
            

    @visitor.when(TypePropDefNode)
    def visit(self, node: TypePropDefNode):
        try:
            prop_type = self.context.get_type(node.type)
            self.current_type.define_attribute(node.id, prop_type)
        except SemanticError as ex:
            self.errors.append(ex.text)


    @visitor.when(TypeFuncDefNode)
    def visit(self, node: TypeFuncDefNode):
        param_names = node.params
        param_types = [self.context.get_type(x) for x in node.params_types]

        try:
            return_type = self.context.get_type(node.return_type)
            self.current_type.define_method(node.id, param_names, param_types, return_type)
        except SemanticError as ex:
            self.errors.append(ex.text)


def build_graph(statements: List[TypeDefNode]):
    adyacence_list = dict()
    for item in statements:
        adyacence_list[item.id] = []

    startNode = None
    for item in statements:
        if item.parent:
            if item.id in adyacence_list:
                if not startNode : startNode = item.id
                adyacence_list[item.id].append(item.parent.lex)

    return adyacence_list, startNode != None


def check_cycles(adyacence_list):
    visited = set()
    queue = []

    for typeDef in list(adyacence_list.keys()):
        if typeDef not in visited: queue.append(typeDef)

        while len(queue) > 0:
            current = queue.pop(0)
            visited.add(current)

            for node in adyacence_list[current]:
                if node in visited:
                    return True
                
                queue.append(node)
        
    return False
