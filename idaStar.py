import possibleMoves

# IDA* search algorithm
def ida_star(start_state, goal_state, heuristic_fn):
    threshold = heuristic_fn(start_state)
    while True:
        result, new_threshold = search(start_state, goal_state, 0, threshold, heuristic_fn)
        if result == "FOUND":
            return int(threshold)
        if result == float("inf"):
            return "NOT FOUND"
        threshold = new_threshold

def search(state, goal_state, g, threshold, heuristic_fn):
    f = g + heuristic_fn(state)
    if f > threshold:
        return float("inf"), f
    if state == goal_state:
        return "FOUND", f
    min_threshold = float("inf")
    for move in possibleMoves.get_moves(state):
        result, new_threshold = search(move, goal_state, g+1, threshold, heuristic_fn)
        if result == "FOUND":
            return "FOUND", f
        if result != float("inf") and new_threshold < min_threshold:
            min_threshold = new_threshold
    return min_threshold, float("inf")
