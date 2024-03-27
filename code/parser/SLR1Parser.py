from cmp.automata import State, lr0_formatter
from parser.ShiftReduceParser import ShiftReduceParser

    
from parser.utils import build_LR0_automaton, compute_firsts, compute_follows

class SLR1Parser(ShiftReduceParser):
    """
    SLR(1) Parser implementation, a type of LR parser that uses lookahead of one symbol.
    """
    # self.grammar
    # self.verbose
    # self.action
    # self.goto
    # self._build_parsing_table
    
    def _build_parsing_table(self):
        """
        Build the parsing table for SLR(1) parser.
        """

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
                lr0_item = state.state

                next_symbol = lr0_item.NextSymbol

                # S -> alpha
                item_production = lr0_item.production
                S = item_production.Left

                if lr0_item.IsReduceItem:

                    # Augmented symbol production, OK case
                    if S == G.startSymbol:
                        # (S' -> S.)
                        self._register(self.action, (idx, G.EOF), (self.OK, None))

                    # Reduce item REDUCE case
                    else:
                        # (S -> wxv.)
                        production_index = G.Productions.index(item_production)
                        for follower in follows[S]:
                            self._register(self.action, (idx, follower), (self.REDUCE, production_index))
                            
                else:
                    # Transition SHIFT case:
                    if next_symbol:
                        dest_index = node.transitions[next_symbol.Name][0].idx
                        if next_symbol.IsTerminal:
                            # (S -> w.xv)
                            self._register(self.action, (idx, next_symbol), (self.SHIFT, dest_index))
                        if next_symbol.IsNonTerminal:
                            # (S -> w.Xv)
                            self._register(self.goto, (idx, next_symbol), dest_index)

    
    @staticmethod
    def _register(table, key, value):
        """
        Helper method to register values into the parsing tables.
        
        Args:
            table (dict): The ACTION or GOTO table.
            key: The key for the table.
            value: The value to store.
        """
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value