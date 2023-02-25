import copy
import heapq
from TilePuzzle import *


def a_star_lookahead(tile_puzzle, k=0):
    UB = float('inf')

    # Create the initial node and priority opened
    initial_node = Node(tile_puzzle.start_state, tile_puzzle)
    min_cost, UB = lookAhead(tile_puzzle, initial_node, initial_node.F() + k, UB, float('inf'), k)
    if min_cost > initial_node.F():
        initial_node.fu = min_cost
    opened = [initial_node]
    heapq.heapify(opened)
    closed = set()

    while opened:
        # Get the node with the lowest cost + heuristic
        current_node = heapq.heappop(opened)  # input - best node in open list: v
        # print(len(opened))  # 362880
        if current_node.g >= UB:  # 1 #or current_node.state == final_state
            # The solution has been found ,return path
            moves = current_node.getPathDirections()
            return (len(moves),moves[::-1])  # 2 - halt

        closed.add(str(current_node.state))  # 3
        current_node.is_closed = True
        # Generate possible moves and add them to the opened
        for neighbour in current_node.neighbours:  # 4
            child = Node(neighbour, tile_puzzle, parent=current_node, g=current_node.g + 1)  # 5 - generateNode(op,v)
            if str(child.state) in closed:
                continue
            if child.fu >= UB:  # 6
                continue  # 7 - Prune
            if child.state == final_state:  # 8 - goalTest(child)=True
                UB = child.fu  # 8
            LHB = min(UB, current_node.F() + k)  # 10 - LHB=lookahead bound
            if child.fu <= LHB:  # 11
                min_cost, UB = lookAhead(tile_puzzle, child, LHB, UB, float('inf'),
                                         k)  # 12, 13 - lookahead call can update UB
                if min_cost > child.F():  # 14.1
                    child.fu = min_cost  # 14.2
            if child not in opened:  # 15 - duplicateDetection(child)=False
                heapq.heappush(opened, child)  # 16 - Insert child to open list
            else:  # 17
                index = opened.index(child)
                if opened[index] > child:  # 18 - Reorder child in OPEN (if required)
                    heapq.heapreplace(opened, child)
                # heapq.heappush(opened, child)
                #     opened[index] = child
                #     heapq.heapify(opened)

    # No solution found
    return None


def lookAhead(tile_puzzle, v, LHB, UB, min_cost, k, current_level=0):
    if current_level > k:
        return min_cost, UB
    moves = v.get_moves()
    for op in moves:  # 1
        child = Node(op, tile_puzzle, parent=v, g=v.g + 1)  # 2 - generateNode(op, v)
        child.move = v.get_move_direction(child)

        if child.isFinalState:  # 3 - goalTest(child)=True
            UB = child.g  # 4
            min_cost = min(min_cost, child.fu)  # 5
        else:  # 6
            if child.fu >= LHB:  # 7
                min_cost = min(min_cost, child.fu)  # 8
            else:  # 9
                new_min_cost, UB = lookAhead(tile_puzzle, child, LHB, UB, min_cost, k,
                                             current_level + 1)  # 10 - recursive call
                min_cost = min(min_cost, new_min_cost)  # 10 - get the minimum
    return min_cost, UB
