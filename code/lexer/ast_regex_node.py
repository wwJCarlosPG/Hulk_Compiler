import os
import sys
current_route = os.path.dirname(os.path.abspath(__file__))
prev_route = os.path.join(current_route, "..", "lexer")
sys.path.append(prev_route)
from ast_node import AtomicNode, UnaryNode, BinaryNode
from automata_work import NFA
from automaton_operations import *
EPSILON = 'ε'

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
    
# class ComplementNode(UnaryNode):
#     @staticmethod
#     def operate(value):
#         return automata_complement(value)

#search how to implement this    
class SquareBracketNode(UnaryNode):
    @staticmethod
    def operate(value):
        pass