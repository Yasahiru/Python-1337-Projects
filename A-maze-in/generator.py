import random
from typing import List, Tuple
from direction import Direction

from cell import Cell
from maze import Maze


class MazeGenerator:
    """
        Generates a perfect maze using DFS
        recursive backtracking algorithm.
    """

    def generate(self, maze: Maze) -> None:
        """
            Generate a maze in-place.
        """

        start_cell: Cell = maze.get_cell(0, 0)
        stack: List[Cell] = []

        current: Cell = start_cell
        current.visited = True

        while True:
            neighbors = self._get_unvisited_neighbors(current, maze)

            if neighbors:
                direction, next_cell = self._choose_random_neighbor(neighbors)

                maze.remove_wall_between(current, next_cell, direction)

                stack.append(current)

                current = next_cell
                current.visited = True

            elif stack:
                current = stack.pop()

            else:
                break

        if not maze.perfect:
            self._add_imperfections(maze)

    def _get_unvisited_neighbors(
        self, cell: Cell, maze: Maze
    ) -> List[Tuple[Direction, Cell]]:

        neighbors = maze.get_neighbors(cell)
        result = []

        for direction, neighbor in neighbors:
            if not neighbor.visited:
                result.append((direction, neighbor))

        return result

    def _choose_random_neighbor(
        self, neighbors: List[Tuple[Direction, Cell]]
    ) -> Tuple[Direction, Cell]:

        """ Select a random neighbor from the list. """
        return random.choice(neighbors)

    def _add_imperfections(self, maze: Maze) -> None:
        imperfection_rate: float = 0.2

        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)

                for direction in (Direction.E, Direction.S):
                    dx, dy = direction.delta()
                    nx, ny = x + dx, y + dy

                    if not maze.in_bounds(nx, ny):
                        continue

                    neighbor = maze.get_cell(nx, ny)
                    if not cell.has_wall(direction):
                        continue

                    # # 🧠 NEW SAFETY CHECK
                    # if maze._creates_open_area_3x2_or_2x3(
                    #     maze, x, y, direction
                    # ):
                    #     continue

                    if random.random() < imperfection_rate:
                        maze.remove_wall_between(cell, neighbor, direction)

    def print_maze(self, maze: Maze) -> None:
        rows = maze.height * 2 + 1
        cols = maze.width * 4 + 1

        # 🧱 Canvas
        canvas = [[" " for _ in range(cols)] for _ in range(rows)]

        # 🪜 Corners
        for r in range(0, rows, 2):
            for c in range(0, cols, 4):
                canvas[r][c] = "╬"

        # 🪜 Walls
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)

                r = y * 2
                c = x * 4

                if cell.has_wall(Direction.N):
                    for i in range(1, 4):
                        canvas[r][c + i] = "═"

                if cell.has_wall(Direction.S):
                    for i in range(1, 4):
                        canvas[r + 2][c + i] = "═"

                if cell.has_wall(Direction.W):
                    canvas[r + 1][c] = "║"

                if cell.has_wall(Direction.E):
                    canvas[r + 1][c + 4] = "║"
                # 🪜 Fix outer borders (replace ╬ with proper chars)

                # Corners
                canvas[0][0] = "╔"
                canvas[0][cols - 1] = "╗"
                canvas[rows - 1][0] = "╚"
                canvas[rows - 1][cols - 1] = "╝"

                # Top border
                for c in range(4, cols - 1, 4):
                    canvas[0][c] = "╦"

                # Bottom border
                for c in range(4, cols - 1, 4):
                    canvas[rows - 1][c] = "╩"

                # Left border
                for r in range(2, rows - 1, 2):
                    canvas[r][0] = "╠"

                # Right border
                for r in range(2, rows - 1, 2):
                    canvas[r][cols - 1] = "╣"
        # 🪜 ENTRY / EXIT (FIXED)
        entry_x, entry_y = maze.entry
        exit_x, exit_y = maze.exit

        # 🔹 Open ENTRY wall
        if entry_y == 0:  # top
            canvas[0][entry_x * 4 + 2] = " "
        elif entry_y == maze.height - 1:  # bottom
            canvas[rows - 1][entry_x * 4 + 2] = " "
        elif entry_x == 0:  # left
            canvas[entry_y * 2 + 1][0] = " "
        elif entry_x == maze.width - 1:  # right
            canvas[entry_y * 2 + 1][cols - 1] = " "

        # 🔹 Open EXIT wall
        if exit_y == 0:
            canvas[0][exit_x * 4 + 2] = " "
        elif exit_y == maze.height - 1:
            canvas[rows - 1][exit_x * 4 + 2] = " "
        elif exit_x == 0:
            canvas[exit_y * 2 + 1][0] = " "
        elif exit_x == maze.width - 1:
            canvas[exit_y * 2 + 1][cols - 1] = " "

        # 🪜 Mark S / E inside maze
        canvas[entry_y * 2 + 1][entry_x * 4 + 2] = "S"
        canvas[exit_y * 2 + 1][exit_x * 4 + 2] = "E"

        # 🪜 Print
        for row in canvas:
            print("".join(row))
