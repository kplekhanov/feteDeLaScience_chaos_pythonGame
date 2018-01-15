import pygame

from obstacles import Circle


class HoleCircle(Circle):
    def catch(self, missile):
        return self.getDist2Obj(missile) <= self.r
    
    def display(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), [int(self.x), int(self.y)], self.r, 0)