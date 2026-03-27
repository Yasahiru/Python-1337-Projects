from generator import MazeGenerator
from maze import Maze
from config_parser import Config
from solver import MazeSolver
import sys
import curses
import time


def draw_maze(stdscr, maze, path, color_mode=0):
    from direction import Direction

    # Use color_mode to change the "Wall" color pair
    # Mode 0: Green, Mode 1: Blue, Mode 2: Red (example)
    if color_mode == 0:
        wall_pair = curses.color_pair(1)
    else:
        wall_pair = curses.color_pair(2)

    if color_mode == 1:
        wall_pair = curses.color_pair(2)
    else:
        wall_pair = curses.color_pair(3)

    WALL_CHAR = "#"
    PATH_CHAR = "  "

    H, W = maze.height * 2 + 1, maze.width * 2 + 1

    # 1. Draw Walls
    for y in range(H):
        for x in range(W):
            stdscr.addstr(y, x * 2, WALL_CHAR * 2, wall_pair)

    # 2. Carve Paths (Empty spaces)
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            cy, cx = y * 2 + 1, x * 2 + 1
            stdscr.addstr(cy, cx * 2, PATH_CHAR)

            for d in Direction:
                if d.name == "ALL":
                    continue
                if not cell.has_wall(d):
                    dx, dy = d.delta()
                    stdscr.addstr(cy + dy, (cx + dx) * 2, PATH_CHAR)

    # 3. Draw the Solution Path (The blue line)
    if path:
        curr_x, curr_y = maze.entry
        # Start cell
        stdscr.addstr(
            curr_y * 2 + 1, (curr_x * 2 + 1) * 2, PATH_CHAR,
            curses.color_pair(2)
        )
        for move in path:
            d = Direction[move]
            dx, dy = d.delta()
            # Draw corridor AND next cell
            stdscr.addstr(
                curr_y * 2 + 1 + dy,
                (curr_x * 2 + 1 + dx) * 2, PATH_CHAR, curses.color_pair(2))
            curr_x, curr_y = curr_x + dx, curr_y + dy
            stdscr.addstr(
                curr_y * 2 + 1,
                (curr_x * 2 + 1) * 2, PATH_CHAR, curses.color_pair(2))

    # 4. Draw Entry/Exit
    sx, sy = maze.entry
    ex, ey = maze.exit
    stdscr.addstr(sy * 2 + 1, (sx * 2 + 1) * 2, " S", curses.color_pair(4))
    stdscr.addstr(ey * 2 + 1, (ex * 2 + 1) * 2, " E", curses.color_pair(3))


def animate_path(stdscr, maze, path):
    from direction import Direction

    x, y = maze.entry

    for move in path:
        d = Direction[move]
        dx, dy = d.delta()
        x += dx
        y += dy

        stdscr.addstr(y * 2 + 1, (x * 2 + 1) * 2, ".", curses.color_pair(2))
        stdscr.refresh()
        time.sleep(0.02)


def run_app(stdscr, maze, generator, solver):
    curses.curs_set(0)
    curses.start_color()

    # Define color pairs for different modes
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Mode 0
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Mode 1 / Path
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)   # Mode 2 / Exit
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Start

    path = ""
    needs_regen = True
    color_mode = 0

    while True:
        stdscr.clear()

        if needs_regen:
            maze.reset_visits()
            generator.generate(maze)
            path = solver.solve(maze)
            needs_regen = False

        draw_maze(stdscr, maze, path, color_mode)

        stdscr.addstr(0, 0, "1:regen  2:color  a:animate  q:quit")

        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('1'):
            needs_regen = True

        elif key == ord('2'):
            color_mode = (color_mode + 1) % 3

        elif key == ord('q'):
            break

        elif key == ord('a'):
            animate_path(stdscr, maze, path)


def main():
    if (len(sys.argv) == 2):
        conf = Config()
        conf.load(sys.argv[1])
        maze = Maze(
            conf.width,
            conf.height,
            conf.entry,
            conf.exit,
            conf.perfect,
        )
        generator = MazeGenerator()
        solver = MazeSolver()
        curses.wrapper(lambda stdscr: run_app(stdscr, maze, generator, solver))
    else:
        print("give only the confige file's name")


if __name__ == "__main__":
    main()


# if __name__ == "__main__":
#     main()
