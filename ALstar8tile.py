import heapq


class Node:
    def __init__(self, state, parent=None, move=None, depth=0, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
        self.heuristic = self.calculate_heuristic()

    def calculate_heuristic(self):
        # Calculate the Manhattan distance heuristic for the 8-tile puzzle
        distance = 0
        for i in range(3):
            for j in range(3):
                value = self.state[i][j]
                if value != 0:
                    row = (value - 1) // 3
                    col = (value - 1) % 3
                    distance += abs(row - i) + abs(col - j)
        return distance

    def __lt__(self, other):
        # Used for sorting in the priority queue
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


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
    # Generate possible moves for a given node
    moves = []
    if node.move != 'down':
        moves.append(move([row[:] for row in node.state], 'up'))
    if node.move != 'up':
        moves.append(move([row[:] for row in node.state], 'down'))
    if node.move != 'right':
        moves.append(move([row[:] for row in node.state], 'left'))
    if node.move != 'left':
        moves.append(move([row[:] for row in node.state], 'right'))
    return moves


def a_star_lookahead(initial_state):
    # Create the initial node and priority queue
    initial_node = Node(initial_state)
    queue = [initial_node]
    heapq.heapify(queue)
    explored = set()

    while queue:
        # Get the node with the lowest cost + heuristic
        current_node = heapq.heappop(queue)
        explored.add(str(current_node.state))

        if current_node.heuristic == 0:
            # The solution has been found
            moves = []
            while current_node.move:
                moves.append(current_node.move)
                current_node = current_node.parent
            return moves[::-1]

        # Generate possible moves and add them to the queue
        for child_state in get_moves(current_node):
            child = Node(child_state, parent=current_node, move=None, depth=current_node.depth + 1)

            if str(child.state) not in explored:
                # Calculate the cost of the move based on the lookahead
                child_moves = get_moves(child)
                lookahead_cost = 0
                for move_state in child_moves:
                    lookahead_node = Node(move_state)
                    lookahead_cost += lookahead_node.calculate_heuristic()
                lookahead_cost /= len(child_moves)
                child.cost = current_node.cost + 1 + lookahead_cost
                child.move = get_move_direction(current_node.state, child_state)
                heapq.heappush(queue, child)

    # No solution found
    return None

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

solvable_state = [
    [1, 2, 3],
    [4, 5, 6],
    [0, 7, 8]
]
print(a_star_lookahead(solvable_state))
