from typing import List, Tuple, Set
from direction import Direction, ALL_DIRECTIONS
from model.cell import Cell
from maze import Maze
import random

# 5-row x 3-col pixel bitmaps for digits '4' and '2'
DIGIT_4 = [
    [1, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 0, 1],
    [0, 0, 1],
]
DIGIT_2 = [
    [1, 1, 1],
    [0, 0, 1],
    [1, 1, 1],
    [1, 0, 0],
    [1, 1, 1],
]

DIGIT_H = 5
DIGIT_W = 3
GAP = 1
PATTERN_W = DIGIT_W + GAP + DIGIT_W
PATTERN_H = DIGIT_H


class MazeGenerator:
    """Generates a perfect maze using DFS"""

    def generate(self, maze: Maze) -> None:

        # Step 1: stamp '42' onto the fresh grid before anything else
        self._stamp_42(maze)

        # Step 2: DFS carves the maze, naturally routing around 42 cells
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

    def _stamp_42(self, maze: Maze) -> None:
        """
        Stamp the '42' pattern onto the grid before generation.

        For each cell that forms a digit:
          - walls are set to ALL_DIRECTIONS (fully closed box)
          - visited is set to True so DFS never enters it
          - shared walls between adjacent 42 cells are removed
            so the digits render as one connected solid shape

        Neighbors of stamped cells also get their facing wall closed
        so the grid is coherent from the very start.

        Prints an error and returns early if the maze is too small.
        """
        if maze.width < PATTERN_W + 2 or maze.height < PATTERN_H + 2:
            print("Error: maze is too small to display the '42' pattern.")
            maze.cells_42: Set[Tuple[int, int]] = set()
            return

        start_x = (maze.width - PATTERN_W) // 2
        start_y = (maze.height - PATTERN_H) // 2

        cells_42: Set[Tuple[int, int]] = set()

        for row in range(DIGIT_H):
            for col in range(DIGIT_W):
                if DIGIT_4[row][col]:
                    cells_42.add((start_x + col, start_y + row))
                if DIGIT_2[row][col]:
                    cells_42.add((start_x + DIGIT_W + GAP + col, start_y + row))

        # Store on maze so the renderer can look it up
        maze.cells_42 = cells_42

        # Fully wall off and pre-visit every 42 cell
        for (x, y) in cells_42:
            cell = maze.get_cell(x, y)
            cell.walls = ALL_DIRECTIONS
            cell.visited = True

        # Remove the shared wall between adjacent 42 cells so each
        # digit renders as one connected solid shape, not isolated boxes
        for (x, y) in cells_42:
            for direction in (
                Direction.N, Direction.E, Direction.S, Direction.W
            ):
                dx, dy = direction.delta()
                nx, ny = x + dx, y + dy
                if (nx, ny) in cells_42:
                    maze.get_cell(x, y).remove_wall(direction)

        # Close the facing wall on every non-42 neighbor
        # so wall coherence holds before DFS even starts
        for (x, y) in cells_42:
            for direction in (
                Direction.N, Direction.E, Direction.S, Direction.W
            ):
                dx, dy = direction.delta()
                nx, ny = x + dx, y + dy

                if not maze.in_bounds(nx, ny):
                    continue
                if (nx, ny) in cells_42:
                    continue

                maze.get_cell(nx, ny).add_wall(direction.opposite())

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

                    if maze.cells_42:
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
