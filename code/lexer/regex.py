from cmp.utils import Token
from grammar.regex_grammar import G, symbol
from cmp.tools.parsing import metodo_predictivo_no_recursivo
from cmp.evaluation import evaluate_reverse_parse
from lexer.automata import nfa_to_dfa, automata_minimization
from parser.SLR1Parser import SLR1Parser

parser = SLR1Parser(G) 
class Regex():
    def __init__(self, exp):
        self.exp = exp
        self.automaton = self.regex_automaton()
        pass
    
    def regex_tokenizer(self): 
        """
        Tokenizes the regular expressions.
        
        Args:
            text (str): The text to tokenize.
            G (dict): The grammar containing token definitions.
            skip_whitespaces (bool, optional): Whether to skip whitespaces. Defaults to True.
        
        Returns:
            list: List of tokens representing the regular expression.
        """
        tokens = []

        fixed_tokens = {lex: Token(lex,G[lex]) for lex in '| * + - ? ( ) [ ] symbol ε'.split()}
    
        is_symbol_set = is_escape = False    
        text = self.exp
        for char in text:

            if is_escape:
                token = Token(char, symbol)

                tokens.append(token)
                is_escape = False
                continue

            if char == ']':
                is_symbol_set = False            
            elif is_symbol_set:
                if char != '-':
                    tokens.append(Token(char, symbol))
                    continue
            elif char == '[':
                is_symbol_set = True
            elif char == '\\':
                is_escape = True
                continue

            try:
                token = fixed_tokens[char]
            except KeyError:
                token = Token(char, symbol)
            tokens.append(token)                 
            

        tokens.append(Token('$', G.EOF))
        return tokens
    



    def regex_automaton(self):
        """
        Constructs the automaton for a given regular expression.
        
        Args:
            regex (str): The regular expression.
        
        Returns:
            Automaton: The deterministic finite automaton (DFA) representing the regular expression.
        """
        regex_tokens = self.regex_tokenizer()
        token_types = [t.token_type for t in regex_tokens]
        parse, oper = parser(token_types)
        regex_ast = evaluate_reverse_parse(parse, oper, regex_tokens)
        regex_nfa = regex_ast.evaluate()
        return automata_minimization(nfa_to_dfa(regex_nfa))
        
    