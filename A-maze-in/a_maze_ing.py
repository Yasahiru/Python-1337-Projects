from generator import MazeGenerator
from maze import Maze


# ------------------ Run Example ------------------
def main():
    maze = Maze(6, 5,)
    generator = MazeGenerator()
    generator.generate(maze)

    generator.print_maze(maze)


if __name__ == "__main__":
    main()
