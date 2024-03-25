import cmp.visitor as visitor 
from cmp.semantic import ErrorType, VoidType, IntType, StringType, BoolType
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
        self.context.types['number'] = IntType() 
        self.context.types['string'] = StringType() 
        self.context.types['bool'] = BoolType() 
        self.context.types['void'] = VoidType()
        self.context.types['error'] = ErrorType()
        for statement in node.statement_seq:
            self.visit(statement)
        
    @visitor.when(TypeDefNode)
    def visit(self, node: TypeDefNode):
        try:
            self.context.create_type(node.id.lex)   
        except SemanticError as ex:
            self.errors.append(ex.text)