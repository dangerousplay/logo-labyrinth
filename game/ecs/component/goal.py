from dataclasses import dataclass as component
from game.ecs.component.motion import Position


@component
class Goal:
    position: Position

    def __init__(self, position: Position):
        self.position = position
