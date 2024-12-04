# settings.py
import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080
NODE_RADIUS = 20
EDGE_WIDTH = 3
TOOLBAR_HEIGHT = 110  # Increased to accommodate two rows of buttons

# Mode flag
is_dark_mode = True  # Start in dark mode

# Color Schemes
dark_mode_colors = {
    'BACKGROUND_COLOR': (10, 10, 50),        # Dark Blue
    'BUTTON_COLOR': (0, 0, 128),             # Navy Blue
    'BUTTON_HIGHLIGHT_COLOR': (25, 25, 112), # Midnight Blue
    'NODE_COLOR': (30, 144, 255),            # Dodger Blue
    'EDGE_COLOR': (70, 130, 180),            # Steel Blue
    'FONT_COLOR': (255, 255, 255),           # White
    'VISITED_NODE_COLOR': (255, 215, 0),     # Gold
      'FRINGE_NODE_COLOR': (255, 140, 0),  # Dark Orange
    'PATH_COLOR': (0, 255, 0),               # Lime
    'TOOLBAR_COLOR': (15, 15, 70),           # Slightly lighter dark blue
    'START_NODE_COLOR': (0, 255, 127),       # Spring Green
    'GOAL_NODE_COLOR': (255, 69, 0),         # Orange Red
    'INPUT_BOX_COLOR': (50, 50, 100),        # Darker Blue
}

light_mode_colors = {
    'BACKGROUND_COLOR': (245, 245, 245),     # Light Gray
    'BUTTON_COLOR': (220, 220, 220),         # Light Gray
    'BUTTON_HIGHLIGHT_COLOR': (200, 200, 200),# Gray
    'NODE_COLOR': (173, 216, 230),           # Light Blue
    'EDGE_COLOR': (0, 0, 0),                 # Black
    'FONT_COLOR': (0, 0, 0),                 # Black
    'VISITED_NODE_COLOR': (255, 165, 0),     # Orange
    'FRINGE_NODE_COLOR': (255, 140, 0),  # Dark Orange
    'PATH_COLOR': (34, 139, 34),             # Forest Green
    'TOOLBAR_COLOR': (230, 230, 230),        # Light Gray
    'START_NODE_COLOR': (50, 205, 50),       # Lime Green
    'GOAL_NODE_COLOR': (220, 20, 60),        # Crimson
    'INPUT_BOX_COLOR': (255, 255, 255),      # White
}

# Function to get current color scheme
def get_color(name):
    return dark_mode_colors[name] if is_dark_mode else light_mode_colors[name]

# Pygame setup
infoObject = pygame.display.Info()  # Get real screen size to adjust window size
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h - 50), pygame.RESIZABLE)
pygame.display.set_caption("Interactive Graph Visualizer")

# Load a gaming-style font
font_name = "Orbitron-Regular.ttf"  # Ensure this font file exists
try:
    font = pygame.font.Font(font_name, 24)
except:
    # Fallback if the font is not found
    font = pygame.font.SysFont('Arial', 24)

# Toolbar Buttons
BUTTON_WIDTH = 140
BUTTON_HEIGHT = 40
BUTTON_SPACING = 10

buttons = {
    # First column buttons
    "Add Node": pygame.Rect(10, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Remove Node": pygame.Rect(10, 10 + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT),
  
    # Second column buttons
    "Move Node": pygame.Rect(160, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Reset": pygame.Rect(160, 10 + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT),
    
    # Third column buttons
    "Set Start": pygame.Rect(360, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Set Goal": pygame.Rect(360, 10 + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT),

    # Fourth column buttons
    "Add Heuristic": pygame.Rect(550, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Connect Nodes": pygame.Rect(550, 10 + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT),

    # Fifth column buttons
    "Run BFS": pygame.Rect(760, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Run DFS": pygame.Rect(760, 10 + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT),

    # Sixth column buttons
    "Run UCS": pygame.Rect(910, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Run Greedy": pygame.Rect(910, 10 + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT),

    # Seventh column buttons
    "Run A*": pygame.Rect(1060, 10, BUTTON_WIDTH, BUTTON_HEIGHT),

    # Eighth column buttons
    "Example": pygame.Rect(1600, 10, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Toggle Dark Mode": pygame.Rect(1600, 10 + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT),
}

# Input box for entering values
input_box = pygame.Rect(300, 500, 140, 32)
