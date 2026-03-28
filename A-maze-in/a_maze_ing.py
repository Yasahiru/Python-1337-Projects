from generator import MazeGenerator, print_maze
from config_parser import Config
from solver import MazeSolver
from maze import Maze
import sys


# ------------------ Run Example ------------------
def main_loop(maze_obj: Maze, generator: MazeGenerator, solver: MazeSolver):
    show_path = False
    colors = ["\033[42m", "\033[43m", "\033[46m", "\033[47m"]
    color_idx = 0
    path_str = solver.solve(maze_obj)

    while True:
        print_maze(maze_obj, path_str, show_path, colors[color_idx])
        print(
            "\n1: Re-generate | 2: Show/Hide Path | 3: Change Color | Q: Quit"
        )

        choice = input("Choice? ").lower()
        if choice == '1':
            maze_obj.reset_maze()
            generator.generate(maze_obj)
            path_str = solver.solve(maze_obj)
        elif choice == '2':
            show_path = not show_path
        elif choice == '3':
            color_idx = (color_idx + 1) % len(colors)
        elif choice == 'q':
            break


def main():
    try:
        conf = Config()
        conf.load(sys.argv[1])
        maze = Maze(
            conf.width, conf.height,
            conf.entry, conf.exit,
            conf.perfect
        )
        solver = MazeSolver()
        generator = MazeGenerator()
        generator.generate(maze)
        main_loop(maze_obj=maze, generator=generator, solver=solver)
        path = solver.solve(maze)
        print(path)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
