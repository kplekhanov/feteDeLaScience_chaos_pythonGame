import numpy as np

from canon import Canon
from levels.base import BaseLevel
from obstacles import Circle
from target import TargetArea


class Level2(BaseLevel):
    MAX_TIME = 600

    def initialize(self, world):
        for i in range(-5,6):
            world.addObstacle(Circle(
                r=15, pos=[world.width/2 + i*world.width/13, 0.36*world.height]))
            world.addObstacle(Circle(
                r=15, pos=[world.width/2 + i*world.width/13, 0.2*world.height]))
        for i in range(-5,5):
            world.addObstacle(Circle(
                r=15, pos=[world.width/2+world.width/39 + i*world.width/13, 0.28*world.height]))
            world.addObstacle(Circle(
                r=15, pos=[world.width/2+world.width/39 + i*world.width/13, 0.44*world.height]))
        world.canon = Canon(r=75, pos=[world.width/2, world.height], theta=-np.pi/2)
        world.target = TargetArea(pos=(world.width / 2, world.height * 0.05), width=world.width * 0.05, height=world.height * 0.05)