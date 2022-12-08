import esper
from pyrr import Vector3

from game.ecs.component.scene import Light


def create(world: esper.World, position: Vector3, color=Vector3([1, 1, 1]), attenuation=Vector3([1, 0, 0])):
    light = Light(position=position, color=color, attenuation=attenuation)
    return world.create_entity(light), light
