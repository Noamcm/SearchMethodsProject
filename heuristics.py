import math


def euclidean_distance_heuristic(state):
    # Heuristic function - returns the Euclidean distance between two tiles
    distance = 0  # total euclidean distances of all states
    for i in range(3):
        for j in range(3):
            tile = state[i][j]
            if tile != 0:
                goal_i, goal_j = (tile - 1) // 3, (tile - 1) % 3
                distance += math.sqrt((i - goal_i) ** 2 + (j - goal_j) ** 2)
    return distance


def manhattan_distance_heuristic(state):
    distance = 0  # total manhattan distances of all states
    for i in range(3):
        for j in range(3):
            tile = state[i][j]
            if tile != 0:
                goal_i, goal_j = (tile - 1) // 3, (tile - 1) % 3
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance

def empty_heuristic(state):
    return 0
