from functools import cache

import esper
import pyrr
from pyphysx import *

from game.ecs.component.physics import Scale, vector_swap_yz
from game.ecs.component.scene import Mesh

WALL_MESH = "resources/models/treasure_chest/treasure_chest_4k.gltf"


@cache
def _wall_mesh():
    return Mesh(WALL_MESH)


def create(world: esper.World, physx_scene: Scene, position: pyrr.Vector3, space: float):
    actor = RigidStatic()
    actor.set_global_pose(vector_swap_yz(position))
    actor.attach_shape(Shape.create_box([1.0 * space - 0.1, 1.0 * space - 0.1, 30.0], Material(dynamic_friction=1., restitution=1.)))

    mesh = _wall_mesh()

    physx_scene.add_actor(actor)

    entity = world.create_entity(mesh, Scale([2, 2, 3]))
    world.add_component(entity, actor, RigidActor)


