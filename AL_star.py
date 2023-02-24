import heapq


class Node:
    def __init__(self, state, parent=None, move=None, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost
        self.heuristic = calculate_heuristic(state)
        self.fu = self.calculate_fu()

    def calculate_fu(self):
        # Calculate the cost of the move based on the lookahead
        self_moves = get_moves(self)
        lookahead_cost = []
        for move_state in self_moves:
            lookahead_cost.append(calculate_heuristic(move_state))
        return (self.cost + min(lookahead_cost))



    def __lt__(self, other):
        # Used for sorting in the priority opened
        #return (self.cost + self.heuristic) < (other.cost + other.heuristic)
        return self.fu < other.fu

    def __eq__(self, other):
        return self.state == other.state

    def F(self):
        return self.cost+self.heuristic

def find_blank(state):
    # Helper function to find the location of the blank tile (0)
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


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


def get_moves(node):
    # Generate all possible moves from the current node
    moves = []
    i, j = find_blank(node.state)
    if j >0 and node.move != 'right': #left
        move = move_blank(node.state, i, j, i, j - 1)
        moves.append(move)
    if j < 2 and node.move != 'left': #right
        move = move_blank(node.state, i, j, i, j + 1)
        moves.append(move)
    if i > 0 and node.move != 'down': #up
        move = move_blank(node.state, i, j, i - 1, j)
        moves.append(move)
    if i < 2 and node.move != 'up': #down
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
    # Create the initial node and priority opened
    initial_node = Node(initial_state)
    opened = [initial_node]
    heapq.heapify(opened)
    closed = set()
    UB = float('inf')
    
    while opened:
        # Get the node with the lowest cost + heuristic
        current_node = heapq.heappop(opened)
        if current_node.cost >= UB :#and current_node.heuristic == 0:
            # The solution has been found ,return path
            moves = []
            while current_node.move:
                moves.append(current_node.move)
                current_node = current_node.parent
            return moves[::-1]

        closed.add(str(current_node.state))

        # Generate possible moves and add them to the opened
        for op in get_moves(current_node):
            child = Node(op, parent=current_node, move=None, cost=current_node.cost + 1) #generateNode

            child.cost = current_node.cost + 1 + child.fu
            child.move = get_move_direction(current_node.state, child.state)

            if child.fu >= UB:
                continue
            if child.state == final_state:
                UB = child.fu
            LHB = min(UB , current_node.F() +k)
            if child.fu<= LHB:
                min_cost,UB ,_ = lookAhead(child,LHB,UB, float('inf'))
                if min_cost> child.F() :
                    child.fu = min_cost
            if str(child.state) not in closed and child not in opened:
                heapq.heappush(opened, child)
            else:
                index = opened.index(child)
                if (opened[index] > child):
                    opened[index] = child
                heapq.heapify(opened)



                # heapq.heappush(opened, child)

    # No solution found
    return None

def lookAhead(v,LHB,UB, minCost, opened=[]):
    moves = get_moves(v)
    for op in moves:
        child = Node(op, parent=v, move=None, cost=v.cost + 1)  # generateNode
        child.move = get_move_direction(v.state, child.state)
        if child.state in opened:
            continue
        else:
            opened.append(child.state)
        if child.state == final_state:
            UB = child.cost
            minCost = min(minCost, child.fu)
        else:
            if child.fu >=LHB:
                minCost = min(minCost, child.fu)
            else:
                newMinCost, UB, opened = lookAhead(child,LHB,UB, minCost,opened)
                minCost = min(minCost, newMinCost)
    return minCost,UB ,opened




solvable_state = [
    [1, 2, 3],
    [4, 5, 6],
    [0, 7, 8]
]
final_state =  [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]
print(a_star_lookahead(solvable_state, final_state, k=10))
