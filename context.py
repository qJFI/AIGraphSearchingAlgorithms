# context.py
#shared Vars 

# Graph data
nodes = []  # List of nodes as (x, y, id)
edges = []  # List of edges [(node1_id, node2_id, weight)]
heuristics = {}  # Heuristic values for each node
start_node = None
goal_nodes = set()  # Set of goal node ids
next_node_id = 0  # To assign unique IDs to nodes

# Action States
current_action = None
selected_node = None
dragging_node = None
input_active = False
input_text = ""
current_edge = None
