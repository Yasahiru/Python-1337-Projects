from typing import List
from .cell import Cell


class Maze:
    """Represents the maze grid."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.grid: List[List[Cell]] = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]

    """Return the cell at the given coordinates."""
    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    """Check if coordinates are inside the maze."""
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
