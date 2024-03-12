from grammar.grammar import Grammar


class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G: Grammar, verbose=False):
        self.grammar = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [ 0 ]
        cursor = 0
        output = []
        
        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, '<---||--->', w[cursor:])
                
            if (state, lookahead) not in self.action:
                raise SyntaxError('Syntax error in Shift-Reduce parser')
            
            action, tag = self.action[state, lookahead]
            
            if action == self.SHIFT: # --------------------------- (SHIFT case)
                stack.append(tag)
                # stack.append(lookahead)
                cursor += 1

            elif action == self.REDUCE: # ------------------------ (REDUCE case: S -> alpha)
                production = self.grammar.Productions[tag]
                S, alpha = production.Left, production.Right

                # Do pop alpha size times
                pop_count = len(alpha)
                for _ in range(pop_count): stack.pop()

                # Do push with goto state
                top = stack[-1]
                goto = self.goto[top, S]
                stack.append(goto)

                # Add production to output
                output.append(production)

            elif action == self.OK: # ---------------------------- (OK case)
                break
            else:
                raise SyntaxError('Syntax error in Shift-Reduce parser')

        return output