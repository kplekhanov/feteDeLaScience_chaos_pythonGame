import numpy as np

from canon import Canon
from levels.base import BaseLevel


class Level7(BaseLevel):
    MAX_TIME = -1

    def initialize(self, world):
        world.canon = Canon(r=75, pos=[world.width/2, world.height], theta=-np.pi/2)
        world.canon.shotQuantity = 6
        world.showTrajectories = True