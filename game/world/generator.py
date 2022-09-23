import numpy as np
from mazelib import Maze
from mazelib.generate.Prims import Prims
import matplotlib.pyplot as plt


def generate_world(x: int, y: int):
    m = Maze()
    m.generator = Prims(6, 6)
    m.generate()

    show_png(m.grid)


def generate_walls(grid: np.ndarray):
    pass


def show_png(grid):
    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()