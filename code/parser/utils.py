from ContainerSet import ContainerSet
from Item import Item
from automata import State
from grammar.grammar import Grammar
from definitions import NonTerminal, Sentence

def compute_firsts(G: Grammar):
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


def compute_follows(G: Grammar, firsts):
    """
    Compute the Follow sets for the given grammar using the computed First sets.

    Parameters:
    - G: The grammar for which Follow sets are to be computed.
    - firsts: The precomputed First sets for terminals, non-terminals, and sentences.

    Returns:
    - dict: A dictionary containing the computed Follow sets for non-terminals.
    """
    follows = { }
    change = True
    
    # init Follow(Vn)
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            follow_X = follows[X]
            
            if not alpha.IsEpsilon:
                len_alpha = len(alpha._symbols)

                for i in range(len_alpha):
                    Y = alpha._symbols[i]
                    try:
                        beta = alpha._symbols[i+1]
                    except:
                        beta = None

                    if Y.IsNonTerminal and beta:
                        # First(beta) - { epsilon } subset of Follow(Y)
                        change |= follows[Y].update(firsts[beta])

                        # beta ->* epsilon ? Follow(X) subset of Follow(Y)
                        if firsts[beta].contains_epsilon:
                            change |= follows[Y].update(follow_X)

                    # X -> zY ? Follow(X) subset of Follow(Y)
                    if i == len_alpha-1 and Y.IsNonTerminal:
                        change |= follows[Y].update(follow_X)

    with open('follows.txt', 'w') as file:
        for key, value in follows.items():
            file.write(f"{key}: {value}\n")

    return follows



def build_LR0_automaton(G: Grammar):
    """
    Build the LR(0) automaton for the given augmented grammar.

    Parameters:
    - G (Grammar): An augmented grammar.

    Returns:
    - State: The initial state of the LR(0) automaton.
    
    Raises:
    - AssertionError: If the grammar does not meet the required conditions (single start symbol production and augmented grammar).
    """
    assert len(G.startSymbol.productions) == 1 and G.IsAugmentedGrammar, 'Grammar must be augmented'

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0)

    automaton = State(start_item, final=True)

    pending = [ start_item ]
    # Contains for each Item, the corresponding State
    visited = { start_item: automaton }

    while pending:
        current_item = pending.pop()
        if current_item.IsReduceItem:
            continue
        
        next_symbol = current_item.NextSymbol
        next_item = current_item.NextItem()

        # Transitions with next symbol
        if next_symbol:
            current_state = visited[current_item]

            # ~~~~~~~~~~~~~~ Explicit transition ~~~~~~~~~~~~~~
            if not next_item in visited:
                pending.append(next_item)
                visited[next_item] = State(next_item, final=True)

            # (E -> .T+E) -T-> (E -> T.+E)
            # (E -> T.+E) -+-> (E -> T+.E)
            dest_state = visited[next_item]
            current_state.add_transition(next_symbol.Name, dest_state)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


            # ~~~~~~~~~~~~~~~ Epsilon transition ~~~~~~~~~~~~~~~
            if next_symbol.IsNonTerminal:
                epsilon_destination_productions = [p for p in G.Productions if p.Left == next_symbol]
                epsilon_destination_items = [Item(p, 0) for p in epsilon_destination_productions]

                for dest_item in epsilon_destination_items:
                    if not dest_item in visited:
                        pending.append(dest_item)
                        visited[dest_item] = State(dest_item, final=True)
                    
                    # (E -> .T+E) -e-> (T -> .alpha)
                    dest_state = visited[dest_item]
                    current_state.add_epsilon_transition(dest_state)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
    return automaton