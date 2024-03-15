import os
import sys
from lexer.ast_node import * 
from lexer.automata_work import NFA
from lexer.automaton_operations import *

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
    
class ComplementNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_complement(value)