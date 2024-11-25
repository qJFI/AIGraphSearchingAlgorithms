# DrawScene.py
import pygame
import settings
import context

def draw_toolbar():
    """Draw the toolbar with buttons."""
    screen = settings.screen
    buttons = settings.buttons
    font = settings.font
    TOOLBAR_HEIGHT = settings.TOOLBAR_HEIGHT
    BUTTON_WIDTH = settings.BUTTON_WIDTH
    BUTTON_HIGHLIGHT = settings.BUTTON_HIGHLIGHT
    LIGHT_GRAY = settings.LIGHT_GRAY
    WHITE = settings.WHITE
    BLACK = settings.BLACK

    current_action = context.current_action

    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, screen.get_width(), TOOLBAR_HEIGHT))
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
    screen = settings.screen
    nodes = context.nodes
    edges = context.edges
    heuristics = context.heuristics
    start_node = context.start_node
    goal_nodes = context.goal_nodes
    NODE_RADIUS = settings.NODE_RADIUS
    EDGE_WIDTH = settings.EDGE_WIDTH
    font = settings.font
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    TOOLBAR_HEIGHT = settings.TOOLBAR_HEIGHT
    GRAY = settings.GRAY
    GREEN = settings.GREEN
    RED = settings.RED
    BLUE = settings.BLUE
    BLACK = settings.BLACK
    WHITE = settings.WHITE

    screen.fill(WHITE, (0, TOOLBAR_HEIGHT, WIDTH, HEIGHT - TOOLBAR_HEIGHT))

    # Draw edges
    for edge in edges:
        node1_id, node2_id, weight = edge
        node1 = next((n for n in nodes if n[2] == node1_id), None)
        node2 = next((n for n in nodes if n[2] == node2_id), None)
        if node1 and node2:
            x1, y1, _ = node1
            x2, y2, _ = node2
            pygame.draw.line(screen, GRAY, (x1, y1), (x2, y2), EDGE_WIDTH)

            # Draw weight
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            weight_text = font.render(str(weight), True, BLACK)
            screen.blit(weight_text, (mid_x, mid_y))

    # Draw nodes
    for node in nodes:
        x, y, node_id = node
        if node_id == start_node:
            color = GREEN
        elif node_id in goal_nodes:
            color = RED
        else:
            color = BLUE
        pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)
        pygame.draw.circle(screen, BLACK, (x, y), NODE_RADIUS, 2)

        # Draw node label
        label = font.render(str(node_id), True, BLACK)
        screen.blit(label, (x - 10, y - 10))

        # Display heuristic values
        if node_id in heuristics:
            heuristic_text = font.render(f"h={heuristics[node_id]}", True, BLACK)
            screen.blit(heuristic_text, (x + 15, y - 10))

def draw_input_box():
    """Draw the input box for entering edge weights."""
    screen = settings.screen
    input_box = settings.input_box
    font = settings.font
    WHITE = settings.WHITE
    BLACK = settings.BLACK

    input_text = context.input_text

    pygame.draw.rect(screen, WHITE, input_box)
    pygame.draw.rect(screen, BLACK, input_box, 2)
    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    pygame.display.update()
