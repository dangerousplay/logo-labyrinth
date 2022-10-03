from functools import cache

import esper
import glm

from game.ecs.component.goal import Goal
from game.ecs.component.motion import Position
from game.ecs.component.render import Renderable
from game.gfx import Texture


@cache
def _goal_texture_():
    return Texture("game/textures/flag.png", flip=True)


@cache
def _create_goal_renderable_():
    return Renderable(
        _goal_texture_(),
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
            1, 1,
            1, 0.0,
            0.0, 0.0,
            0.0, 1
        )
    )


def create_goal(world: esper.World, x: float, y: float):
    position = Position(x, y, 0)

    return world.create_entity(_create_goal_renderable_(), Goal(position), position)

