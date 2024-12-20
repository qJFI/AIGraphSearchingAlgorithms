# main.py
import pygame
import math
from algorithms import bfs, dfs, ucs, greedy_search, a_star
from DrawScene import draw_toolbar, draw_graph, draw_input_box
import settings
import context

def distance(node1, node2):
    """Calculate Euclidean distance between two nodes."""
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)

def get_clicked_node(pos):
    """Return the id of the node at the clicked position, or None."""
    for node in context.nodes:
        x, y, node_id = node
        if distance(pos, (x, y)) <= settings.NODE_RADIUS:
            return node_id
    return None

def initialize_sample_graph():
    """Initialize the graph with a predefined sample."""
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
    context.next_node_id = 10  # Update next_node_id based on sample nodes
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
        (0, 5, 6),  # Connect node 0 to node 5
        (4, 6, 4),  # Connect node 4 to node 6
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
        9: 0,  # One of the goal nodes
    }
    context.start_node = 0
    context.goal_nodes = {9}  # Initialize with node 9 as a goal node

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
                    if event.key == pygame.K_RETURN:
                        if context.input_text.isdigit():
                            if context.current_action == "Add Heuristic" and context.selected_node is not None:
                                # Assign the entered heuristic value to the selected node
                                context.heuristics[context.selected_node] = int(context.input_text)
                                context.input_text = ""
                                context.input_active = False
                                context.selected_node = None

                            elif context.current_action == "Connect Nodes" and context.current_edge is not None:
                                # Modify the weight of the existing edge instead of adding a new one
                                node1, node2 = context.current_edge
                                edge_found = False

                                # Search for the existing edge and update the weight
                                for i, edge in enumerate(context.edges):
                                    if (edge[0] == node1 and edge[1] == node2) or (edge[0] == node2 and edge[1] == node1):
                                        context.edges[i] = (node1, node2, int(context.input_text))
                                        edge_found = True
                                        break

                                # If the edge doesn't exist, add it as a new one
                                if not edge_found:
                                    context.edges.append((node1, node2, int(context.input_text)))

                                context.input_text = ""
                                context.input_active = False
                                context.current_edge = None

                    elif event.key == pygame.K_BACKSPACE:
                        # Allow backspace to edit the input text
                        context.input_text = context.input_text[:-1]
                    else:
                        # Append new character to the input text
                        context.input_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN: # like C# MouseDown
                pos = pygame.mouse.get_pos()
                if pos[1] <= settings.TOOLBAR_HEIGHT:  # Check if click is on the toolbar
                    for label, rect in settings.buttons.items():
                        if rect.collidepoint(pos):
                            if label == "Toggle Dark Mode":
                                # Toggle the dark mode
                                settings.is_dark_mode = not settings.is_dark_mode
                                # No need to change current_action
                                break
                            elif label == "Reset":
                                # Reset the graph and context variables
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
                                break
                            else:
                                context.current_action = label
                                context.selected_node = None
                                context.input_active = False
                                context.dragging_node = None
                                # Initialize sample graph if "Example" button is pressed
                                if label == "Example":
                                    initialize_sample_graph()
                                break
                else:  # Graph interaction
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
                                context.heuristics[clicked_node]=1
                            else:
                                context.goal_nodes.add(clicked_node)
                                context.heuristics[clicked_node]=0
                    elif context.current_action == "Connect Nodes":
                        clicked_node = get_clicked_node(pos)
                        if clicked_node is not None:
                            if context.selected_node is None:
                                context.selected_node = clicked_node
                            else:
                                context.current_edge = (context.selected_node, clicked_node)
                                context.input_active = True
                                settings.input_box.center = pos
                                context.selected_node = None
                    elif context.current_action == "Move Node":
                        clicked_node = get_clicked_node(pos)
                        if clicked_node is not None:
                            context.dragging_node = clicked_node
                    elif context.current_action == "Remove Node":
                        clicked_node = get_clicked_node(pos)
                        if clicked_node is not None:
                            # Remove the node by id
                            context.nodes = [n for n in context.nodes if n[2] != clicked_node]
                            # Remove all edges connected to this node
                            context.edges[:] = [e for e in context.edges if clicked_node not in e[:2]]
                            context.start_node = None if context.start_node == clicked_node else context.start_node
                            context.goal_nodes.discard(clicked_node)  # Remove from goal nodes if present
                            context.heuristics.pop(clicked_node, None)
                    elif context.current_action == "Add Heuristic":
                        clicked_node = get_clicked_node(pos)
                        if clicked_node is not None:
                            context.selected_node = clicked_node
                            context.input_active = True
                            settings.input_box.center = pos

            if event.type == pygame.MOUSEBUTTONUP:
                if context.current_action == "Move Node":
                    context.dragging_node = None

            if event.type == pygame.MOUSEMOTION:
                if context.dragging_node is not None:
                    # Update the position of the dragging node
                    for idx, node in enumerate(context.nodes):
                        if node[2] == context.dragging_node:
                            context.nodes[idx] = (event.pos[0], event.pos[1], node[2])
                            break

        # Run algorithms if action is selected
        if context.current_action == "Run BFS" and context.start_node is not None and context.goal_nodes:
            bfs()
            context.current_action = None

        if context.current_action == "Run DFS" and context.start_node is not None and context.goal_nodes:
            dfs()
            context.current_action = None

        if context.current_action == "Run UCS" and context.start_node is not None and context.goal_nodes:
            ucs()
            context.current_action = None

        if context.current_action == "Run Greedy" and context.start_node is not None and context.goal_nodes:
            greedy_search()
            context.current_action = None

        if context.current_action == "Run A*" and context.start_node is not None and context.goal_nodes:
            a_star()
            context.current_action = None

if __name__ == "__main__":
    main()
