from ContainerSet import ContainerSet
from definitions import NonTerminal, Sentence

def compute_firsts(G):
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
            local_first = _compute_local_first(firsts, alpha)
            
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

def _compute_local_first(firsts, alpha):
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


def compute_follows(G, firsts):
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