import numpy as np

from canon import Canon
from levels.base import BaseLevel
from obstacles import Rectangle
from target import TargetArea


class Level1(BaseLevel):
    MAX_TIME = 240

    def initialize(self, world):
        world.addObstacle(Rectangle(world.width * 0.625, world.height * 0.33,
                                    world.width * 0.75, 50,
                                    0))
        world.addObstacle(Rectangle(world.width * 0.375, world.height * 0.66,
                                    world.width * 0.75, 50,
                                    0))
        world.target = TargetArea(pos=(world.width * 0.85, world.height * 0.15),
                                   width=world.width * 0.2, height=world.height * 0.2)
        world.canon = Canon(r=75, pos=[world.width * 0.5, world.height], theta=-np.pi / 2)