import pygame
import heapq
from queue import Queue

YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
EDGE_WIDTH = 3

# Existing BFS, DFS, UCS, and Greedy Search functions

def bfs(start, goal, nodes, edges, draw_graph):
    """Perform Breadth-First Search."""
    if start is None or goal is None:
        return

    queue = Queue()
    queue.put(start)
    visited = set()
    came_from = {}

    while not queue.empty():
        current = queue.get()

        if current == goal:
            reconstruct_path(came_from, start, goal, nodes, draw_graph)
            return

        visited.add(current)
        for edge in edges:
            if edge[0] == current and edge[1] not in visited:
                queue.put(edge[1])
                visited.add(edge[1])
                came_from[edge[1]] = current
            elif edge[1] == current and edge[0] not in visited:
                queue.put(edge[0])
                visited.add(edge[0])
                came_from[edge[0]] = current

        draw_graph()
        for node in visited:
            pygame.draw.circle(pygame.display.get_surface(), YELLOW, nodes[node], 20)
        pygame.display.update()
        pygame.time.wait(300)

def dfs(start, goal, nodes, edges, draw_graph):
    """Perform Depth-First Search."""
    if start is None or goal is None:
        return

    stack = [start]
    visited = set()
    came_from = {}

    while stack:
        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            reconstruct_path(came_from, start, goal, nodes, draw_graph)
            return

        for edge in edges:
            if edge[0] == current and edge[1] not in visited:
                stack.append(edge[1])
                came_from[edge[1]] = current
            elif edge[1] == current and edge[0] not in visited:
                stack.append(edge[0])
                came_from[edge[0]] = current

        draw_graph()
        for node in visited:
            pygame.draw.circle(pygame.display.get_surface(), YELLOW, nodes[node], 20)
        pygame.display.update()
        pygame.time.wait(300)

def ucs(start, goal, nodes, edges, draw_graph):
    """Perform Uniform Cost Search."""
    if start is None or goal is None:
        return

    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (cost, node)
    visited = set()
    came_from = {}
    cost_so_far = {start: 0}

    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == goal:
            reconstruct_path(came_from, start, goal, nodes, draw_graph)
            return

        for edge in edges:
            if edge[0] == current_node or edge[1] == current_node:
                neighbor = edge[1] if edge[0] == current_node else edge[0]
                new_cost = current_cost + edge[2]

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    came_from[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_cost, neighbor))

        draw_graph()
        for node in visited:
            pygame.draw.circle(pygame.display.get_surface(), YELLOW, nodes[node], 20)
        pygame.display.update()
        pygame.time.wait(300)

def greedy_search(start, goal, nodes, edges, heuristics, draw_graph):
    """Perform Greedy Best-First Search."""
    if start is None or goal is None:
        return

    priority_queue = []
    heapq.heappush(priority_queue, (heuristics[start], start))  # (heuristic value, node)
    visited = set()
    came_from = {}

    while priority_queue:
        _, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == goal:
            reconstruct_path(came_from, start, goal, nodes, draw_graph)
            return

        for edge in edges:
            if edge[0] == current_node or edge[1] == current_node:
                neighbor = edge[1] if edge[0] == current_node else edge[0]
                if neighbor not in visited:
                    heapq.heappush(priority_queue, (heuristics.get(neighbor, float('inf')), neighbor))
                    came_from[neighbor] = current_node

        draw_graph()
        for node in visited:
            pygame.draw.circle(pygame.display.get_surface(), YELLOW, nodes[node], 20)
        pygame.display.update()
        pygame.time.wait(300)

def a_star(start, goal, nodes, edges, heuristics, draw_graph):
    """Perform A* Search."""
    if start is None or goal is None:
        return

    priority_queue = []
    heapq.heappush(priority_queue, (heuristics[start], 0, start))  # (f_cost, g_cost, node)
    visited = set()
    came_from = {}
    g_costs = {start: 0}

    while priority_queue:
        _, current_g_cost, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == goal:
            reconstruct_path(came_from, start, goal, nodes, draw_graph)
            return

        for edge in edges:
            if edge[0] == current_node or edge[1] == current_node:
                neighbor = edge[1] if edge[0] == current_node else edge[0]
                tentative_g_cost = current_g_cost + edge[2]

                if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristics.get(neighbor, float('inf'))
                    came_from[neighbor] = current_node
                    heapq.heappush(priority_queue, (f_cost, tentative_g_cost, neighbor))

        draw_graph()
        for node in visited:
            pygame.draw.circle(pygame.display.get_surface(), YELLOW, nodes[node], 20)
        pygame.display.update()
        pygame.time.wait(300)

def reconstruct_path(came_from, start, goal, nodes, draw_graph):
    """Reconstruct the path from start to goal."""
    current = goal
    while current != start:
        prev = came_from[current]
        pygame.draw.line(pygame.display.get_surface(), GREEN, nodes[current], nodes[prev], EDGE_WIDTH + 2)
        current = prev
        pygame.display.update()
        pygame.time.wait(300)
