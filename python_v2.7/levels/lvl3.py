import numpy as np

from canon import Canon
from levels.base import BaseLevel
from obstacles import Circle
from target import TargetArea


class Level3(BaseLevel):
    MAX_TIME = 600

    def initialize(self, world):
        world.addObstacle(Circle(r=150, pos=[world.width/2, world.height/2]))
        world.addObstacle(Circle(r=world.height,
                                 pos=[-world.height*np.sqrt(3)/2, world.height/2]))
        world.addObstacle(Circle(r=world.height,
                                 pos=[world.width+world.height*np.sqrt(3)/2, world.height/2]))
        world.canon = Canon(r=75, pos=[world.width/2, world.height], theta=-np.pi/2)
        world.target = TargetArea(pos=(world.width / 2, world.height * 0.21),
                                  width=world.height * 0.04, height=world.height * 0.04)
