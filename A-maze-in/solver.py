from collections import deque
from typing import Dict, Tuple, List, Optional

from maze import Maze
from direction import Direction


class MazeSolver:
    """
    Solves the maze using BFS (shortest path).
    Returns path as a string of directions: NESW
    """

    def solve(self, maze: Maze) -> str:
        start = maze.entry  # (x, y)
        goal = maze.exit    # (x, y)

        queue = deque([start])

        # parent: (x, y) -> ((px, py), direction_taken)
        parent: Dict[
            Tuple[int, int], Optional[Tuple[Tuple[int, int], Direction]]
        ] = {
            start: None
        }

        while queue:
            x, y = queue.popleft()

            if (x, y) == goal:
                return self._reconstruct_path(parent, goal)

            cell = maze.get_cell(x, y)

            for direction in Direction:
                # skip ALL if you added it in enum
                if direction.name == "ALL":
                    continue

                # only move if NO wall
                if cell.has_wall(direction):
                    continue

                dx, dy = direction.delta()
                nx, ny = x + dx, y + dy

                if not maze.in_bounds(nx, ny):
                    continue

                if (nx, ny) in parent:
                    continue  # already visited

                parent[(nx, ny)] = ((x, y), direction)
                queue.append((nx, ny))

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
            path.append(direction.name)  # "N", "E", "S", "W"
            current = prev

        path.reverse()
        return "".join(path)
