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
        self.fu = self.heuristic  # self.F()  #float('inf')
        self.neighbours = self.get_neighbours()
        self.isFinalState = True if self.state == tile_puzzle.final_state else False

    def __lt__(self, other):
        # Used for sorting in the priority opened
        # return (self.g + self.heuristic) < (other.g + other.heuristic)
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
            state[i][j], state[i - 1][j] = self.state[i - 1][j],  self.state[i][j]
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
    def __init__(self, size, difficulty, heuristic_func):
        self.size = int(math.sqrt(size+1))
        if size == 8:
            self.final_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
            if difficulty=="easy":
                self.start_state = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
            if difficulty=="medium":
                #self.start_state = [[2, 3, 4], [1, 5, 6], [8, 7, 0]]
                self.start_state = [[3,4,2], [1,0,6], [8,5,7]]
            if difficulty=="hard":
                self.start_state = [[2, 1, 3], [5, 4, 0], [7, 8, 6]]
            if difficulty=="extreme":
                self.start_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
            if difficulty=="unsolvable":
                self.start_state = [[1, 2, 3], [4, 5, 6], [8, 7, 0]]
        elif size == 15:
            self.final_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
            if difficulty=="easy":
                self.start_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [0, 13, 14, 15]]
            # if difficulty=="medium":
            #     self.start_state = [[2, 3, 4], [1, 5, 6], [8, 7, 0]]
            # if difficulty=="hard":
            #     self.start_state = [[2, 1, 3], [5, 4, 0], [7, 8, 6]]
            # if difficulty=="extreme":
            #     self.start_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

        if heuristic_func=="manhattan":
            self.heuristic_func = self.manhattan_distance_heuristic
        if heuristic_func=="euclidean":
            self.heuristic_func = self.euclidean_distance_heuristic
        if heuristic_func=="empty":
            self.heuristic_func = self.empty_heuristic

    def euclidean_distance_heuristic(self,state):
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


    def manhattan_distance_heuristic(self,state):
        distance = 0  # total manhattan distances of all states
        for i in range(self.size):
            for j in range(self.size):
                value = state[i][j]
                if value != 0:
                    row = (value - 1) // self.size
                    col = (value - 1) % self.size
                    distance += abs(row - i) + abs(col - j)
        return distance


    def empty_heuristic(self,state):
        return 0
