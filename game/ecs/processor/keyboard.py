from typing import Any, List

import esper
import math

from moderngl_window.context.base import KeyModifiers, BaseKeys
from moderngl_window.scene import KeyboardCamera
from pyphysx import RigidDynamic
from pyrender import Camera
from pyrr import Vector3, Vector4

from game.ecs.component.physics import Direction, swap_yz, vector_swap_yz
from game.ecs.component.player import Player

_CHARACTER_VELOCITY = 13


def pyaw_to_vector(pitch: float, yaw: float) -> Vector4:
    xz_len = math.cos(pitch)
    x = xz_len * math.cos(yaw)
    y = math.sin(pitch)
    z = xz_len * math.sin(-yaw)

    return Vector4([x, y, z, 0])


class KeyboardProcessor(esper.Processor):
    def __init__(self):
        self.player_actor: RigidDynamic = None
        self.camera: KeyboardCamera = None
        self.direction: List[Direction] = []

    def process(self, time, camera: Camera, *args, **kwargs):
        _, (_, player_actor) = self.world.get_components(Player, RigidDynamic)[0]
        player_actor: RigidDynamic

        self.player_actor = player_actor

        player_position = swap_yz(player_actor.get_global_pose()[0])
        camera.position = Vector3(player_position)
        camera.position[1] += 1

        self.camera = camera

        self.update_player(player_actor)

    def update_player(self, player_actor):
        player_velocity = Vector3([0, 0, 0])

        for direction in self.direction:
            if direction == Direction.FRONT:
                player_velocity = player_velocity + self.camera.dir

            if direction == Direction.BACK:
                player_velocity = player_velocity - self.camera.dir

            if direction == Direction.LEFT:
                player_velocity = player_velocity - self.camera.right

            if direction == Direction.RIGHT:
                player_velocity = player_velocity + self.camera.right

        player_velocity[1] = 0
        player_actor.set_linear_velocity(vector_swap_yz(player_velocity) * _CHARACTER_VELOCITY)

    def process_key(self, keys: BaseKeys, key: Any, action: Any, modifiers: KeyModifiers):
        def update_direction(key_action, direction):
            if key_action == keys.ACTION_PRESS:
                self.direction.append(direction)
            else:
                self.direction.remove(direction)

        if key == keys.W:
            update_direction(action, Direction.FRONT)
        if key == keys.S:
            update_direction(action, Direction.BACK)
        if key == keys.A:
            update_direction(action, Direction.LEFT)
        if key == keys.D:
            update_direction(action, Direction.RIGHT)
