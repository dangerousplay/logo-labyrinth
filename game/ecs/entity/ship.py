import os.path
from functools import cache

import esper
import pyrr
from pyphysx import Scene, RigidStatic, Shape, Material, RigidActor
from pyrr import Matrix44

from game.ecs.component.physics import Scale, vector_swap_yz
from game.ecs.component.scene import Mesh

SHIP_MESH = "resources/models/dutch_ship_large/dutch_ship_large_01_2k.gltf"


@cache
def _ship_mesh():
    return Mesh(SHIP_MESH)


def create(world: esper.World, physx_scene: Scene, position: pyrr.Vector3):
    actor = RigidStatic()
    actor.set_global_pose(vector_swap_yz(position))

    mesh = _ship_mesh()

    physx_scene.add_actor(actor)

    entity = world.create_entity(mesh)
    world.add_component(entity, actor, RigidActor)


