import heapq
from TilePuzzle import *


# A* search algorithm
def a_star(tile_puzzle):
    initial_node = Node(tile_puzzle.start_state, tile_puzzle)
    opened = [initial_node]  # heap
    heapq.heapify(opened)
    closed = set()

    while opened:
        current_node = heapq.heappop(opened)
        if current_node.isFinalState:
            moves = current_node.getPathDirections()
            return len(moves), moves[::-1]
        closed.add(current_node)

        for neighbour in current_node.neighbours:
            child = Node(neighbour, tile_puzzle, parent=current_node, g=current_node.g + 1)  # generateNode(op,v)
        #    if child in closed:
        #        continue
            if child not in opened and child not in closed:  # not visited at all
                heapq.heappush(opened, child)
            elif child in opened and child.g < opened[opened.index(child)].g:
                heapq.heapreplace(opened, child)
            elif child in closed:
                old_child = list(closed)[list(closed).index(child)]
                if (child.g < old_child.g):
                    heapq.heapreplace(opened, child)
    return None
