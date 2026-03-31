from typing import List, Tuple
from model.cell import Cell
from direction import Direction
import time


class Maze:
    """Represents the maze grid."""

    def __init__(
        self, width: int, height: int,
        entry: int, _exit: int, perfect: bool
    ) -> None:

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = _exit
        self.perfect = perfect

        self.grid: List[List[Cell]] = []
        self.initialize_grid()

    def initialize_grid(self) -> None:
        """ initializing the grid """
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell(x, y))
            self.grid.append(row)

    def reset_maze(self) -> None:
        """Full reset: reset visited status AND restore all walls."""
        from direction import ALL_DIRECTIONS
        for row in self.grid:
            for cell in row:
                cell.visited = False
                cell.walls = ALL_DIRECTIONS

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

        """ Remove walls between two adjacent cells in the given direction."""
        cell.remove_wall(direction)
        neighbor.remove_wall(direction.opposite())


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
