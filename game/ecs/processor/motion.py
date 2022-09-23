import esper

from ..component.motion import Velocity, Position


class MovementProcessor(esper.Processor):

    def process(self):
        for ent, (vel, pos) in self.world.get_components(Velocity, Position):
            pos.x += vel.x
            pos.y += vel.y
            pos.z += vel.z


class CollisionProcessor(esper.Processor):
    def process(self):
        pass