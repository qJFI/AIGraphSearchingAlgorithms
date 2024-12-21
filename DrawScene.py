# DrawScene.py
import pygame
import settings
import context

def draw_toolbar():
    #Draw the toolbar with buttons
    screen = settings.screen
    buttons = settings.buttons
    font = settings.font
    TOOLBAR_HEIGHT = settings.TOOLBAR_HEIGHT
    BUTTON_WIDTH = settings.BUTTON_WIDTH
    FONT_COLOR = settings.get_color('FONT_COLOR')
    BLACK = (0, 0, 0)

    current_action = context.current_action

    TOOLBAR_COLOR = settings.get_color('TOOLBAR_COLOR')
    pygame.draw.rect(screen, TOOLBAR_COLOR, (0, 0, screen.get_width(), TOOLBAR_HEIGHT))

    for label, rect in buttons.items():
        # Highlight the selected button
        mouse_pos = pygame.mouse.get_pos()
        BUTTON_COLOR = settings.get_color('BUTTON_COLOR')
        BUTTON_HIGHLIGHT_COLOR = settings.get_color('BUTTON_HIGHLIGHT_COLOR')
        if rect.collidepoint(mouse_pos):
            color = BUTTON_HIGHLIGHT_COLOR
        elif current_action == label:
            color = BUTTON_HIGHLIGHT_COLOR
        else:
            color = BUTTON_COLOR
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text_surface = font.render(label, True, FONT_COLOR)
        screen.blit(
            text_surface,
            (rect.x + (BUTTON_WIDTH - text_surface.get_width()) // 2, rect.y + 10),
        )

def draw_graph():
    #Draw the graph with nodes, edges, and heuristic values
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
    BLACK = (0, 0, 0)

    BACKGROUND_COLOR = settings.get_color('BACKGROUND_COLOR')
    NODE_COLOR = settings.get_color('NODE_COLOR')
    EDGE_COLOR = settings.get_color('EDGE_COLOR')
    PATH_COLOR = settings.get_color('PATH_COLOR')
    FONT_COLOR = settings.get_color('FONT_COLOR')
    VISITED_NODE_COLOR = settings.get_color('VISITED_NODE_COLOR')
    START_NODE_COLOR = settings.get_color('START_NODE_COLOR')
    GOAL_NODE_COLOR = settings.get_color('GOAL_NODE_COLOR')

    screen.fill(BACKGROUND_COLOR, (0, TOOLBAR_HEIGHT, WIDTH, HEIGHT - TOOLBAR_HEIGHT))

    # Draw edges
    for edge in edges:
        node1_id, node2_id, weight = edge
        node1 = next((n for n in nodes if n[2] == node1_id), None)
        node2 = next((n for n in nodes if n[2] == node2_id), None)
        if node1 and node2:
            x1, y1, _ = node1
            x2, y2, _ = node2
            pygame.draw.line(screen, EDGE_COLOR, (x1, y1), (x2, y2), EDGE_WIDTH)

            # Draw weight
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            weight_text = font.render(str(weight), True, FONT_COLOR)
            screen.blit(weight_text, (mid_x, mid_y))

    # Draw nodes
    for node in nodes:
        x, y, node_id = node
        if node_id == start_node:
            color = START_NODE_COLOR
        elif node_id in goal_nodes:
            color = GOAL_NODE_COLOR
        else:
            color = NODE_COLOR
        pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)
        pygame.draw.circle(screen, BLACK, (x, y), NODE_RADIUS, 2)

        # Draw node label
        label = font.render(str(node_id), True, FONT_COLOR)
        screen.blit(label, (x - 10, y - 10))

        # Display heuristic values
        if node_id in heuristics:
            heuristic_text = font.render(f"h={heuristics[node_id]}", True, FONT_COLOR)
            screen.blit(heuristic_text, (x + 15, y - 10))

def draw_input_box():
    #Draw the input box for entering edge weights
    screen = settings.screen
    input_box = settings.input_box
    font = settings.font
    FONT_COLOR = settings.get_color('FONT_COLOR')
    INPUT_BOX_COLOR = settings.get_color('INPUT_BOX_COLOR')
    BLACK = (0, 0, 0)

    input_text = context.input_text

    pygame.draw.rect(screen, INPUT_BOX_COLOR, input_box)
    pygame.draw.rect(screen, BLACK, input_box, 2)
    text_surface = font.render(input_text, True, FONT_COLOR)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    pygame.display.update()
