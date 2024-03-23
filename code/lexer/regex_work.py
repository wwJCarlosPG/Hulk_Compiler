from cmp.utils import Token
from grammar.test_grammar import G
from cmp.tools.parsing import metodo_predictivo_no_recursivo
from cmp.tools.evaluation import evaluate_parse
from automaton_minimization import automata_minimization #este es el mío que da error
from cmp.tools.automata import automata_minimization
from automata_work import nfa_to_dfa

def regex_tokenizer(text, G, skip_whitespaces=True): #retorna los tokens de las expresiones regulares
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
    fixed_tokens = { lex: Token(lex, G[lex]) for lex in '| * ( ) ε'.split() }
    special_char = False
    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        elif special_char:
            token = Token(char, G['symbol'])
            special_char = False            
        elif char == '\\':
            special_char = True
            continue 
        else:
            try:
                token = fixed_tokens[char]
            except:
                token = Token(char, G['symbol'])
        tokens.append(token)        
    tokens.append(Token('$', G.EOF))
    return tokens



def regex_automaton(regex):
     """
    Constructs the automaton for a given regular expression.
    
    Args:
        regex (str): The regular expression.
    
    Returns:
        Automaton: The minimized deterministic finite automaton (DFA) representing the regular expression.
    """
    # This parser needs to be a global variable because it is shared across the grammar.
     parser = metodo_predictivo_no_recursivo(G)
     regex_tokens = regex_tokenizer(regex,G)
     regex_parser = parser(regex_tokens)
     regex_ast = evaluate_parse(regex_parser,regex_tokens)
     regex_nfa = regex_ast.evaluate()
     return automata_minimization(nfa_to_dfa(regex_nfa))
