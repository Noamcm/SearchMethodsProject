import heapq
from TilePuzzle import *


best_sol_goal_node = None

def a_star_lookahead(tile_puzzle, k=0, check_lookahead_closed=False):
    global best_sol_goal_node
    UB = float('inf')
    best_sol_goal_node = None
    initial_node = Node(tile_puzzle.start_state, tile_puzzle)    # Create the initial node and priority opened
    opened = [initial_node]
    heapq.heapify(opened)
    closed = set()

    while opened:
        # Get the node with the lowest cost + heuristic ??
        current_node = heapq.heappop(opened)  # input - best node in open list: v
        if current_node.g >= UB:  # 1 # The solution has been found ,return path
            moves = best_sol_goal_node.getPathDirections()
            return len(moves), moves[::-1]  # 2 - halt
        closed.add(current_node)  # 3
        # Generate possible moves and add them to the opened
        for neighbour in current_node.neighbours:  # 4
            child = Node(neighbour, tile_puzzle, parent=current_node, g=current_node.g + 1)  # 5 - generateNode(op,v)
            if child in closed:  # NOT IN ALGORITHM - TO CHECK
                continue
            if child.fu > UB:  # 6
                continue  # 7 - Prune
            if child.isFinalState:  # 8 - goalTest(child)=True
                UB = child.fu  # 8
            LHB = min(UB, current_node.f + k)  # 10 - LHB=lookahead bound
            if child.fu <= LHB:  # 11
                min_cost, UB = lookAhead(tile_puzzle, child, LHB, UB, float('inf'), check_lookahead_closed, closed)  # 12, 13 - lookahead call can update UB  # k
                if min_cost > child.f:  # 14.1
                    child.fu = min_cost  # 14.2
            if child not in opened:  # 15 - duplicateDetection(child)=False
                heapq.heappush(opened, child)  # 16 - Insert child to open list
            else:  # 17
                index = opened.index(child)
                if opened[index] > child:  # 18 - Reorder child in OPEN (if required)
                    del opened[index]
                    heapq.heappush(opened, child)

    # No solution found
    return None, None


def lookAhead(tile_puzzle, v, LHB, UB, min_cost, check_lookahead_closed, closed_list):
    global best_sol_goal_node
    for op in v.neighbours:  # 1
        child = Node(op, tile_puzzle, parent=v, g=v.g + 1)  # 2 - generateNode(op, v)
        if child.isFinalState:  # 3 - goalTest(child)=True    TODO: check and UB > child.g
            UB = child.g  # 4
            min_cost = min(min_cost, child.fu)  # 5
            best_sol_goal_node = child
        elif check_lookahead_closed and child in closed_list:
            return min_cost, UB
        else:  # 6
            if child.fu >= LHB:  # 7
                min_cost = min(min_cost, child.fu)  # 8
            else:  # 9
                lookahead_cost, UB = lookAhead(tile_puzzle, child, LHB, UB, min_cost, check_lookahead_closed, closed_list)  # 10 - recursive call
                min_cost = min(min_cost, lookahead_cost)  # 10 - get the minimum
    return min_cost, UB
