import esper

from ..component.motion import Velocity, Position, Collider


class MovementProcessor(esper.Processor):

    def process(self, delta_time):
        for ent, (vel, pos) in self.world.get_components(Velocity, Position):
            pos.x += vel.x
            pos.y += vel.y
            pos.z += vel.z


class CollisionProcessor(esper.Processor):
    def process(self, delta_time):
        for ent_a, ([velocity, pos_a]) in self.world.get_components(Velocity, Position):

            if not velocity.is_moving():
                continue

            for ent_b, ([pos_b]) in self.world.get_components(Position):

                if ent_b == ent_a:
                    continue

                distance = pos_a.distance(pos_b)

                if distance < 1:
                    pos_a.x -= velocity.x
                    pos_a.y -= velocity.y
                    pos_a.z -= velocity.z