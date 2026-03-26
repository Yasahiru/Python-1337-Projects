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

    def print_maze(self, maze: Maze):
        for y in range(maze.height):
            # Top walls
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                print("+", end="")
                print(("---" if cell.has_wall(Direction.N) else "   "), end="")
            print("+")

            # Side walls
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                print(("|" if cell.has_wall(Direction.W) else " "), end="")
                print("   ", end="")
            print("|")

        # Bottom border
        for x in range(maze.width):
            print("+---", end="")
        print("+")
