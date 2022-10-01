import itertools
import os
from dataclasses import dataclass as component
from typing import Iterator

import glm
from OpenGL.GL import GL_ARRAY_BUFFER, glBindVertexArray, GL_STATIC_DRAW, GL_FLOAT, GL_FALSE, \
    GL_ELEMENT_ARRAY_BUFFER, glGenVertexArrays, glVertexAttribPointer, glEnableVertexAttribArray

from .motion import Direction
from ...gfx import Texture, create_buffer, Buffer


@component
class Renderable:
    is_visible: bool
    texture: Texture
    uv_mapping: Buffer
    vertices: Buffer
    elements_buffer: Buffer
    vao: int

    def __init__(self, texture: Texture, vertices: glm.array, indices: glm.array, uv_mapping: glm.array):
        self.is_visible = True
        self.texture = texture

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        self.vao = vao

        self.uv_mapping = create_buffer(GL_ARRAY_BUFFER, GL_STATIC_DRAW, uv_mapping)
        self.vertices = create_buffer(GL_ARRAY_BUFFER, GL_STATIC_DRAW, vertices)
        self.elements_buffer = create_buffer(GL_ELEMENT_ARRAY_BUFFER, GL_STATIC_DRAW, indices)

        self.vertices.use()

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * glm.sizeof(glm.float32), None)
        glEnableVertexAttribArray(0)

        self.uv_mapping.use()

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 2 * glm.sizeof(glm.float32), None)
        glEnableVertexAttribArray(1)

    def use(self):
        glBindVertexArray(self.vao)


@component
class WalkAnimation:
    animations: dict[Direction, Iterator[Texture]]
    current_direction: Direction

    animation_time: float
    duration: float

    def __init__(self, animations: dict[Direction, str], time=1, flip=True):
        self.animations = {}
        self.animation_time = time

        for direction, path in animations.items():
            textures = map(lambda f: os.path.join(path, f), os.listdir(path))
            textures = filter(os.path.isfile, textures)
            textures = list(map(lambda f: Texture(f, flip), textures))

            self.animations[direction] = itertools.cycle(textures)

