import esper
import glm
import numpy as np
import pyrr
from mazelib import Maze
from mazelib.generate.GrowingTree import GrowingTree
from mazelib.generate.Prims import Prims
import matplotlib.pyplot as plt
from mazelib.solve.ShortestPath import ShortestPath
from moderngl_window.scene import Camera
from pyphysx import Scene, RigidStatic, Material
from pyrr import Vector3

from game.ecs.entity import wall, player, chest, ship, beach
from game.ecs.processor.end import EndProcessor
from game.ecs.processor.physics import PhysicsProcessor
from game.ecs.processor.render import RenderProcessor


def generate_world(x: int, z: int, camera=Camera()):
    m = Maze()
    m.generator = GrowingTree(x, z)
    m.solver = ShortestPath()
    m.generate_monte_carlo(repeat=5, entrances=5)

    # show_png(m.grid)

    scene = Scene()

    scene.add_actor(
        RigidStatic.create_plane(material=Material(static_friction=0.1, dynamic_friction=0.1, restitution=0.5))
    )

    world = create_world(scene, x, z)

    space = 2.5

    generate_walls(world, scene, m.grid, space)

    _create_landscape_(world, scene)

    if len(m.solutions) > 0:
        solution = m.solutions[0]
        start = solution[0]
        end = solution[-1]

        player_position = Vector3([start[0] * space, 0, start[1] * space])

        player.create(world, scene, player_position, camera)
        chest.create(world, scene, Vector3([end[0] * space, 0.0, end[1] * space]))

    return world, scene


def _create_landscape_(world: esper.World, scene: Scene):
    ship.create(world, scene, Vector3([3, 0, -20]))
    beach.create(world, scene, Vector3([0, 0, 0]))


def create_world(scene: Scene, x: int, z: int):
    world = esper.World()

    world.add_processor(EndProcessor(), 3)
    world.add_processor(PhysicsProcessor(scene))
    world.add_processor(RenderProcessor(world), 4)

    return world


def _wall_positions_(grid: np.ndarray):
    for z, walls in enumerate(grid):
        for x, wall in enumerate(walls):
            if wall:
                yield x, z


def generate_walls(world: esper.World, scene: Scene, grid: np.ndarray, space: float):
    for x, z in _wall_positions_(grid):
        wall.create(world, scene, Vector3([x * space, 0, z * space]), space)


def show_png(grid):
    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()