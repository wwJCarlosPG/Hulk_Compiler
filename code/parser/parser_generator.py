from grammar.grammar import Grammar
from SLR1_Parser import SLR1_Parser
from ContainerSet import ContainerSet
from Item import Item
from automata import State, lr0_formatter
from definitions import NonTerminal, Sentence
from utils import compute_firsts, compute_follows, build_LR0_automaton


class Parser_Generator():
    def __init__(self, G: Grammar):
        """
        Initialize the ParserGenerator from a Grammar G.

        Attributes:

        Example:
        ```
        parser_gen = ParserGenerator()
        parser = parser_gen.build_parser()
        ```
        """
        self.grammar = G

        computed_firsts = compute_firsts(G)

        self.firsts = computed_firsts
        self.follows = compute_follows(G, computed_firsts)

        # Extend Grammar with S'-> E
        GG = G.AugmentedGrammar()

        # Build NFA LR(0) automaton
        NFA = build_LR0_automaton(GG)

        # Convert to FDA LR(0) automaton
        DFA = NFA.to_deterministic(lr0_formatter)
        self.DFA = DFA

        # Write automatons
        NFA.graph().write("nfa.dot", format='raw', encoding='utf-8')
        DFA.graph().write("dfa.dot", format='raw', encoding='utf-8')

        
    def build_SLR1(self):
        """
        Build and return the SLR(1) parser object.

        Returns:
        - Parser: The generated SLR(1) parser object.
        """
        parser = SLR1_Parser(self.DFA)
        return parser
