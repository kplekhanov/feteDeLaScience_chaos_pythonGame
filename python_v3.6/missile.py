import numpy as np
import pygame

from obstacles import Circle


R_MISSILE = 13

class Missile(Circle):
    def __init__(self, r=R_MISSILE, pos=(0.,0.), vel=(0.,0.)):
        self.r = r
        self.x, self.y = pos
        self.vx, self.vy = vel
        self.vabs = np.sqrt(self.vx**2 + self.vy**2)
        self.surface = pygame.image.load(('fig/BilliardBall.png'))
        
    def display(self, screen):
        screen.blit(self.surface, (int(self.x-R_MISSILE), int(self.y-R_MISSILE)))
        #pygame.draw.circle(screen, (0, 0, 255), [int(self.x), int(self.y)], self.r, 1)