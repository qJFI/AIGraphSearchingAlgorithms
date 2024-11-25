# settings.py
import pygame

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
BLUE = (73, 154, 229)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (200, 200, 200)
BUTTON_HIGHLIGHT = (180, 180, 180)

infoObject = pygame.display.Info()  # get real screen size to adjust window size
# Pygame setup
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h - 50), pygame.RESIZABLE)
pygame.display.set_caption("Interactive Graph Visualizer")
font = pygame.font.SysFont('Calibri (Headings)', 24)

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
