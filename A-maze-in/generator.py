import random
import time
from typing import List, Tuple

from direction import Direction
from model.cell import Cell
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
        return open_count >= 6


def print_maze(
        maze: Maze,
        path: str = "",
        show_path: bool = True,
        wall_color: str = "\033[42m",
        animate: bool = False
) -> None:
    """
    Visual representation of the maze for the terminal.
    Shows walls, entry, exit, and the solution path.
    """
    RESET = "\033[0m"
    WALL = f"{wall_color}  {RESET}"
    PATH = "\033[44m  \033[0m"
    EMPTY = "  "
    START = "\033[45m  \033[0m"
    END = "\033[41m  \033[0m"

    h_canvas, w_canvas = maze.height * 2 + 1, maze.width * 2 + 1
    canvas = [[WALL for _ in range(w_canvas)] for _ in range(h_canvas)]
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            cy, cx = y * 2 + 1, x * 2 + 1
            canvas[cy][cx] = EMPTY

            for d in (Direction.N, Direction.E, Direction.S, Direction.W):
                if not cell.has_wall(d):
                    dx, dy = d.delta()
                    canvas[cy + dy][cx + dx] = EMPTY

    path_coords: List[Tuple[int, int]] = []
    if path:
        curr_x, curr_y = maze.entry
        path_coords.append((curr_x, curr_y))
        for move in path:
            d = Direction[move]
            dx, dy = d.delta()
            curr_x, curr_y = curr_x + dx, curr_y + dy
            path_coords.append((curr_x, curr_y))

    def render(step: int = None) -> None:
        print("\033[H\033[J", end="")
        for y in range(h_canvas):
            for x in range(w_canvas):
                if y % 2 == 1 and x % 2 == 1:
                    mx, my = x // 2, y // 2
                    if (mx, my) == maze.entry:
                        print(START, end="")
                        continue
                    if (mx, my) == maze.exit:
                        print(END, end="")
                        continue
                    if show_path and path_coords:
                        limit = step if step is not None else len(path_coords)
                        if (mx, my) in path_coords[:limit]:
                            print(PATH, end="")
                            continue
                print(canvas[y][x], end="")
            print()
    if animate and show_path:
        for i in range(1, len(path_coords) + 1):
            render(i)
            time.sleep(0.05)
    else:
        render()
