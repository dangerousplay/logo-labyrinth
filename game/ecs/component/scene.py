import os.path
from abc import abstractmethod
from functools import cache

import numpy
from moderngl_window import resources
from moderngl_window.meta import SceneDescription

from dataclasses import dataclass as component

from moderngl_window.scene import MeshProgram
from moderngl_window.scene.programs import TextureLightProgram, TextureProgram, VertexColorProgram, \
    TextureVertexColorProgram, ColorLightProgram, FallbackProgram
from pyrr import Vector3


@cache
def default_programs():
    return [
        TextureLightProgram(),
        TextureProgram(),
        VertexColorProgram(),
        TextureVertexColorProgram(),
        ColorLightProgram(),
        FallbackProgram(),
    ]


@component
class Renderable:

    @abstractmethod
    def draw(
        self,
        projection_matrix: numpy.ndarray = None,
        camera_matrix: numpy.ndarray = None,
        program: MeshProgram = None,
        time=0.0
    ):
        pass


@component
class Mesh(Renderable):
    def __init__(self, scene_file: str):
        self.mesh = resources.scenes.load(
            SceneDescription(
                path=os.path.abspath(scene_file),
            )
        )

    def draw(
        self,
        projection_matrix: numpy.ndarray = None,
        camera_matrix: numpy.ndarray = None,
        program: MeshProgram = None,
        time=0.0
    ):
        if program:
            self.mesh.apply_mesh_programs([program] + default_programs())

        self.mesh.draw(
            projection_matrix=projection_matrix,
            camera_matrix=camera_matrix,
            time=time
        )


@component
class Light:
    attenuation: Vector3
    color: Vector3
    position: Vector3
