import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (73, 154, 229)
LIGHT_GRAY = (200, 200, 200)
BUTTON_HIGHLIGHT = (180, 180, 180)

# Node and Edge settings
NODE_RADIUS = 20
EDGE_WIDTH = 3

def draw_toolbar(screen, buttons, current_action, font):
    """Draw the toolbar with buttons."""
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, 1920, 100))  # Toolbar area
    for label, rect in buttons.items():
        color = BUTTON_HIGHLIGHT if current_action == label else WHITE
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text_surface = font.render(label, True, BLACK)
        screen.blit(
            text_surface,
            (rect.x + (rect.width - text_surface.get_width()) // 2, rect.y + 10),
        )

def draw_graph(screen, nodes, edges, start_node, goal_node, font):
    """Draw the graph with nodes, edges, start and goal nodes."""
    screen.fill(WHITE, (0, 100, 1920, 1080 - 100))  # Clear the area below toolbar

    # Draw edges
    for edge in edges:
        node1 = nodes[edge[0]]
        node2 = nodes[edge[1]]
        pygame.draw.line(screen, GRAY, node1, node2, EDGE_WIDTH)

    # Draw nodes
    for i, node in enumerate(nodes):
        color = GREEN if i == start_node else RED if i == goal_node else BLUE
        pygame.draw.circle(screen, color, node, NODE_RADIUS)
        pygame.draw.circle(screen, BLACK, node, NODE_RADIUS, 2)
        label = font.render(str(i), True, BLACK)
        screen.blit(label, (node[0] - 10, node[1] - 10))
