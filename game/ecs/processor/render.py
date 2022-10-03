from functools import cache

import esper
import glm
from OpenGL.GL import GL_TRIANGLES, glDrawElements, GL_UNSIGNED_INT

from game.ecs.component.motion import Position, Scale, Velocity
from game.ecs.component.render import Renderable, WalkAnimation
from game.gfx import Shader


DEFAULT_SCALE = Scale(1.0, 1.0, 1.0)


@cache
def _texture_shader_():
    return Shader('game/shaders/texture_vs.glsl', 'game/shaders/texture_fs.glsl')


class RenderProcessor(esper.Processor):

    def __init__(self, world_size: glm.fmat4x4 = glm.ortho(-10, 30, -10, 30)):
        self.world_size = world_size

    def process(self, delta_time):
        texture_shader = _texture_shader_()

        texture_shader.use()

        for ent, (render, pos) in self.world.get_components(Renderable, Position):
            render: Renderable = render
            scale = DEFAULT_SCALE

            if self.world.has_component(ent, Scale):
                scale = self.world.component_for_entity(ent, Scale)

            texture = render.texture

            projection = self.world_size

            scale = glm.scale(glm.vec3(scale.x, scale.y, scale.z))

            translation = glm.translate(glm.vec3(pos.x, pos.y, pos.z))

            texture_shader.set_uniform_texture_2d("tex", texture, 0)
            texture_shader.set_uniform_mat4("transformations",  projection * translation * scale)

            texture.use()
            texture_shader.use()

            render.use()

            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)


class AnimationProcessor(esper.Processor):

    def process(self, delta_time):
        for ent, (render, animation, velocity) in self.world.get_components(Renderable, WalkAnimation, Velocity):
            if not velocity.is_moving():
                continue

            render: Renderable = render

            direction = velocity.directions()[0]

            animation: WalkAnimation = animation
            animations = animation.animations.get(direction)

            if animations is not None:
                render.texture = next(animations)
