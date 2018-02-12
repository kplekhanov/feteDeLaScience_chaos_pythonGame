import numpy as np

from canon import Canon
from levels.base import BaseLevel
from obstacles import Circle


class Level6(BaseLevel):
    MAX_TIME = 99.9 * 60

    def initialize(self, world):
        world.addObstacle(Circle(world.height*0.25, (world.width * 0.5, world.height * 0.5), 1.0))
        world.canon = Canon(r=75, pos=[world.width/2, world.height], theta=-np.pi/2)
        world.canon.shotQuantity = 6
        world.showTrajectories = True
