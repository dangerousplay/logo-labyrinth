from functools import cache

import esper
import glm

from ..component.motion import Position, Velocity, Direction
from ..component.player import Player
from ..component.render import Renderable, WalkAnimation
from ...gfx import Texture


@cache
def _player_texture_():
    return Texture("game/textures/yoshi/walk_down/1.png", flip=True)


@cache
def _create_renderable_():
    return Renderable(
        _player_texture_(),
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


@cache
def _walk_animation_():
    return WalkAnimation(animations={
        Direction.DOWN: "game/textures/yoshi/walk_down",
        Direction.UP: "game/textures/yoshi/walk_up",
        Direction.LEFT: "game/textures/yoshi/walk_left",
        Direction.RIGHT: "game/textures/yoshi/walk_right",
    })


def create_player(world: esper.World, x: float, y: float):
    return world.create_entity(
        _create_renderable_(),
        Position(x, y, 0), Velocity(0.0, 0.0, 0.0),
        _walk_animation_(),
        Player()
    )
