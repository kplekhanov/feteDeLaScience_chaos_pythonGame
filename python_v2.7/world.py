import numpy as np

from canon import Canon
from target import TargetArea
from trajectoryDict import TrajectoryDict


class World(object):
    def __init__(self, width=400, height=400):
        self.width, self.height = width, height
        self.target = TargetArea()
        self.canon = Canon()
        self.missiles = []
        self.obstacles = []
        self.holes = []
        self.trajectoryDict = TrajectoryDict()
        self.showTrajectories = False
        self.interaction = False
        self.nt = 1
        self.dt = 1.

    def addMissile(self):
        self.missiles += self.canon.getMissile()
        self.adjust()

    def addObstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def addHole(self, hole):
        self.holes.append(hole)

    def adjust(self):
        if len(self.missiles) == 0:
            return
        vmax = np.max([m.vabs for m in self.missiles])
        self.nt = 1 * int(np.ceil(vmax))
        self.dt = 1. / self.nt

    def move(self, winCallback, loseCallback):
        self.adjust()
        self.trajectoryDict.appendTrajectory(self.missiles)
            
        for it in range(self.nt):
            for m in self.missiles:
                if (m.x + m.vx * self.dt >= self.width - m.r or
                    m.x + m.vx * self.dt <= m.r):
                    m.vx = -m.vx
                elif (m.y + m.vy * self.dt <= m.r or
                      m.y + m.vy * self.dt >= self.height - m.r):
                    m.vy = -m.vy
                                       
                for o in self.obstacles:
                    o.reflectMissile(m, self.dt)
                    
                for h in self.holes:
                    if h.catch(m):
                        loseCallback()
                        
                if self.target.catch(m):
                    winCallback()
                        
                if self.interaction:
                    for n in self.missiles:
                        if not n is m: 
                            n.reflectMissile(m, self.dt)
                
                m.x, m.y = m.x + m.vx * self.dt, m.y + m.vy * self.dt
                
    def display(self, screen):
        if self.showTrajectories == True:
            self.trajectoryDict.display(screen)
        self.target.display(screen)
        for h in self.holes:
            h.display(screen)
        for o in self.obstacles:
            o.display(screen)
        for m in self.missiles:
            m.display(screen)
        self.canon.display(screen)