# settings.py
import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080
NODE_RADIUS = 20
EDGE_WIDTH = 3
TOOLBAR_HEIGHT = 100

# New Color Scheme
BACKGROUND_COLOR = (10, 10, 50)        # Dark Blue
BUTTON_COLOR = (0, 0, 128)             # Navy Blue
BUTTON_HIGHLIGHT_COLOR = (25, 25, 112) # Midnight Blue
NODE_COLOR = (30, 144, 255)            # Dodger Blue
EDGE_COLOR = (70, 130, 180)            # Steel Blue
FONT_COLOR = (255, 255, 255)           # White
VISITED_NODE_COLOR = (255, 215, 0)     # Gold
PATH_COLOR = (0, 255, 0)               # Lime
TOOLBAR_COLOR = (15, 15, 70)           # Slightly lighter dark blue
START_NODE_COLOR = (0, 255, 127)       # Spring Green
GOAL_NODE_COLOR = (255, 69, 0)         # Orange Red
INPUT_BOX_COLOR = (50, 50, 100)        # Darker Blue

# Pygame setup
infoObject = pygame.display.Info()  # Get real screen size to adjust window size
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h - 50), pygame.RESIZABLE)
pygame.display.set_caption("Interactive Graph Visualizer")

# Load a gaming-style font
# You need to have the font file in your project directory
font_name = "Orbitron-Regular.ttf"  # Ensure this font file exists
try:
    font = pygame.font.Font(font_name, 24)
except:
    # Fallback if the font is not found
    font = pygame.font.SysFont('Arial', 24)

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

# Input box for entering values
input_box = pygame.Rect(300, 500, 140, 32)
