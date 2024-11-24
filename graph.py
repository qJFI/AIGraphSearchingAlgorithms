import math

# Graph data
nodes = []  # List of node positions (x, y)
edges = []  # List of edges [(node1_index, node2_index, weight)]
heuristics = {}  # Heuristic values for each node
start_node = None
goal_node = None

NODE_RADIUS = 20

def distance(node1, node2):
    """Calculate Euclidean distance between two nodes."""
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)

def get_clicked_node(pos):
    """Return the index of the node at the clicked position, or None."""
    for i, node in enumerate(nodes):
        if distance(pos, node) <= NODE_RADIUS:
            return i
    return None

def add_node(pos):
    """Add a new node at the given position."""
    nodes.append(pos)

def set_start_goal(pos):
    """Set the start or goal node."""
    global start_node, goal_node
    clicked_node = get_clicked_node(pos)
    if clicked_node is not None:
        if start_node is None:
            start_node = clicked_node
        elif goal_node is None:
            goal_node = clicked_node
        else:
            # If both are set, overwrite the start node first
            start_node = clicked_node
    return clicked_node

def add_edge(node_index, pos):
    """Add an edge between two nodes."""
    target_node = get_clicked_node(pos)
    if target_node is not None and node_index != target_node:
        edges.append((node_index, target_node, 1))  # Default weight of 1

def move_node(node_index, pos):
    """Move a node to a new position."""
    if node_index is not None:
        nodes[node_index] = pos

def remove_node(pos):
    """Remove a node and all connected edges, along with its heuristic value."""
    global start_node, goal_node
    clicked_node = get_clicked_node(pos)
    if clicked_node is not None:
        nodes.pop(clicked_node)
        edges[:] = [(a, b, w) for (a, b, w) in edges if a != clicked_node and b != clicked_node]
        heuristics.pop(clicked_node, None)
        
        # Adjust start and goal nodes if the removed node is one of them
        if start_node == clicked_node:
            start_node = None
        if goal_node == clicked_node:
            goal_node = None

def initialize_sample_graph():
    """Initialize the graph with a predefined sample."""
    global nodes, edges, start_node, goal_node, heuristics
    nodes = [
        (300, 400),
        (500, 300),
        (500, 500),
        (700, 400),
        (400, 200),
        (400, 600),
        (600, 200),
        (600, 600),
        (800, 300),
        (800, 500),
    ]
    edges = [
        (0, 1, 5),
        (1, 2, 3),
        (2, 3, 2),
        (0, 4, 7),
        (1, 4, 4),
        (3, 8, 6),
        (2, 5, 4),
        (3, 9, 3),
        (6, 7, 2),
        (8, 9, 5),
        (0, 5, 6),
        (4, 6, 4),
        (7, 9, 3),
    ]
    heuristics = {
        0: 9,
        1: 8,
        2: 7,
        3: 6,
        4: 10,
        5: 7,
        6: 5,
        7: 4,
        8: 3,
        9: 0,  # Goal node
    }
    start_node = 0
    goal_node = 9
