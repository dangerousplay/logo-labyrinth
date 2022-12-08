from functools import cache

import esper
import pyrr
from pyphysx import Scene, RigidStatic, RigidActor

from game.ecs.component.goal import Goal
from game.ecs.component.physics import Scale, vector_swap_yz
from game.ecs.component.scene import Mesh


BEACH_MESH_PATH = "resources/models/beach/ilha_nova3.glb"


@cache
def _beach_mesh():
    return Mesh(BEACH_MESH_PATH)


def create(world: esper.World, scene: Scene, position: pyrr.Vector3):
    actor = RigidStatic()
    actor.set_global_pose(vector_swap_yz(position))

    scene.add_actor(actor)

    mesh = _beach_mesh()

    entity = world.create_entity(mesh, Scale([2.0, 1.0, 2.0]))
    world.add_component(entity, actor, RigidActor)
