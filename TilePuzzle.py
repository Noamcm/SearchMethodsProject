import math
import random
import copy


class Node:
    def __init__(self, state, tile_puzzle, parent=None, g=0):
        self.state = state
        self.tile_puzzle = tile_puzzle
        self.parent = parent
        self.move = None
        if parent is not None:
            self.move = parent.get_move_direction(self)
        self.g = g
        self.heuristic = tile_puzzle.heuristic_func(state)
        self.fu = self.heuristic  # self.F()  #float('inf') #
        self.neighbours = self.get_neighbours()
        self.isFinalState = True if self.state == tile_puzzle.final_state else False

    def __lt__(self, other):
        # Used for sorting in the priority opened
        if (self.tile_puzzle.algorithm_name == 'a_star'):
            return self.F() < other.F()
        else:
            return self.fu < other.fu

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return str(self.state).__hash__()

    def F(self):
        return self.g + self.heuristic

    def find_blank(self):
        # Helper function to find the location of the blank tile (0)
        for i in range(self.tile_puzzle.size):
            for j in range(self.tile_puzzle.size):
                if self.state[i][j] == 0:
                    return i, j
        return -1, -1

    def moveState(self, direction):
        # Helper function to make a move in a given direction
        i, j = self.find_blank()
        state = copy.deepcopy(self.state)
        if direction == 'up' and i > 0:
            state[i][j], state[i - 1][j] = self.state[i - 1][j], self.state[i][j]
        elif direction == 'down' and i < self.tile_puzzle.size - 1:
            state[i][j], state[i + 1][j] = self.state[i + 1][j], self.state[i][j]
        elif direction == 'left' and j > 0:
            state[i][j], state[i][j - 1] = self.state[i][j - 1], self.state[i][j]
        elif direction == 'right' and j < self.tile_puzzle.size - 1:
            state[i][j], state[i][j + 1] = self.state[i][j + 1], self.state[i][j]
        return state

    def get_neighbours(self):
        neighbours = []
        for direction in ['up', 'down', 'left', 'right']:
            new_state = self.moveState(direction)
            if new_state != self.state:
                neighbours.append(new_state)
        random.shuffle(neighbours)
        return neighbours

    def get_moves(self):
        # Generate all possible moves from the current node
        moves = []
        i, j = self.find_blank()
        if j > 0 and self.move != 'right':  # left
            move = self.move_blank(i, j, i, j - 1)
            moves.append(move)
        if j < self.tile_puzzle.size - 1 and self.move != 'left':  # right
            move = self.move_blank(i, j, i, j + 1)
            moves.append(move)
        if i > 0 and self.move != 'down':  # up
            move = self.move_blank(i, j, i - 1, j)
            moves.append(move)
        if i < self.tile_puzzle.size - 1 and self.move != 'up':  # down
            move = self.move_blank(i, j, i + 1, j)
            moves.append(move)
        return moves

    def move_blank(self, i1, j1, i2, j2):
        # Move the blank space from (i1, j1) to (i2, j2) and return the new state
        new_state = [row[:] for row in self.state]
        new_state[i1][j1], new_state[i2][j2] = new_state[i2][j2], new_state[i1][j1]
        return new_state

    def get_move_direction(self, new_state):
        # Determine the direction of the move based on the old and new states
        curr_i, curr_j = self.find_blank()
        new_i, new_j = new_state.find_blank()
        if curr_i < new_i:
            return 'down'
        elif curr_i > new_i:
            return 'up'
        elif curr_j < new_j:
            return 'right'
        elif curr_j > new_j:
            return 'left'

    def getPathDirections(self):
        moves = []
        current_node = self
        while current_node.move:
            moves.append(current_node.move)
            current_node = current_node.parent
        return moves


