import copy

# Get the possible moves for the blank space
def get_moves(state):
    moves = []
    blank_i, blank_j = None, None
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                blank_i, blank_j = i, j
                break
        if blank_i is not None:
            break
    if blank_i > 0:
        # Move the tile above the blank space down
        new_state = copy.deepcopy(state)
        new_state[blank_i][blank_j], new_state[blank_i-1][blank_j] = new_state[blank_i-1][blank_j], new_state[blank_i][blank_j]
        moves.append(new_state)
    if blank_i < 2:
        # Move the tile below the blank space up
        new_state = copy.deepcopy(state)
        new_state[blank_i][blank_j], new_state[blank_i+1][blank_j] = new_state[blank_i+1][blank_j], new_state[blank_i][blank_j]
        moves.append(new_state)
    if blank_j > 0:
        # Move the tile to the left of the blank space to the right
        new_state = copy.deepcopy(state)
        new_state[blank_i][blank_j], new_state[blank_i][blank_j-1] = new_state[blank_i][blank_j-1], new_state[blank_i][blank_j]
        moves.append(new_state)
    if blank_j < 2:
        # Move the tile to the right of the blank space to the left
        new_state = copy.deepcopy(state)
        new_state[blank_i][blank_j], new_state[blank_i][blank_j+1] = new_state[blank_i][blank_j+1], new_state[blank_i][blank_j]
        moves.append(new_state)
    return moves