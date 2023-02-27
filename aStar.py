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
            if child in closed:
                continue
            elif child in opened and child.g < opened[opened.index(child)].g:
                index = opened.index(child)
                del opened[index]
            heapq.heappush(opened, child)

    return None
