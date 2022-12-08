import enum
from dataclasses import dataclass as component

import numpy
import pyrr
from pyrr import Matrix44, Vector3


def vector_swap_yz(vector: Vector3) -> Vector3:
    return Vector3([vector.x, vector.z, vector.y])


def swap_yz(vector: numpy.ndarray) -> numpy.ndarray:
    return numpy.array([vector[0], vector[2], vector[1]])


class Direction(enum.IntEnum):
    UP = enum.auto()
    DOWN = enum.auto()
    FRONT = enum.auto()
    BACK = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


@component
class Scale:
    value: pyrr.Matrix44

    def __init__(self, scale):
        self.value = Matrix44.from_scale(scale, dtype='f4')
