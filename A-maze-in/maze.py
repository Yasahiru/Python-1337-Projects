from typing import List, Tuple
from cell import Cell
from direction import Direction


class Maze:
    """Represents the maze grid."""

    def __init__(
        self, width: int, height: int,
        # entry: int, exit: int
    ) -> None:

        self.width = width
        self.height = height
        # self.entry = entry
        # self.exit = exit

        self.grid: List[List[Cell]] = []
        self.initialize_grid()

    def initialize_grid(self) -> None:

        """ initializing the grid """
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell(x, y))
            self.grid.append(row)

    def get_cell(self, x: int, y: int) -> Cell:

        """ Return the cell at the given coordinates."""
        return self.grid[y][x]

    def in_bounds(self, x: int, y: int) -> bool:

        """ Check if coordinates are inside the maze."""
        return 0 <= x < self.width and 0 <= y < self.height

    def reset_visits(self):
        for row in self.grid:
            for cell in row:
                cell.visited = False

    def get_neighbors(self, cell: Cell) -> List[Tuple[Direction, Cell]]:

        """ Return all valid adjacent cells """
        neighbors: List[Tuple[Direction, Cell]] = []

        for direction in Direction:
            dx, dy = direction.delta()
            nx = cell.x + dx
            ny = cell.y + dy

            if self.in_bounds(nx, ny):
                neighbor = self.get_cell(nx, ny)
                neighbors.append((direction, neighbor))

        return neighbors

    def remove_wall_between(
        self,
        cell: Cell,
        neighbor: Cell,
        direction: Direction
    ) -> None:

        """
            Remove walls between two adjacent
            cells in the given direction.
        """
        cell.remove_wall(direction)
        neighbor.remove_wall(direction.opposite())
