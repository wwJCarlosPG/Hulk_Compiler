import cmp.visitor as visitor
from cmp.semantic import ErrorType, VoidType, NumberType, StringType, BoolType, AnyType, ObjectType
from cmp.semantic import Context
from cmp.semantic import SemanticError
from parser.ast_nodes import ProgramNode, TypeDefNode


class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.context = Context()
        self.context.types['any'] = AnyType()
        self.context.types['number'] = NumberType()
        self.context.types['string'] = StringType()
        self.context.types['bool'] = BoolType()
        self.context.types['object'] = ObjectType()
        self.context.types['error'] = ErrorType()

        self.context.types['any'].set_parent(self.context.types['object'])
        self.context.types['number'].set_parent(self.context.types['object'])
        self.context.types['string'].set_parent(self.context.types['object'])
        self.context.types['bool'].set_parent(self.context.types['object'])

        for statement in node.statement_seq:
            self.visit(statement)

    @visitor.when(TypeDefNode)
    def visit(self, node: TypeDefNode):
        try:
            self.context.create_type(node.id, [p.id for p in node.params], [p.type for p in node.params])

        except SemanticError as ex:
            self.errors.append(ex)