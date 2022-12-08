from dataclasses import dataclass as component

import pyrr


@component
class Goal:
    position: pyrr.Vector3

