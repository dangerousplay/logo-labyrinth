import enum
from dataclasses import dataclass as component
from typing import List

import glm


class Direction(enum.IntEnum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


@component
class Velocity:
    x: float
    y: float
    z: float

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def is_moving(self):
        moving = map(lambda x: x != 0, [self.x, self.y, self.z])
        return any(moving)

    def directions(self) -> List[Direction]:
        directions = []

        if self.x > 0:
            directions.append(Direction.RIGHT)
        elif self.x < 0:
            directions.append(Direction.LEFT)
        if self.y > 0:
            directions.append(Direction.UP)
        elif self.y < 0:
            directions.append(Direction.DOWN)

        return directions


@component
class Position:
    pos: glm.vec3

    def __init__(self, x, y, z):
        self.pos = glm.vec3(x, y, z)

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, value: float):
        self.pos[0] = value

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, value: float):
        self.pos[1] = value

    @property
    def z(self):
        return self.pos[2]

    @z.setter
    def z(self, value: float):
        self.pos[2] = value

    def distance(self, other) -> float:
        return glm.distance2(self.pos, other.pos)


@component
class Scale:
    x: float
    y: float
    z: float

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

@component
class Collider:
    pass
