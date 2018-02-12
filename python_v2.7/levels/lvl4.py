import numpy as np

from canon import Canon
from levels.base import BaseLevel
from obstacles import Circle, Rectangle, Line
from target import TargetArea


class Level4(BaseLevel):
    MAX_TIME = 540

    def initialize(self, world):
        r = world.height * 5 / 12
        world.addObstacle(Circle(r=r,
                                 pos=[world.width + r * 0.3, world.height / 2]))
        world.addObstacle(Line(world.width * 0.6, world.height / 4,
                               world.width * 0.3, 0))
        world.addObstacle(Rectangle(world.width * 0.2, world.height * 0.42,
                                    world.width * 0.45, 30,
                                    0))
        world.addObstacle(Rectangle(world.width * 0.2, world.height * 0.58,
                                    world.width * 0.5, 35,
                                    0))
        world.addObstacle(Circle(
            r=20, pos=[world.width * 0.43, world.height * 0.42]))
        world.addObstacle(Circle(
            r=55, pos=[world.width * 0.46, world.height * 0.58]))
        world.canon = Canon(r=75, pos=[world.width/2, world.height], theta=-np.pi/2)
        world.target = TargetArea(pos=(world.width * 0.35, world.height * 0.5),
                                  width=world.height * 0.1, height=world.height * 0.1)