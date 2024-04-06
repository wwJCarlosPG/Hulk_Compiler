from cmp.pycompiler import Grammar
from parser.utils import is_in_vocabulary

class ShiftReduceParser:
    """An abstract shift-reduce parser implementation."""

    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G: Grammar, verbose=False):
        """
        Initialize the Shift-Reduce Parser.

        Args:
            G (Grammar): The grammar for the parser.
            verbose (bool): Whether to print verbose output during parsing.
        """
        self.grammar = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        """Build the parsing table for the parser."""
        raise NotImplementedError()

    def __call__(self, tokens):
        """
        Parse the input sequence using shift-reduce parsing.

        Args:
            w (list): The input sequence to parse.

        Returns:
            list: The list of productions used for parsing.
        """
        try:
            w = [token.token_type for token in tokens]
            _ = is_in_vocabulary(tokens)
        except AttributeError:
            w = tokens
            
        
        stack = [ 0 ]
        cursor = 0
        output = []
        operations = []
        
        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, '<---||--->', w[cursor:])
                
            if (state, lookahead) not in self.action:
                snnipet = self.__getSnnipet__([t.lex for t in tokens], cursor)
                raise SyntaxError(' Symbol not expected:\n' + snnipet)
            
            action, tag = self.action[state, lookahead]
            
            if action == self.SHIFT: # --------------------------- (SHIFT case)
                stack.append(tag)
                operations.append(self.SHIFT)
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
                operations.append(self.REDUCE)

            elif action == self.OK: # ---------------------------- (OK case)
                break
            else:
                raise SyntaxError('Syntax error in Shift-Reduce parser')

        return output, operations

    def __getSnnipet__(self, w, cursor):
        position = cursor

        if cursor < 10:
            start = 0
        else:
            start = cursor - 10
            position = 10

        if cursor + 10 > len(w)-1:
            end = len(w)-1
        else:
            end = cursor + 10

        if cursor == 0:
            position +=1
        if cursor == len(w)-1:
            position -=1
        
        tokens_list = w[start:end]
        sizes = [len(x) for x in tokens_list]
        
        first_line = ''
        seconde_line = ''
        for i in range(len(tokens_list)):
            first_line += tokens_list[i] + ' '
            if i == position:
                seconde_line += ('^' * sizes[i]) + ' '
            else:
                seconde_line += (' ' * sizes[i]) + ' '

    
        return first_line + '\n' + seconde_line