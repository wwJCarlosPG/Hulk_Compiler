from automata import State, lr0_formatter
from ShiftReduceParser import ShiftReduceParser

    
from utils import build_LR0_automaton, compute_firsts, compute_follows

class SLR1Parser(ShiftReduceParser):
    # self.grammar
    # self.verbose
    # self.action
    # self.goto
    # self._build_parsing_table

    def _build_parsing_table(self):

        G = self.grammar.AugmentedGrammar(True)
        
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)
        
        # Build NFA LR(0) automaton
        NFA = build_LR0_automaton(G)

        # Convert to FDA LR(0) automaton
        DFA = NFA.to_deterministic(lr0_formatter)

        # Write automatons
        NFA.graph().write("nfa.dot", format='raw', encoding='utf-8')
        DFA.graph().write("dfa.dot", format='raw', encoding='utf-8')


        for i, node in enumerate(DFA):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in DFA:
            idx = node.idx
            for state in node.state:
                item = state.state
                # Your code here!!!
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
    
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value