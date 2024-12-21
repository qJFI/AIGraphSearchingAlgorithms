# main.py
import pygame
import math
from algorithms import bfs, dfs, ucs, greedy_search, a_star
from DrawScene import draw_toolbar, draw_graph, draw_input_box
import settings
import context

def distance(node1, node2):
    # Calculate Euclidean distance between two nodes.
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)
    # could use Manhattan distance for similar Heuristic return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])


def calculateAllHurestics():
    # Automatically calculate and set heuristics for nodes without existing values.
    for node in context.nodes:
        node_id = node[2]
        
        # Calculate heuristic as the minimum distance to any goal node
        min_distance = float('inf')
        for goal_id in context.goal_nodes:
            goal_node = next((n for n in context.nodes if n[2] == goal_id), None)
            if goal_node:
                distance_to_goal = distance(node, goal_node)
                if distance_to_goal < min_distance:
                    min_distance = distance_to_goal
            context.heuristics[node_id] = int(min_distance) 

def get_clicked_node(pos):
    # Return the id of the node at the clicked position, or None.
    for node in context.nodes:
        x, y, node_id = node
        if distance(pos, (x, y)) <= settings.NODE_RADIUS:
            return node_id
    return None

def initialize_sample_graph():
    # Initialize the graph with a predefined sample.
    context.nodes = [
        (300, 400, 0),
        (500, 300, 1),
        (500, 500, 2),
        (700, 400, 3),
        (400, 200, 4),
        (400, 600, 5),
        (600, 200, 6),
        (600, 600, 7),
        (800, 300, 8),
        (800, 500, 9),
    ]
    context.next_node_id = 10  # no of example nodes
    context.edges = [
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
        (7, 9, 3),  # Connect node 7 to node 9
    ]
    context.heuristics = {
        0: 9,
        1: 8,
        2: 7,
        3: 6,
        4: 10,
        5: 7,
        6: 5,
        7: 4,
        8: 3,
        9: 0,  # One of the goal nodes heuristic=0
    }
    context.start_node = 0
    context.goal_nodes = {9}  # Initialize with node 9 as a goal node

def handle_toolbar_click(pos):
    # Handle toolbar button clicks.
    for label, rect in settings.buttons.items():
        if rect.collidepoint(pos):
            if label == "Toggle Dark Mode":
                settings.is_dark_mode = not settings.is_dark_mode
                break
            elif label == "Reset":
                reset_context()
                break
            else:
                context.current_action = label
                context.selected_node = None
                context.input_active = False
                context.dragging_node = None
                if label == "Example":
                    initialize_sample_graph()
                break

def reset_context():
    # Reset all context variables.
    context.nodes = []
    context.edges = []
    context.heuristics = {}
    context.start_node = None
    context.goal_nodes = set()
    context.next_node_id = 0
    context.current_action = None
    context.selected_node = None
    context.dragging_node = None
    context.input_active = False
    context.input_text = ""
    context.current_edge = None

def handle_graph_interaction(pos):
    # Handle interactions with the graph.
    if context.current_action == "Add Node":
        context.nodes.append((pos[0], pos[1], context.next_node_id))
        context.next_node_id += 1
    elif context.current_action == "Set Start":
        clicked_node = get_clicked_node(pos)
        if clicked_node is not None:
            context.start_node = clicked_node
    elif context.current_action == "Set Goal":
        clicked_node = get_clicked_node(pos)
        if clicked_node is not None:
            if clicked_node in context.goal_nodes:
                context.goal_nodes.remove(clicked_node)
                context.heuristics[clicked_node] = 1
            else:
                context.goal_nodes.add(clicked_node)
                context.heuristics[clicked_node] = 0
    elif context.current_action == "Connect Nodes":
        handle_connect_nodes(pos)
    elif context.current_action == "Move Node":
        clicked_node = get_clicked_node(pos)
        if clicked_node is not None:
            context.dragging_node = clicked_node
    elif context.current_action == "Remove Node":
        remove_node(get_clicked_node(pos))
    elif context.current_action == "Add Heuristic":
        clicked_node = get_clicked_node(pos)
        if clicked_node is not None:
            context.selected_node = clicked_node
            context.input_active = True
            settings.input_box.center = pos
    elif context.current_action == "All Heuristics":
        calculateAllHurestics()
        context.current_action = None

def handle_connect_nodes(pos):
    # Handle connecting nodes with edges.
    clicked_node = get_clicked_node(pos)
    if clicked_node is not None:
        if context.selected_node is None:
            context.selected_node = clicked_node
        else:
            context.current_edge = (context.selected_node, clicked_node)
            context.input_active = True
            settings.input_box.center = pos
            context.selected_node = None

def remove_node(node_id):
    # Remove a node and its connected edges.
    if node_id is not None:
        context.nodes = [n for n in context.nodes if n[2] != node_id]
        context.edges[:] = [e for e in context.edges if node_id not in e[:2]]
        if context.start_node == node_id:
            context.start_node = None
        context.goal_nodes.discard(node_id)
        context.heuristics.pop(node_id, None)

def run_selected_algorithm():
    # Run the selected algorithm based on the current action.
    if context.current_action == "Run BFS" and context.start_node is not None and context.goal_nodes:
        bfs()
        context.current_action = None
    elif context.current_action == "Run DFS" and context.start_node is not None and context.goal_nodes:
        dfs()
        context.current_action = None
    elif context.current_action == "Run UCS" and context.start_node is not None and context.goal_nodes:
        ucs()
        context.current_action = None
    elif context.current_action == "Run Greedy" and context.start_node is not None and context.goal_nodes:
        greedy_search()
        context.current_action = None
    elif context.current_action == "Run A*" and context.start_node is not None and context.goal_nodes:
        a_star()
        context.current_action = None



def handle_input(event):
    # Handle text input events.
    if event.key == pygame.K_RETURN:
        if context.input_text.isdigit():
            if context.current_action == "Add Heuristic" and context.selected_node is not None:
                context.heuristics[context.selected_node] = int(context.input_text)
                context.input_text = ""
                context.input_active = False
                context.selected_node = None
            elif context.current_action == "Connect Nodes" and context.current_edge is not None:
                node1, node2 = context.current_edge
                edge_found = False
                for i, edge in enumerate(context.edges):
                    if (edge[0] == node1 and edge[1] == node2) or (edge[0] == node2 and edge[1] == node1):
                        context.edges[i] = (node1, node2, int(context.input_text))
                        edge_found = True
                        break
                if not edge_found:
                    context.edges.append((node1, node2, int(context.input_text)))

                context.input_text = ""
                context.input_active = False
                context.current_edge = None
    elif event.key == pygame.K_BACKSPACE:
        context.input_text = context.input_text[:-1]
    else:
        context.input_text += event.unicode

def main():
    running = True

    while running:
        draw_toolbar()
        draw_graph()

        if context.input_active:
            draw_input_box()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    return

                if context.input_active:
                    handle_input(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] <= settings.TOOLBAR_HEIGHT:
                    handle_toolbar_click(pos)
                else:
                    handle_graph_interaction(pos)

            if event.type == pygame.MOUSEBUTTONUP:
                if context.current_action == "Move Node":
                    context.dragging_node = None

            if event.type == pygame.MOUSEMOTION:
                if context.dragging_node is not None:
                    for idx, node in enumerate(context.nodes):
                        if node[2] == context.dragging_node:
                            context.nodes[idx] = (event.pos[0], event.pos[1], node[2])
                            break

        run_selected_algorithm()


if __name__ == "__main__":
    main()
