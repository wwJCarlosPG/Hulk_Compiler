from lexer.automata import NFA
from lexer.automaton_operations import *
from grammar.regex_grammar import G
EPSILON = 'ε'

class Node:
    def evaluate(self):
        raise NotImplementedError()
        
class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, node):
        self.node = node
        
    def evaluate(self):
        value = self.node.evaluate() 
        return self.operate(value)
    
    @staticmethod
    def operate(value):
        raise NotImplementedError()
        
class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def evaluate(self):
        lvalue = self.left.evaluate() 
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)
    
    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()
    

class EpsilonNode(AtomicNode):
    def evaluate(self):
        return NFA(states=2, finals=[1], transitions={(0, ''): [1]})

class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        return NFA(states=2, finals=[1], transitions={(0, s): [1]})

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)
    
class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_union(lvalue, rvalue)
    
class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_concatenation(lvalue, rvalue)
    
class PositiveClosureNode(UnaryNode):
    @staticmethod
    def operate(value: NFA):        
        return NFA.automata_concatenation(value,value.automata_closure())
    
class ZeroOrOneNode(UnaryNode):
    @staticmethod
    def operate(value: NFA):        
        return NFA.automata_union(value,EpsilonNode(G.EOF).evaluate())
    
class RangeNode(Node):
    def __init__(self, first: SymbolNode, last: SymbolNode) -> None:
        self.first = first
        self.last = last

    def evaluate(self):
        value = [self.first]
        for i in range(ord(self.first.lex)+1,ord(self.last.lex)):
            value.append(SymbolNode(chr(i)))
        value.append(self.last)
        return value      
