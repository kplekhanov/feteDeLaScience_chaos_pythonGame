import numpy as np
import pygame

from missile import Missile


def rot_center(image, angle):
    """rotate an image while keeping its center"""
    rect = image.get_rect()
    rot_image = pygame.transform.rotozoom(image, angle, 1.)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect

class Canon(object):
    def __init__(self, r=75, pos=(0.,0.), theta=0):
        self.r = r
        self.x, self.y = pos
        self.x1 = pos[0] + r * np.cos(theta)
        self.y1 = pos[1] + r * np.sin(theta)
        self.theta = theta
        self.state = 0
        self.v = 0
        self.vmin = 3
        self.vmax = 20
        self.scaling = 15.
        self.shotQuantity = 1 # how many missiles per shot
        self.ofsety = 8
        
        self.getSurface()
        
    def getSurface(self):
        self.surface0 = pygame.image.load(('fig/Canon.png'))
        w = self.surface0.get_width() * 0.75
        self.surface0 = pygame.transform.rotozoom(self.surface0, 90, self.r * 1. / w)
        self.surface = self.surface0
        self.rect = self.surface0.get_rect()
        self.rect.center = (self.x + self.r * np.cos(self.theta) / 2,
                            self.y+self.ofsety + self.r * np.sin(self.theta) / 2)
                
    def setDirection(self, pos):
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        self.thetaOld = self.theta
        self.theta = np.arctan2(dy, dx)
        self.x1 = self.x + self.r * np.cos(self.theta)
        self.y1 = self.y + self.r * np.sin(self.theta)
        self.surface, self.rect = rot_center(self.surface0, -self.theta * 180 / np.pi - 90)
        self.rect.center = (self.x + self.r * np.cos(self.theta) / 2,
                            self.y+self.ofsety + self.r * np.sin(self.theta) / 2)
        
    def setSpeed(self, pos):
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        self.v  = self.r * np.cos(self.theta) * dx
        self.v += self.r * np.sin(self.theta) * dy
        self.v /= self.r * self.scaling
        if self.v < 0:
            self.v = self.vmin
        elif self.v > self.vmax:
            self.v = self.vmax
        
    def getMissile(self):
        indices = [0]
        for i in range(1, self.shotQuantity):
            indices += [-i,i]
        missiles = []
        for i in indices:
            newTheta = self.theta + i * np.pi / 1000
            vx = self.v * np.cos(newTheta)
            vy = self.v * np.sin(newTheta)
            x = self.x + self.r * np.cos(newTheta)
            y = self.y + self.r * np.sin(newTheta)
            missiles.append(Missile(pos=[x, y], vel=[vx, vy]))
        return missiles
        
    def display(self, screen):
        if self.state == 0:
            screen.blit(self.surface, self.rect)
        if self.state == 1:
            begPos = [int(self.x1), int(self.y1+6)]
            endPos = [int(self.x + self.r * np.cos(self.theta) * (1 + self.v / self.vmax)),
                       int(self.y+self.ofsety + self.r * np.sin(self.theta) * (1 + self.v / self.vmax))]
            pygame.draw.line(screen, (255, 0, 0), begPos, endPos, 5)
            screen.blit(self.surface, self.rect)
        if self.state == 2:
            screen.blit(self.surface, self.rect)
            