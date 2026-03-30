import random
from maze import Maze
from model.cell import Cell
from collections import deque
from model.generator import Generator
from typing import Dict, List, Optional, Tuple
from direction import Direction, ALL_DIRECTIONS


# Helper to prevent large open areas
def can_remove_wall(maze: Maze, neighbor: Cell) -> bool:
    """Returns True if removing the wall won't create an open area > 2x2."""
    open_count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = neighbor.x + dx, neighbor.y + dy
            if maze.in_bounds(nx, ny):
                n = maze.get_cell(nx, ny)
                if n.walls != ALL_DIRECTIONS:
                    open_count += 1
    return open_count < 3


class DFSMazeGenerator(Generator):
    def generate(self, maze: Maze, seed=None) -> None:
        if seed is not None:
            random.seed(seed)
        maze.reset_visits()
        self._dfs(maze, maze.get_cell(0, 0))

    def _dfs(self, maze: Maze, cell: Cell) -> None:
        cell.visited = True
        neighbors = []
        for d, c in maze.get_neighbors(cell):
            if not c.visited:
                neighbors.append((d, c))
        random.shuffle(neighbors)

        for direction, neighbor in neighbors:
            if not neighbor.visited and can_remove_wall(maze, neighbor):
                maze.remove_wall_between(cell, neighbor, direction)
                self._dfs(maze, neighbor)


class PrimMazeGenerator(Generator):
    def generate(self, maze: Maze, seed=None) -> None:
        if seed is not None:
            random.seed(seed)
        maze.reset_visits()
        start = maze.get_cell(0, 0)
        start.visited = True

        walls: List[Tuple[Cell, Cell, Direction]] = []
        for direction, neighbor in maze.get_neighbors(start):
            walls.append((start, neighbor, direction))

        while walls:
            idx = random.randint(0, len(walls) - 1)
            cell, neighbor, direction = walls.pop(idx)
            if not neighbor.visited and can_remove_wall(maze, neighbor):
                maze.remove_wall_between(cell, neighbor, direction)
                neighbor.visited = True
                for d, n in maze.get_neighbors(neighbor):
                    if not n.visited:
                        walls.append((neighbor, n, d))


def bfs_solve(maze: Maze, start: Cell, end: Cell) -> List[Cell]:
    queue = deque([start])
    came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {
        (start.x, start.y): None
    }
    visited = set()
    visited.add((start.x, start.y))

    while queue:
        current = queue.popleft()
        if current == end:
            break

        for dir, neigh in maze.get_neighbors(current):
            if not current.has_wall(dir):
                if (neigh.x, neigh.y) not in visited:
                    queue.append(neigh)
                    visited.add((neigh.x, neigh.y))
                    came_from[(neigh.x, neigh.y)] = (current.x, current.y)

    path: List[Cell] = []
    current_coords = (end.x, end.y)
    while current_coords is not None:
        x, y = current_coords
        path.append(maze.get_cell(x, y))
        current_coords = came_from.get(current_coords)
    path.reverse()
    return path
