import pygame
import math
from algorithms import bfs, dfs, ucs, greedy_search, a_star
import heapq

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080
NODE_RADIUS = 20
EDGE_WIDTH = 3
TOOLBAR_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (200, 200, 200)
BUTTON_HIGHLIGHT = (180, 180, 180)

# Pygame setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Interactive Graph Visualizer")
font = pygame.font.SysFont(None, 24)

# Toolbar Buttons
BUTTON_WIDTH = 140
BUTTON_HEIGHT = 40
buttons = {
    "Add Node": pygame.Rect(10, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Connect Nodes": pygame.Rect(160, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Set Start": pygame.Rect(310, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Set Goal": pygame.Rect(460, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Move Node": pygame.Rect(610, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Remove Node": pygame.Rect(760, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Run BFS": pygame.Rect(910, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Run DFS": pygame.Rect(1060, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Run UCS": pygame.Rect(1210, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Add Heuristic": pygame.Rect(1360, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Example": pygame.Rect(1510, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Run Greedy": pygame.Rect(1660, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Run A*": pygame.Rect(1810, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
}

# Graph data
nodes = []  # List of node positions (x, y)
edges = []  # List of edges [(node1_index, node2_index, weight)]
heuristics = {}  # Heuristic values for each node
start_node = None
goal_node = None

# Action States
current_action = None
selected_node = None
dragging_node = None
input_active = False
input_box = pygame.Rect(300, 500, 140, 32)
input_text = ""
current_edge = None


def draw_toolbar():
    """Draw the toolbar with buttons."""
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    for label, rect in buttons.items():
        # Highlight the selected button
        color = BUTTON_HIGHLIGHT if current_action == label else WHITE
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text_surface = font.render(label, True, BLACK)
        screen.blit(
            text_surface,
            (rect.x + (BUTTON_WIDTH - text_surface.get_width()) // 2, rect.y + 10),
        )

def draw_graph():
    """Draw the graph with nodes, edges, and heuristic values."""
    screen.fill(WHITE, (0, TOOLBAR_HEIGHT, WIDTH, HEIGHT - TOOLBAR_HEIGHT))

    # Draw edges
    for edge in edges:
        node1 = nodes[edge[0]]
        node2 = nodes[edge[1]]
        pygame.draw.line(screen, GRAY, node1, node2, EDGE_WIDTH)

        # Draw weight
        mid_x = (node1[0] + node2[0]) // 2
        mid_y = (node1[1] + node2[1]) // 2
        weight_text = font.render(str(edge[2]), True, BLACK)
        screen.blit(weight_text, (mid_x, mid_y))

    # Draw nodes
    for i, node in enumerate(nodes):
        color = GREEN if i == start_node else RED if i == goal_node else BLUE
        pygame.draw.circle(screen, color, node, NODE_RADIUS)
        pygame.draw.circle(screen, BLACK, node, NODE_RADIUS, 2)

        # Draw node label
        label = font.render(str(i), True, BLACK)
        screen.blit(label, (node[0] - 10, node[1] - 10))

        # Display heuristic values
        if i in heuristics:
            heuristic_text = font.render(f"h={heuristics[i]}", True, BLACK)
            screen.blit(heuristic_text, (node[0] + 15, node[1] - 10))

def draw_input_box():
    """Draw the input box for entering edge weights."""
    pygame.draw.rect(screen, WHITE, input_box)
    pygame.draw.rect(screen, BLACK, input_box, 2)
    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    pygame.display.update()

def distance(node1, node2):
    """Calculate Euclidean distance between two nodes."""
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)

def get_clicked_node(pos):
    """Return the index of the node at the clicked position, or None."""
    for i, node in enumerate(nodes):
        if distance(pos, node) <= NODE_RADIUS:
            return i
    return None

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
        (0, 5, 6),  # Connect node 0 to node 5
        (4, 6, 4),  # Connect node 4 to node 6
        (7, 9, 3),  # Connect node 7 to node 9
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

def main():
    global current_action, selected_node, start_node, goal_node, dragging_node, input_active, input_text, current_edge
    running = True

    while running:
        draw_toolbar()
        draw_graph()

        if input_active:
            draw_input_box()

        pygame.display.update()

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

                if input_active:
                    if event.key == pygame.K_RETURN:
                        if input_text.isdigit():
                            if current_action == "Add Heuristic" and selected_node is not None:
                                # Assign the entered heuristic value to the selected node
                                heuristics[selected_node] = int(input_text)
                                input_text = ""
                                input_active = False
                                selected_node = None

                            elif current_action == "Connect Nodes" and current_edge is not None:
                                # Modify the weight of the existing edge instead of adding a new one
                                node1, node2 = current_edge
                                edge_found = False

                                # Search for the existing edge and update the weight
                                for i, edge in enumerate(edges):
                                    if (edge[0] == node1 and edge[1] == node2) or (edge[0] == node2 and edge[1] == node1):
                                        edges[i] = (node1, node2, int(input_text))
                                        edge_found = True
                                        break

                                # If the edge doesn't exist, add it as a new one (optional)
                                if not edge_found:
                                    edges.append((node1, node2, int(input_text)))

                                input_text = ""
                                input_active = False
                                current_edge = None

                    elif event.key == pygame.K_BACKSPACE:
                        # Allow backspace to edit the input text
                        input_text = input_text[:-1]
                    else:
                        # Append new character to the input text
                        input_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] <= TOOLBAR_HEIGHT:  # Check if click is on the toolbar
                    for label, rect in buttons.items():
                        if rect.collidepoint(pos):
                            current_action = label
                            selected_node = None
                            input_active = False
                            dragging_node = None
                            # Initialize sample graph if "Example" button is pressed
                            if label == "Example":
                                initialize_sample_graph()
                            break
                else:  # Graph interaction
                    if current_action == "Add Node":
                        nodes.append(pos)
                    elif current_action == "Set Start":
                        clicked_node = get_clicked_node(pos)
                        if clicked_node is not None:
                            start_node = clicked_node
                    elif current_action == "Set Goal":
                        clicked_node = get_clicked_node(pos)
                        if clicked_node is not None:
                            goal_node = clicked_node
                    elif current_action == "Connect Nodes":
                        clicked_node = get_clicked_node(pos)
                        if clicked_node is not None:
                            if selected_node is None:
                                selected_node = clicked_node
                            else:
                                current_edge = (selected_node, clicked_node)
                                input_active = True
                                input_box.center = pos
                                selected_node = None
                    elif current_action == "Move Node":
                        clicked_node = get_clicked_node(pos)
                        if clicked_node is not None:
                            dragging_node = clicked_node
                    elif current_action == "Remove Node":
                        clicked_node = get_clicked_node(pos)
                        if clicked_node is not None:
                            nodes.pop(clicked_node)
                            edges[:] = [e for e in edges if clicked_node not in e]
                            start_node = None if start_node == clicked_node else start_node
                            goal_node = None if goal_node == clicked_node else goal_node
                            heuristics.pop(clicked_node, None)
                    elif current_action == "Add Heuristic":
                        clicked_node = get_clicked_node(pos)
                        if clicked_node is not None:
                            selected_node = clicked_node
                            input_active = True
                            input_box.center = pos

            if event.type == pygame.MOUSEBUTTONUP:
                if current_action == "Move Node":
                    dragging_node = None

            if event.type == pygame.MOUSEMOTION:
                if dragging_node is not None:
                    nodes[dragging_node] = event.pos

            if current_action == "Run BFS" and start_node is not None and goal_node is not None:
                bfs(start_node, goal_node, nodes, edges, draw_graph)
                current_action = None

            if current_action == "Run DFS" and start_node is not None and goal_node is not None:
                dfs(start_node, goal_node, nodes, edges, draw_graph)
                current_action = None

            if current_action == "Run UCS" and start_node is not None and goal_node is not None:
                ucs(start_node, goal_node, nodes, edges, draw_graph)
                current_action = None

            if current_action == "Run Greedy" and start_node is not None and goal_node is not None:
                greedy_search(start_node, goal_node, nodes, edges, heuristics, draw_graph)
                current_action = None

            if current_action == "Run A*" and start_node is not None and goal_node is not None:
                a_star(start_node, goal_node, nodes, edges, heuristics, draw_graph)
                current_action = None

if __name__ == "__main__":
    main()
