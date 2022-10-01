from functools import cache

import esper
import glm

from game.ecs.component.motion import Position
from game.ecs.component.render import Renderable
from game.gfx import Texture


@cache
def _path_texture_():
    return Texture("game/textures/block/dirt.png")


@cache
def _create_path_renderable_():
    return Renderable(
        _path_texture_(),
        vertices=glm.array(
            glm.float32,
            # positions
            0.5, 0.5, 0.0,  # top right
            0.5, -0.5, 0.0,  # bottom right
            -0.5, -0.5, 0.0,  # bottom left
            -0.5, 0.5, 0.0,  # top left
        ),
        indices=glm.array(
            glm.uint32,
            0, 1, 3,  # first triangle
            1, 2, 3  # second triangle
        ),
        uv_mapping=glm.array(
            glm.float32,
            0.2, 0.2,
            0.2, 0.0,
            0.0, 0.0,
            0.0, 0.2
        )
    )


def create_path(world: esper.World, x: float, y: float):
    return world.create_entity(_create_path_renderable_(), Position(x, y, 0))