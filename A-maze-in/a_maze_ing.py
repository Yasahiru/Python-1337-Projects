from generator import MazeGenerator, print_maze
from maze import Maze
from config_parser import Config
from solver import MazeSolver
from typing import List
import sys


# ------------------ Run Example ------------------
def main_loop(maze_obj: Maze, generator: MazeGenerator, solver: MazeSolver):
    show_path: bool = False
    animate: bool = False
    colors: List[str] = ["\033[42m", "\033[43m", "\033[46m", "\033[47m"]
    color: int = 0
    path: str = solver.solve(maze_obj)

    while True:
        try:
            print_maze(maze_obj, path, show_path, colors[color], animate)
            print(
                "\n1: Re-generate | 2: Show/Hide Path |"
                " 3: Change Color | 4: Animation | Q: Quit"
            )

            choice = input("Choice? ").lower()
            if choice == '1':
                maze_obj.reset_maze()
                generator.generate(maze_obj)
                path = solver.solve(maze_obj)
            elif choice == '2':
                show_path = True
            elif choice == '3':
                color = (color + 1) % len(colors)
            elif choice == '4':
                animate = not animate
            elif choice == 'q':
                break
            else:
                print("invalid key")
        except KeyboardInterrupt:
            pass


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
