from dataclasses import dataclass as component

import esper
import numpy as np
import pyrr
from moderngl_window.scene import Camera
from pyphysx import *

from game.ecs.component.physics import vector_swap_yz
from game.ecs.component.player import Player


def create(world: esper.World, physx_scene: Scene, position: pyrr.Vector3, camera: Camera):
    actor = RigidDynamic()
    actor.set_global_pose(vector_swap_yz(position))
    actor.attach_shape(Shape.create_box([1.0, 1.0, 1.0], Material(static_friction=10., restitution=1.)))
    actor.set_mass(1000)

    physx_scene.add_actor(actor)

    entity = world.create_entity(
        actor,
        Player()
    )

    world.add_component(entity, camera, Camera)
    world.add_component(entity, actor, RigidActor)
