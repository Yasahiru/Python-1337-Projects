from dataclasses import dataclass
from enum import IntEnum


@dataclass
class Cell:
    N, E, S, W = 1, 2, 4, 8
    x: int
    y: int
    walls: int = N | E | S | W
    visited: bool = False

    """Check if a wall exists in the given direction."""
    def has_wall(self, direction: int) -> bool:
        return bool(self.walls & direction)

    """Remove a wall from the cell."""
    def remove_wall(self, direction: int) -> None:
        self.walls &= ~direction


class Direction(IntEnum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