class TilePuzzle:
    def __init__(self, size, difficulty, heuristic_func, algorithm_name):
        self.size = int(math.sqrt(size + 1))
        self.algorithm_name = algorithm_name
        if size == 8:
            self.final_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
            if difficulty == "easy":
                self.start_state = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
            if difficulty == "medium":
                # self.start_state = [[2, 3, 4], [1, 5, 6], [8, 7, 0]]
                #self.start_state = [[0, 1, 2], [5, 6, 3], [4, 7, 8]] #size 8
                #self.start_state = [[0, 2, 3], [1, 4, 6], [7, 5, 8]] #size 4
                self.start_state = [[2, 3, 6], [1, 4, 8], [7, 5, 0]] #size 8
                # self.start_state = [[3,4,2], [1,0,6], [8,5,7]]
                # self.start_state = [[1, 3, 7], [4, 5, 8], [6, 2, 0]]
            if difficulty == "hard":
                self.start_state = [[2, 1, 3], [5, 4, 0], [7, 8, 6]]
            if difficulty == "extreme":
                self.start_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
            if difficulty == "unsolvable":
                self.start_state = [[1, 2, 3], [4, 5, 6], [8, 7, 0]]
        elif size == 15:
            self.final_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
            if difficulty == "easy":
                self.start_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [0, 13, 14, 15]]
            # if difficulty=="medium":
            #     self.start_state = [[2, 3, 4], [1, 5, 6], [8, 7, 0]]
            # if difficulty=="hard":
            #     self.start_state = [[2, 1, 3], [5, 4, 0], [7, 8, 6]]
            # if difficulty=="extreme":
            #     self.start_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

        if heuristic_func == "manhattan":
            self.heuristic_func = self.manhattan_distance_heuristic
        if heuristic_func == "hamming":
            self.heuristic_func = self.hamming_distance_heuristic
        if heuristic_func == "max":
            self.heuristic_func = self.max_heuristic
        if heuristic_func == "euclidean":
            self.heuristic_func = self.euclidean_distance_heuristic
        if heuristic_func == "empty":
            self.heuristic_func = self.empty_heuristic

    def euclidean_distance_heuristic(self, state):
        # Heuristic function - returns the Euclidean distance between two tiles
        distance = 0  # total euclidean distances of all states
        for i in range(self.size):
            for j in range(self.size):
                value = state[i][j]
                if value != 0:
                    row = (value - 1) // self.size
                    col = (value - 1) % self.size
                    distance += math.sqrt((i - row) ** 2 + (j - col) ** 2)
        return distance

    def manhattan_distance_heuristic(self, state):
        # distance = 0  # total manhattan distances of all states
        # for i in range(self.size):
        #     for j in range(self.size):
        #         value = state[i][j]
        #         if value != 0:
        #             row = (value - 1) // self.size
        #             col = (value - 1) % self.size
        #             distance += abs(row - i) + abs(col - j)
        start = [num for sublist in state for num in sublist]
        goal = [num for sublist in  self.final_state for num in sublist]
        distance = sum(abs(b % 3 - g % 3) + abs(b // 3 - g // 3) for b, g in ((start.index(i), goal.index(i)) for i in range(1,9)))
        # dict_d = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (1, 0), 5: (1, 1), 6: (1, 2), 7: (2, 0), 8: (2, 1), 0: (2, 2)}
        # dict_distance = 0
        # for i in range(self.size):
        #     for j in range(self.size):
        #         value = state[i][j]
        #         dict_distance += abs(dict_d[value][0] - i) + abs(dict_d[value][1] - j)
        # 
        # print("code dist:" + str(distance))
        # print("dict dist:" + str(dict_distance))
        return distance

    def hamming_distance_heuristic(self, state):
        # start = [num for sublist in state for num in sublist]
        # goal = [num for sublist in  self.final_state for num in sublist]
        # x= [0 if start.index(i)==goal.index(i) else 1 for i in range(1,9)]
        # distance = sum(x)
        distance=0
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] != self.final_state[i][j]:
                    distance+=1
        return distance

    def max_heuristic(self, state):
        """Calculate the max heuristic between the current state and the goal state."""
        max_distance = 0
        start = [num for sublist in state for num in sublist]
        goal = [num for sublist in  self.final_state for num in sublist]

        for i in range(len(start)):
            if start[i] != 0:
                current_row = i // 3
                current_col = i % 3
                goal_index = goal.index(start[i])
                goal_row = goal_index // 3
                goal_col = goal_index % 3
                distance = max(abs(current_row - goal_row), abs(current_col - goal_col))
                if distance > max_distance:
                    max_distance = distance
        return max_distance

    def empty_heuristic(self, state):
        return 0
