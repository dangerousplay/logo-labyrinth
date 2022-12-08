from typing import List, Optional

import esper
from pyphysx import RigidActor

from game.ecs.component.goal import Goal
from game.ecs.component.physics import swap_yz
from game.ecs.component.player import Player


_TOUCH_RANGE = 1.5


class EndProcessor(esper.Processor):
    def __init__(self):
        pass

    def process(self, *args, **kwargs):

        for ent_a, ([actor, _]) in self.world.get_components(RigidActor, Player):
            for ent_b, ([goal]) in self.world.get_components(Goal):

                player_pos = swap_yz(actor.get_global_pose()[0])
                distance = goal.position - player_pos

                if distance.length < _TOUCH_RANGE:
                    esper.dispatch_event("regenerate_world", True)
