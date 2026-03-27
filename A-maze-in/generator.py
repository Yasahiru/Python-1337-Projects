import random
import time
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
        rate = 0.2

        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)

                for direction in Direction:
                    if direction.name == "ALL":
                        continue

                    dx, dy = direction.delta()
                    nx, ny = x + dx, y + dy

                    if not maze.in_bounds(nx, ny):
                        continue

                    if not cell.has_wall(direction):
                        continue

                    if random.random() >= rate:
                        continue

                    if self._creates_open_area_3x3(maze, x, y, direction):
                        continue

                    neighbor = maze.get_cell(nx, ny)
                    maze.remove_wall_between(cell, neighbor, direction)

    def _creates_open_area_3x3(
        self, maze: Maze, x: int, y: int, direction: Direction
    ) -> bool:
        dx, dy = direction.delta()
        # nx, ny = x + dx, y + dy

        # simulate removal
        test_cells = []
        for yy in range(y - 1, y + 2):
            for xx in range(x - 1, x + 2):
                if maze.in_bounds(xx, yy):
                    test_cells.append((xx, yy))
        open_count = 0
        for (cx, cy) in test_cells:
            cell = maze.get_cell(cx, cy)
            walls = 0
            for d in (Direction.N, Direction.E, Direction.S, Direction.W):
                if cell.has_wall(d):
                    walls += 1
            if walls <= 1:
                open_count += 1
        return open_count >= 6  # heuristic threshold

    def print_maze(
        self, maze: Maze, path: str = "", animate: bool = False
    ) -> None:

        # 🎨 COLORS
        WALL = "\033[42m  \033[0m"   # green
        PATH = "\033[44m  \033[0m"   # blue
        EMPTY = "  "
        START = "\033[45m  \033[0m"
        END = "\033[41m  \033[0m"

        H = maze.height * 2 + 1
        W = maze.width * 2 + 1

        canvas = [[WALL for _ in range(W)] for _ in range(H)]

        # 🪜 CARVE PATHS (THIS IS THE IMPORTANT PART)
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)

                cy = y * 2 + 1
                cx = x * 2 + 1

                canvas[cy][cx] = EMPTY  # cell itself

                for d in (Direction.N, Direction.E, Direction.S, Direction.W):
                    if not cell.has_wall(d):
                        dx, dy = d.delta()
                        canvas[cy + dy][cx + dx] = EMPTY  # open passage

        # 🪜 BUILD PATH
        path_cells = []
        x, y = maze.entry
        path_cells.append((x, y))

        for move in path:
            d = Direction[move]
            dx, dy = d.delta()
            x += dx
            y += dy
            path_cells.append((x, y))

        # 🪜 ANIMATION
        def draw(step=None):
            print("\033[H\033[J", end="")

            for y in range(H):
                for x in range(W):

                    # convert to maze cell
                    if y % 2 == 1 and x % 2 == 1:
                        mx, my = x // 2, y // 2

                        if (mx, my) == maze.entry:
                            print(START, end="")
                            continue
                        if (mx, my) == maze.exit:
                            print(END, end="")
                            continue

                        if step is not None and (mx, my) in path_cells[:step]:
                            print(PATH, end="")
                            continue

                    print(canvas[y][x], end="")
                print()

        if animate:
            for i in range(len(path_cells) + 1):
                draw(i)
                time.sleep(0.03)
        else:
            draw()
