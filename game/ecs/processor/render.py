import esper


class RenderProcessor(esper.Processor):
    def process(self):
        for ent, (vel, pos) in self.world.get_components(Renderable, Position):
            pos.x += vel.x
            pos.y += vel.y
            pos.z += vel.z