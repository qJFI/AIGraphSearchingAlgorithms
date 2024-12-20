# algorithms.py
import pygame
import heapq
from queue import Queue
import context
import settings
from DrawScene import draw_graph

def get_node_pos(node_id):
    """Retrieve the position (x, y) of a node given its id."""
    for node in context.nodes:
        if node[2] == node_id:
            return (node[0], node[1])
    return None

def highlight_nodes(visited, fringe):
    """Highlight visited and fringe nodes during the search."""
    VISITED_NODE_COLOR = settings.get_color('VISITED_NODE_COLOR')
    FRINGE_NODE_COLOR = settings.get_color('FRINGE_NODE_COLOR')
    NODE_RADIUS = settings.NODE_RADIUS
    screen = settings.screen

    # Highlight visited nodes
    for node_id in visited:
        pos = get_node_pos(node_id)
        if pos:
            pygame.draw.circle(screen, VISITED_NODE_COLOR, pos, NODE_RADIUS)

    # Highlight fringe nodes
    for node_id in fringe:
        pos = get_node_pos(node_id)
        if pos and node_id not in visited:
            pygame.draw.circle(screen, FRINGE_NODE_COLOR, pos, NODE_RADIUS)

def reconstruct_path(came_from, start, goal):
    """Reconstruct the path from start to goal."""
    current = goal
    path = [current]
    while current != start:
        current = came_from.get(current)
        if current is None:
            break
        path.append(current)

    path.reverse()

    # Draw the final path
    draw_graph()
    PATH_COLOR = settings.get_color('PATH_COLOR')
    EDGE_WIDTH = settings.EDGE_WIDTH
    screen = settings.screen

    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]
        current_pos = get_node_pos(current_node)
        next_pos = get_node_pos(next_node)
        if current_pos and next_pos:
            pygame.draw.line(
                screen,
                PATH_COLOR,
                current_pos,
                next_pos,
                EDGE_WIDTH + 2,
            )
    pygame.display.flip()
    pygame.time.wait(1000)

def bfs():
    """Perform Breadth-First Search."""
    start = context.start_node
    goals = context.goal_nodes
    if start is None or not goals:
        return

    queue = Queue()
    queue.put(start)
    visited = set()
    came_from = {}

    while not queue.empty():
        current = queue.get()

        if current in visited:
            continue

        visited.add(current)

        if current in goals:
            reconstruct_path(came_from, start, current)
            return  # Stop the search upon reaching the first goal

        for edge in context.edges:
            neighbor = None
            if edge[0] == current:
                neighbor = edge[1]
            elif edge[1] == current:
                neighbor = edge[0]
            if neighbor is not None and neighbor not in visited:
                queue.put(neighbor)
                if neighbor not in came_from:
                    came_from[neighbor] = current

        # Extract current fringe nodes from the queue
        fringe = list(queue.queue)

        draw_graph()
        highlight_nodes(visited, fringe)
        pygame.display.flip()
        pygame.event.pump()
        pygame.time.wait(1500)

def dfs():
    """Perform Depth-First Search."""
    start = context.start_node
    goals = context.goal_nodes
    if start is None or not goals:
        return

    stack = [start]
    visited = set()
    came_from = {}

    while stack:
        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)

        if current in goals:
            reconstruct_path(came_from, start, current)
            return  # Stop the search upon reaching the first goal

        for edge in context.edges:
            neighbor = None
            if edge[0] == current:
                neighbor = edge[1]
            elif edge[1] == current:
                neighbor = edge[0]
            if neighbor is not None and neighbor not in visited:
                stack.append(neighbor)
                if neighbor not in came_from:
                    came_from[neighbor] = current

        # Extract current fringe nodes from the stack
        fringe = list(stack)

        draw_graph()
        highlight_nodes(visited, fringe)
        pygame.display.flip()
        pygame.event.pump()
        pygame.time.wait(1500) #s


def ucs():
    """Perform Uniform Cost Search."""
    start = context.start_node
    goals = context.goal_nodes
    if start is None or not goals:
        return

    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (cost, node)
    came_from = {}
    cost_so_far = {start: 0}
    visited = set()

    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node in goals:
            reconstruct_path(came_from, start, current_node)
            return  # Stop the search upon reaching the first goal

        for edge in context.edges:
            neighbor = None
            if edge[0] == current_node:
                neighbor = edge[1]
            elif edge[1] == current_node:
                neighbor = edge[0]
            if neighbor is not None:
                new_cost = current_cost + edge[2]
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_cost, neighbor))

        # Extract current fringe nodes from the priority queue
        fringe = [node for (_, node) in priority_queue]

        draw_graph()
        highlight_nodes(visited, fringe)
        pygame.display.flip()
        pygame.event.pump()
        pygame.time.wait(1500)

def greedy_search():
    """Perform Greedy Best-First Search."""
    start = context.start_node
    goals = context.goal_nodes
    heuristics = context.heuristics
    if start is None or not goals:
        return

    priority_queue = []
    heapq.heappush(priority_queue, (heuristics.get(start, float('inf')), start))
    came_from = {}
    visited = set()

    while priority_queue:
        _, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node in goals:
            reconstruct_path(came_from, start, current_node)
            return  # Stop the search upon reaching the first goal

        for edge in context.edges:
            neighbor = None
            if edge[0] == current_node:
                neighbor = edge[1]
            elif edge[1] == current_node:
                neighbor = edge[0]
            if neighbor is not None and neighbor not in visited:
                heapq.heappush(priority_queue, (heuristics.get(neighbor, float('inf')), neighbor))
                if neighbor not in came_from:
                    came_from[neighbor] = current_node

        # Extract current fringe nodes from the priority queue
        fringe = [node for (_, node) in priority_queue]

        draw_graph()
        highlight_nodes(visited, fringe)
        pygame.display.flip()
        pygame.event.pump()
        pygame.time.wait(1500)

def a_star():
    """Perform A* Search."""
    start = context.start_node
    goals = context.goal_nodes
    heuristics = context.heuristics
    if start is None or not goals:
        return

    priority_queue = []
    start_h = heuristics.get(start, float('inf'))
    heapq.heappush(priority_queue, (start_h, 0, start))  # (f_cost, g_cost, node)
    came_from = {}
    g_costs = {start: 0}
    visited = set()

    while priority_queue:
        _, current_g_cost, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node in goals:
            reconstruct_path(came_from, start, current_node)
            return  # Stop the search upon reaching the first goal

        for edge in context.edges:
            neighbor = None
            if edge[0] == current_node:
                neighbor = edge[1]
            elif edge[1] == current_node:
                neighbor = edge[0]
            if neighbor is not None:
                tentative_g_cost = current_g_cost + edge[2]
                if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristics.get(neighbor, float('inf'))
                    came_from[neighbor] = current_node
                    heapq.heappush(priority_queue, (f_cost, tentative_g_cost, neighbor))

        # Extract current fringe nodes from the priority queue
        fringe = [node for (_, _, node) in priority_queue]

        draw_graph()
        highlight_nodes(visited, fringe)
        pygame.display.flip()
        pygame.event.pump()
        pygame.time.wait(1500)

