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

def bfs(draw_graph):
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

        draw_graph()
        highlight_visited_nodes(visited)
        pygame.display.update()
        pygame.time.wait(300)

def dfs(draw_graph):
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

        draw_graph()
        highlight_visited_nodes(visited)
        pygame.display.update()
        pygame.time.wait(300)

def ucs(draw_graph):
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

        draw_graph()
        highlight_visited_nodes(visited)
        pygame.display.update()
        pygame.time.wait(300)

def greedy_search(draw_graph):
    """Perform Greedy Best-First Search."""
    start = context.start_node
    goals = context.goal_nodes
    if start is None or not goals:
        return

    priority_queue = []
    heapq.heappush(priority_queue, (context.heuristics.get(start, float('inf')), start))  # (heuristic value, node)
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
                heapq.heappush(priority_queue, (context.heuristics.get(neighbor, float('inf')), neighbor))
                if neighbor not in came_from:
                    came_from[neighbor] = current_node

        draw_graph()
        highlight_visited_nodes(visited)
        pygame.display.update()
        pygame.time.wait(300)

def a_star(draw_graph):
    """Perform A* Search."""
    start = context.start_node
    goals = context.goal_nodes
    if start is None or not goals:
        return

    priority_queue = []
    start_h = context.heuristics.get(start, float('inf'))
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
                    f_cost = tentative_g_cost + context.heuristics.get(neighbor, float('inf'))
                    came_from[neighbor] = current_node
                    heapq.heappush(priority_queue, (f_cost, tentative_g_cost, neighbor))

        draw_graph()
        highlight_visited_nodes(visited)
        pygame.display.update()
        pygame.time.wait(300)

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
    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]
        current_pos = get_node_pos(current_node)
        next_pos = get_node_pos(next_node)
        if current_pos and next_pos:
            pygame.draw.line(
                settings.screen,
                settings.GREEN,
                current_pos,
                next_pos,
                settings.EDGE_WIDTH + 2,
            )
    pygame.display.update()
    pygame.time.wait(1000)

def highlight_visited_nodes(visited):
    """Highlight the visited nodes during the search."""
    for node_id in visited:
        pos = get_node_pos(node_id)
        if pos:
            pygame.draw.circle(settings.screen, settings.YELLOW, pos, settings.NODE_RADIUS)
