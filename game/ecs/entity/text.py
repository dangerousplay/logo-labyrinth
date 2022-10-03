import esper
import glm

from game.ecs.component.motion import Position, Scale
from game.ecs.component.render import Renderable
from game.gfx import Texture


def _create_text_renderable_(texture: Texture):
    return Renderable(
        texture,
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


def create_text(world: esper.World, x: float, y: float, text: Texture, scale=Scale(1, 1, 1)):
    position = Position(x, y, 0)

    return world.create_entity(_create_text_renderable_(text), position, scale)

