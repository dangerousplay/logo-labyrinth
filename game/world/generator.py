import esper
import glm
import numpy as np
from mazelib import Maze
from mazelib.generate.GrowingTree import GrowingTree
from mazelib.generate.Prims import Prims
import matplotlib.pyplot as plt
from mazelib.solve.ShortestPath import ShortestPath

from game.ecs.entity import wall, path, player
from game.ecs.processor.motion import MovementProcessor, CollisionProcessor
from game.ecs.processor.render import RenderProcessor, AnimationProcessor


def generate_world(x: int, y: int):
    m = Maze()
    m.generator = GrowingTree(x, y)
    m.solver = ShortestPath()
    m.generate_monte_carlo(repeat=5, entrances=5)

    show_png(m.grid)

    world = create_world(x, y)

    generate_walls(world, m.grid)

    player_entity = None

    if len(m.solutions) > 0:
        solution = m.solutions[0]
        start = solution[0]
        end = solution[-1]

        player_entity = player.create_player(world, start[0], start[1])
        path.create_path(world, end[0], end[1])

    return world, player_entity


def create_world(x: int, y: int):
    world = esper.World()

    world_size = glm.ortho(-10, 20 + x, -10, 20 + y)

    world.add_processor(CollisionProcessor())
    world.add_processor(MovementProcessor(), 1)
    world.add_processor(AnimationProcessor(), 2)
    world.add_processor(RenderProcessor(world_size=world_size), 3)

    return world


def _wall_positions_(grid: np.ndarray):
    for y, walls in enumerate(grid):
        for x, wall in enumerate(walls):
            if wall:
                yield x, y


def generate_walls(world: esper.World, grid: np.ndarray):
    for x, y in _wall_positions_(grid):
        wall.create_wall(world, x, y)


def generate_solution(world: esper.World, grid: np.ndarray):
    for x, y in grid:
        path.create_path(world, x, y)


def show_png(grid):
    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()