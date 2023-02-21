from queue import Queue


def bfs_lookahead(graph, start, goal, lookahead_func):
    """
    Breadth-first search with lookahead

    Parameters:
    - graph: a dictionary representing the graph
    - start: the starting node
    - goal: the goal node
    - lookahead_func: a function that takes a node and returns an estimated cost to the goal

    Returns:
    - the shortest path from start to goal as a list of nodes, or None if no path exists
    """
    queue = Queue()
    visited = set()

    # Add the starting node to the queue
    queue.put([start])

    while not queue.empty():
        path = queue.get()
        node = path[-1]

        if node == goal:
            # We found the goal
            return path

        if node not in visited:
            # Add the node to the visited set
            visited.add(node)

            # Add the neighbors to the queue
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.put(new_path)

                # Lookahead: estimate the cost of reaching the goal from the neighbor
                lookahead_cost = lookahead_func(neighbor)
                if lookahead_cost is not None:
                    # Add the lookahead cost to the path cost
                    new_path_cost = len(new_path) + lookahead_cost
                    queue.put((new_path_cost, new_path))

    # We couldn't find a path from start to goal
    return None

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

def lookahead_func(node):
    if node == 'G':
        return 0
    elif node == 'H':
        return 1
    elif node == 'I':
        return 2
    else:
        return None

path = bfs_lookahead(graph, 'A', 'F', lookahead_func)
print(path)
