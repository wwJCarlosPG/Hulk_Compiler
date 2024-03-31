import cmp.visitor as visitor
from parser.ast_nodes import ProgramNode, TypeDefNode, TypePropDefNode, TypeFuncDefNode
from cmp.semantic import SemanticError, Type
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

        graph = build_graph(type_def_nodes)

        # if there are user defined types
        if len(type_def_nodes) > 0:
            if check_cycles(graph):
                self.errors.append(SemanticError("Circular inheritance detected"))
            else:
                # check method signature
                for item in type_def_nodes:
                    current_type = self.context.get_type(item.id)

                    if item.parent:
                        parent_type: Type = self.context.get_type(item.parent)

                        # parent defined
                        if parent_type in self.visited:

                            # get methods 
                            current_type_methods = [method[0] for method in current_type.all_methods()] 
                            parent_type_methods = [method[0] for method in parent_type.all_methods()] 

                            for method in current_type_methods:
                                if method.name in [m.name for m in parent_type_methods]: # method inherited
                                    parent_method = parent_type.get_method(method.name)

                                    if len(method.param_types) == len(parent_method.param_types): # same params length
                                        if(method.return_type.name == parent_method.return_type.name): # same return type
                                            for i in range(len(method.param_types)): # same params types
                                                current_param_type: Type = self.context.get_type(method.param_types[i])
                                                parent_param_type = self.context.get_type(parent_method.param_types[i])

                                                if not current_param_type.conforms_to(parent_param_type):
                                                    self.errors.append(SemanticError(f'{method} method must have same types for parameters in parent ({parent_type.name}) and inheritor ({current_type.name}) types.'))
                                        else:
                                            self.errors.append(SemanticError(f'{method} method must have same return type in parent ({parent_type.name}) and inheritor ({current_type.name}) types.'))
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
                parent_type = self.context.get_type(node.parent)
                self.current_type.set_parent(parent_type)
            except SemanticError as ex:
                self.errors.append(ex)
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
            self.errors.append(ex)


    @visitor.when(TypeFuncDefNode)
    def visit(self, node: TypeFuncDefNode):
        param_names = node.params
        param_types = [self.context.get_type(x.type) for x in node.params]

        try:
            return_type = self.context.get_type(node.return_type)
            self.current_type.define_method(node.id, param_names, param_types, return_type)
        except SemanticError as ex:
            self.errors.append(ex)


def build_graph(statements: List[TypeDefNode]):
    adyacence_list = dict()

    for item in statements:
        if item.parent:
            if item.parent in adyacence_list:
                adyacence_list[item.parent].append(item.id)
            else: 
                adyacence_list[item.parent] = [item.id]

    return adyacence_list


def check_cycles(adyacence_list):
    visited = set()
    queue = []

    for typeDef in list(adyacence_list.keys()):
        if typeDef not in visited: queue.append(typeDef)

        while len(queue) > 0:
            current = queue.pop(0)
            visited.add(current)

            if current in adyacence_list:
                for node in adyacence_list[current]:
                    if node in visited:
                        return True
                    
                    queue.append(node)
        
    return False
