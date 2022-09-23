
from dataclasses import dataclass as component

import glm

from game.gfx import Texture


@component
class Renderable:
    is_visible: bool
    texture: Texture
    uv_mapping: glm.array
    vertices: glm.array

    def __init__(self, texture: Texture, vertices: glm.array, uv_mapping: glm.array):
        self.vertices = vertices
        self.is_visible = True
        self.texture = texture
        self.uv_mapping = uv_mapping