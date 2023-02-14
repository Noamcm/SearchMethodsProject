import heapq
import possibleMoves

# A* search algorithm
def a_star(start_state, goal_state,heuristic_fn):
    heap = [(0, start_state)]
    visited = set()
    g = {str(start_state): 0}
    while heap:
        f, state = heapq.heappop(heap)
        if state == goal_state:
            return g[str(state)]
        visited.add(str(state))
        possibleMove = possibleMoves.get_moves(state)
        for move in possibleMove:
            new_g = g[str(state)] + 1
            if str(move) not in visited or new_g < g[str(move)]:
                g[str(move)] = new_g
                heapq.heappush(heap, (new_g + heuristic_fn(move), move))
    return "NOT FOUND"
