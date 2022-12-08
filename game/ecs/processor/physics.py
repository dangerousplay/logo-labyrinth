import esper

from pyphysx import Scene
from pyphysx_utils.rate import Rate


class PhysicsProcessor(esper.Processor):
    def __init__(self, scene: Scene, rate: Rate = Rate(60)):
        self.scene = scene
        self.rate = rate

    def process(self, *args, **kwargs):
        self.scene.simulate(self.rate.period())
        self.rate.sleep()

