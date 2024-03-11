from grammar.grammar import Grammar
from SLR1_Parser import SLR1_Parser
from ContainerSet import ContainerSet
from Item import Item
from automata import State
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

        # Write automaton
        dot_graph = NFA.graph().write("nfa.dot", format='raw', encoding='utf-8')

        # Convert to FDA LR(0) automaton
        DFA = NFA.to_deterministic()
        self.DFA = DFA

        # Write automaton
        DFA.graph().write("dfa.dot", format='raw', encoding='utf-8')

        
    def build_SLR1(self):
        """
        Build and return the SLR(1) parser object.

        Returns:
        - Parser: The generated SLR(1) parser object.
        """


        parser = SLR1_Parser()
        return parser


@staticmethod
def __compute_firsts(G: Grammar):
    """
    Compute the First sets for the given grammar.

    Parameters:
    - G: The grammar for which First sets are to be computed.

    Returns:
    - dict: A dictionary containing the computed First sets for terminals, non-terminals, and sentences.
    """
    firsts = {}
    change = True
    
    # init First(Vt)
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
        
    # init First(Vn)
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            # get current First(X)
            first_X = firsts[X]
                
            # init First(alpha)
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
            
            # CurrentFirst(alpha)???
            local_first = __compute_local_first(firsts, alpha)
            
            # update First(X) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
                    
    # First(Vt) + First(Vt) + First(RightSides)
    with open('firsts.txt', 'w') as file:
        file.write("Non Terminals:\n")
        for key, value in firsts.items():
            if isinstance(key, NonTerminal):
                file.write(f"{key}: {value}\n")

        file.write("\nSentences:\n")
        for key, value in firsts.items():
            if isinstance(key, Sentence):
                file.write(f"{key}: {value}\n")

    return firsts

@staticmethod
def __compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()
    
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    if alpha_is_epsilon:
        first_alpha.set_epsilon(True)
    else:
        # First(X0) in First(alpha)
        first_alpha.update(firsts[alpha._symbols[0]])

        # First(Xi) in First(alpha) if \forall j<i Xj.contains_epsilon
        i = 0
        Xi = alpha._symbols[i]
        while firsts[Xi].contains_epsilon:
            if i == len(alpha._symbols):
                first_alpha.set_epsilon()
                break
            i += 1
            Xi = alpha._symbols[i]
            if not firsts[Xi].contains_epsilon:
                first_alpha.update(firsts[Xi])  
                break 
    
    return first_alpha
