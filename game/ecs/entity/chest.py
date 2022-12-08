from functools import cache

import esper
import pyrr
from pyphysx import Scene, RigidStatic, RigidActor

from game.ecs.component.goal import Goal
from game.ecs.component.physics import vector_swap_yz
from game.ecs.component.scene import Mesh


CHEST_MESH_PATH = "resources/models/treasure_chest/treasure_chest_4k.gltf"


@cache
def _chest_mesh():
    return Mesh(CHEST_MESH_PATH)


def create(world: esper.World, scene: Scene, position: pyrr.Vector3):
    actor = RigidStatic()
    actor.set_global_pose(vector_swap_yz(position))

    scene.add_actor(actor)

    mesh = _chest_mesh()

    entity = world.create_entity(mesh, Goal(position))
    world.add_component(entity, actor, RigidActor)
