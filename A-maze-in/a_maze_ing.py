from generator import MazeGenerator
from maze import Maze
from config_parser import Config
import sys


# ------------------ Run Example ------------------
def main():
    try:
        conf = Config()
        conf.load(sys.argv[1])

        maze = Maze(conf.width, conf.height)
        generator = MazeGenerator()
        generator.generate(maze)
        generator.print_maze(maze)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
