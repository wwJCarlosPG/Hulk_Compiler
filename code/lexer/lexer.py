import sys
sys.path.append('code/lexer')
sys.path.append('code/parser/grammar')
sys.path.append('code/parser')
from ast_regex_node import *
from regex_work import regex_automaton
from utils import State, Token

class Lexer:
    def __init__(self, table, eof):
        """
        Initializes the Lexer object.

        Args:
            table (list): A list of tuples containing token types and corresponding regular expressions.
            eof (str): The end-of-file marker.
        """
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton() 

    def _build_regexs(self, table):
        """
        Builds the regular expressions for each token type.

        Args:
            table (list): A list of tuples containing token types and corresponding regular expressions.

        Returns:
            list: A list of automata representing the regular expressions for each token type.
        """
        regexs = []
        for n, (token_type, regex) in enumerate(table):            
            automaton = regex_automaton(regex)           
            automaton = State.from_nfa(automaton)   
            for state in automaton:
                if state.final:
                    state.tag = (token_type,n)
            regexs.append(automaton)
        return regexs    
    
    def _build_automaton(self):
        """
        Builds the automaton from the regular expressions.

        Returns:
            State: The start state of the deterministic finite automaton (DFA).
        """
        start = State('start')
        for automaton in self.regexs:
            start.add_epsilon_transition(automaton) 
        return start.to_deterministic()       
    
    def _walk(self, string):
        """
        Performs a walk through the automaton.

        Args:
            string (str): The input string to tokenize.

        Returns:
            tuple: A tuple containing the final state and the lexeme.
        """
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''        
        for symbol in string:    
            try:
                state = state[symbol][0] 
                lex = lex + symbol
            except TypeError:
                break       
        final = state                    
        final.tag = (None, float('inf'))
        for state in final.state:
            if state.final and state.tag[1] < final.tag[1]:
                final.tag = state.tag
        final_lex = lex          
        return final, final_lex    
    
    def _tokenize(self, text: str, skip_whitespaces=True):
        """
        Tokenizes the input text.

        Args:
            text (str): The input text to tokenize.
            skip_whitespaces (bool, optional): Whether to skip whitespaces. Defaults to True.

        Yields:
            tuple: A tuple containing the lexeme and its corresponding token type.
        """
        remaining_text = text
        while True:
            x = 0
            if skip_whitespaces and remaining_text[0].isspace():     
                remaining_text = remaining_text[1:]
                continue                
            final_state, final_lex = self._walk(remaining_text)
            if final_lex == '':
                yield text.rsplit(remaining_text)[0], final_state.tag[0]
                return            
            yield final_lex, final_state.tag[0] 
            remaining_text = remaining_text.replace(final_lex,'',1)
            if remaining_text == '':
                break        
        yield '$', self.eof    
    
    def __call__(self, text, skip_whitespaces=True):
        """
        Calls the Lexer object to tokenize the input text.

        Args:
            text (str): The input text to tokenize.
            skip_whitespaces (bool, optional): Whether to skip whitespaces. Defaults to True.

        Returns:
            list: A list of Token objects representing the tokens in the input text.
        """
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text, skip_whitespaces) ]


