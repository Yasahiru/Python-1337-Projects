from collections import deque
from typing import Dict, Tuple, List, Optional
from modl.cell import Cell
from maze import Maze
from direction import Direction


class MazeSolver:
    """
    Solves the maze using BFS (shortest path).
    Returns path as a string of directions: NESW
    """

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

        # No path found (should not happen in valid maze)
        raise ValueError("No path found from entry to exit")
    def _reconstruct_path(
        self,
        parent: Dict[
            Tuple[int, int], Optional[Tuple[Tuple[int, int], Direction]]],
        goal: Tuple[int, int]
    ) -> str:
        path: List[str] = []
        current = goal

        while parent[current] is not None:
            prev, direction = parent[current]
            path.append(direction.name)
            current = prev

        path.reverse()
        return "".join(path)
