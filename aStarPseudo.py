
import possibleMoves


closed=[]
opened=[]
def main(v,UB=float('inf'),k):
    if cost(v) >= UB:
        return
    closed.append(v)
    for op in possibleMoves.get_moves(v):
        child = op
        if fu(child)>= UB:
            continue
        if isGoal(child):
            UB=fu(child)
        LHB = min(UB,fs(v)+k)
        if (fu(child)<= LHB):
            minCost = lookAhead(child, LHB, UB, float('inf'))
            if minCost>f(child):
                fu(child)



def lookAhead:
