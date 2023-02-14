import math
# Heuristic function - returns the Euclidean distance between two tiles
def heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            tile = state[i][j]
            if tile != 0:
                goal_i, goal_j = (tile - 1) // 3, (tile - 1) % 3
                distance += math.sqrt((i - goal_i) ** 2 + (j - goal_j) ** 2)
    return distance