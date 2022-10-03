from typing import List, Optional

import esper

from game.ecs.component.goal import Goal
from game.ecs.component.motion import Velocity, Position, Scale
from game.ecs.component.player import Player
from game.ecs.entity import text
from game.gfx import Texture


ImGuiWindowFlags_NoBackground = 1 << 7


class EndProcessor(esper.Processor):
    menu: Optional[List[int]]

    def __init__(self):
        self.menu = None
        self.congratulations_texture = Texture('game/textures/text/congratulations.png', flip=True)
        self.continue_texture = Texture('game/textures/text/continue.png', flip=True)

        esper.set_handler("mouse_click", self._mouse_click_)

    def _mouse_click_(self, x, y, button):
        if self.menu is None:
            return

        # TODO: remove this hardcoded coordinate
        if 5.5 < x < 13.73:
            if 17.53 > y > 11.56:
                esper.dispatch_event("regenerate_world", True)

    def process(self, delta_time):
        for ent_a, ([velocity, pos_a, _]) in self.world.get_components(Velocity, Position, Player):

            if not velocity.is_moving():
                continue

            for ent_b, ([goal]) in self.world.get_components(Goal):

                if ent_b == ent_a:
                    continue

                distance = pos_a.distance(goal.position)

                if distance == 1:
                    if self.menu is None:
                        scale = Scale(10.0, 10.0, 1)

                        congratulations = text.create_text(
                            self.world, 10, 15,
                            self.congratulations_texture,
                            scale
                        )

                        continue_playing = text.create_text(
                            self.world, 10, 5,
                            self.continue_texture,
                            scale
                        )

                        self.menu = [congratulations, continue_playing]
