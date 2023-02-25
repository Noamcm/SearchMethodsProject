import copy
import heapq


class Node:
    def __init__(self, state, parent=None, move=None, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost
        self.heuristic = calculate_heuristic(state)
        self.fu = float('inf')
        self.is_closed = False
        self.neighbours = get_neighbours(self.state)

    def calculate_fu(self):
        # Calculate the cost of the move based on the lookahead
        self_moves = get_moves(self)
        lookahead_cost = []
        for move_state in self_moves:
            lookahead_cost.append(calculate_heuristic(move_state))
        # return (self.g + min(lookahead_cost))
        return (self.g + max(lookahead_cost))

    def __lt__(self, other):
        # Used for sorting in the priority opened
        # return (self.g + self.heuristic) < (other.g + other.heuristic)
        return self.fu < other.fu

    def __eq__(self, other):
        return self.state == other.state

    def F(self):
        return self.g + self.heuristic


def find_blank(state):
    # Helper function to find the location of the blank tile (0)
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return -1, -1


def move(state, direction):
    # Helper function to make a move in a given direction
    i, j = find_blank(state)
    if direction == 'up' and i > 0:
        state[i][j], state[i - 1][j] = state[i - 1][j], state[i][j]
    elif direction == 'down' and i < 2:
        state[i][j], state[i + 1][j] = state[i + 1][j], state[i][j]
    elif direction == 'left' and j > 0:
        state[i][j], state[i][j - 1] = state[i][j - 1], state[i][j]
    elif direction == 'right' and j < 2:
        state[i][j], state[i][j + 1] = state[i][j + 1], state[i][j]
    return state


def get_neighbours(state):
    neighbours = []
    for direction in ['up', 'down', 'left', 'right']:
        new_state = copy.deepcopy(state)
        move(new_state, direction)
        if new_state != state:
            neighbours.append(new_state)
    return neighbours


def get_moves(node):
    # Generate all possible moves from the current node
    moves = []
    i, j = find_blank(node.state)
    if j > 0 and node.move != 'right':  # left
        move = move_blank(node.state, i, j, i, j - 1)
        moves.append(move)
    if j < 2 and node.move != 'left':  # right
        move = move_blank(node.state, i, j, i, j + 1)
        moves.append(move)
    if i > 0 and node.move != 'down':  # up
        move = move_blank(node.state, i, j, i - 1, j)
        moves.append(move)
    if i < 2 and node.move != 'up':  # down
        move = move_blank(node.state, i, j, i + 1, j)
        moves.append(move)
    return moves


def move_blank(state, i1, j1, i2, j2):
    # Move the blank space from (i1, j1) to (i2, j2) and return the new state
    new_state = [row[:] for row in state]
    new_state[i1][j1], new_state[i2][j2] = new_state[i2][j2], new_state[i1][j1]
    return new_state


def get_move_direction(current_state, new_state):
    # Determine the direction of the move based on the old and new states
    curr_i, curr_j = find_blank(current_state)
    new_i, new_j = find_blank(new_state)
    if curr_i < new_i:
        return 'down'
    elif curr_i > new_i:
        return 'up'
    elif curr_j < new_j:
        return 'right'
    elif curr_j > new_j:
        return 'left'


def calculate_heuristic(state):
    # Calculate the Manhattan distance heuristic for the 8-tile puzzle
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                row = (value - 1) // 3
                col = (value - 1) % 3
                distance += abs(row - i) + abs(col - j)
    return distance


def a_star_lookahead(initial_state, final_state, k=0):
    UB = float('inf')

    # Create the initial node and priority opened
    initial_node = Node(initial_state)
    # TODO: lookahead before inserting to opened and update initial_node.fu by DFS to depth k
    min_cost, UB = lookAhead(initial_node, initial_node.F() + k, UB, float('inf'),k)
    opened = [initial_node]
    heapq.heapify(opened)
    closed = set()

    while opened:
        # Get the node with the lowest cost + heuristic
        current_node = heapq.heappop(opened)  # input - best node in open list: v
        print(len(opened)) #362880
        if current_node.g >= UB:  # 1 #or current_node.state == final_state
            # The solution has been found ,return path
            moves = []
            while current_node.move:
                moves.append(current_node.move)
                current_node = current_node.parent
            return moves[::-1]  # 2 - halt

        closed.add(str(current_node.state))  # 3
        current_node.is_closed = True
        # Generate possible moves and add them to the opened
        for ne in current_node.neighbours:  # 4
            child = Node(ne, parent=current_node, g=current_node.g + 1)  # 5 - generateNode(op,v)
            if str(child.state) in closed:
                continue
            # child.g = current_node.g + 1 + child.fu
            # child.move = get_move_direction(current_node.state, child.state)
            if child.fu >= UB:  # 6
                continue  # 7 - Prune
            if child.state == final_state:  # 8 - goalTest(child)=True
                UB = child.fu  # 8
            LHB = min(UB, current_node.F() + k)  # 10 - LHB=lookahead bound
            if child.fu <= LHB:  # 11
                min_cost, UB = lookAhead(child, LHB, UB, float('inf'), k)  # 12, 13 - lookahead call can update UB
                if min_cost > child.F():  # 14.1
                    child.fu = min_cost  # 14.2
            if child not in opened:  # 15 - duplicateDetection(child)=False
                heapq.heappush(opened, child)  # 16 - Insert child to open list
            else:  # 17
                heapq.heapreplace(opened, child)
                #heapq.heappush(opened, child)
                # index = opened.index(child)
                # if opened[index] > child:  # 18 - Reorder child in OPEN (if required)
                #     opened[index] = child
                #     heapq.heapify(opened)

    # No solution found
    return None


def lookAhead(v, LHB, UB, minCost, k, current_level=0):
    if current_level>k:
        return minCost, UB
    moves = get_moves(v)
    for op in moves:  # 1
        child = Node(op, parent=v, g=v.g + 1)  # 2 - generateNode(op, v)
        child.move = get_move_direction(v.state, child.state)

        if child.state == final_state:  # 3 - goalTest(child)=True
            UB = child.g  # 4
            minCost = min(minCost, child.fu)  # 5
        else:  # 6
            if child.fu >= LHB:  # 7
                minCost = min(minCost, child.fu)  # 8
            else:  # 9
                newMinCost, UB = lookAhead(child, LHB, UB, minCost, k, current_level + 1)  # 10 - recursive call
                minCost = min(minCost, newMinCost)  # 10 - get the minimum
    return minCost, UB


unsolvable_state = [
    [1, 2, 3],
    [4, 5, 6],
    [8, 7, 0]
]
easy_solvable_state = [
    [1, 2, 3],
    [4, 5, 6],
    [0, 7, 8]
]
hard_solvable_state = [
    [1, 2, 3],
    [4, 6, 5],
    [8, 7, 0]
]
final_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]
print(a_star_lookahead(hard_solvable_state, final_state, k=2))
