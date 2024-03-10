from ContainerSet import ContainerSet
from definitions import NonTerminal

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