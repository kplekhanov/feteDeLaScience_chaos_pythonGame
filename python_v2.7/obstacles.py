import numpy as np
import pygame
import pygame.gfxdraw
 

DISSIPATION = 0.9
    
class Circle:
    def __init__(self, r=13, pos=(0.,0.), dissipation=DISSIPATION):
        self.r = r
        self.x, self.y = pos
        self.dissipation = dissipation
        
    def getDist2Pt(self, x, y):
        dx = self.x - x
        dy = self.y - y
        return np.hypot(dx, dy)
        
    def getPhi2Pt(self, x, y):
        dx = self.x - x
        dy = self.y - y
        return np.arctan2(dy, dx)
        
    def getDist2Obj(self, obj):
        dx = self.x - obj.x
        dy = self.y - obj.y
        return np.hypot(dx, dy)
        
    def getPhi2Obj(self, obj):
        dx = self.x - obj.x
        dy = self.y - obj.y
        return np.arctan2(dy, dx)
        
    def reflectMissile(self, missile, dt):
        if self.getDist2Pt(missile.x+missile.vx*dt, missile.y+missile.vy*dt) <= self.r + missile.r:
            a1 = np.arctan2(missile.vy, missile.vx)
            a2 = self.getPhi2Obj(missile)
            a3 = 2 * a2 - np.pi - a1
            missile.vabs *= self.dissipation
            missile.vx = missile.vabs * np.cos(a3)
            missile.vy = missile.vabs * np.sin(a3)
        
    def display(self, screen):
        #pygame.draw.circle(screen, (116, 208, 242), [int(self.x), int(self.y)], int(self.r), 0)
        #pygame.draw.circle(screen, (0, 38, 209), [int(self.x), int(self.y)], int(self.r), 3)
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), int(self.r), (116, 208, 242))
        pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), int(self.r-1), (0, 38, 209))
        pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), int(self.r), (0, 38, 209))

        
class Point(Circle):
    def __init__(self, pos=(0.,0.), dissipation=DISSIPATION):
        Circle.__init__(self, 0, pos, dissipation)
    
    def __add__(self, other):
        return Point((self.x + other.x, self.y + other.y), self.dissipation)
        
    def __sub__(self, other):
        return Point((self.x - other.x, self.y - other.y), self.dissipation)
        
    def __mul__(self, f):
        return Point((self.x * f, self.y * f), self.dissipation)


class Line:    
    def __init__(self, x, y, length, theta, dissipation=DISSIPATION):
        self.center = Point((x, y))
        self.length = length
        self.theta = theta
        self.A = Point((x - length * np.cos(theta) / 2, 
                        y - length * np.sin(theta) / 2))
        self.B = Point((x + length * np.cos(theta) / 2,
                        y + length * np.sin(theta) / 2))
        self.vec = self.B - self.A
        self.dissipation = dissipation
        
    def reflectMissile(self, missile, dt):
        vec1 = Point((missile.x, missile.y)) - self.A
        f = max(0., min(1., (vec1.x * self.vec.x + vec1.y * self.vec.y) / (self.length ** 2) ))
        closestPoint = self.A + self.vec * f
        closestPoint.dissipation = self.dissipation
        closestPoint.reflectMissile(missile, dt)
            
    def display(self, screen):
        pygame.draw.line(screen, (0, 38, 209), (self.A.x, self.A.y), (self.B.x, self.B.y), 2)
        

class Rectangle(object):
    def __init__(self, x, y, w, h, theta, dissipation=DISSIPATION):
        self.center = Point((x, y))
        self.width = w
        self.height = h
        self.theta = theta
        self.dissipation = dissipation
        self.lines = []
            
        self.lines.append(Line(x - h*np.sin(self.theta)/2,
                               y + h*np.cos(self.theta)/2, w, theta, dissipation))
        self.lines.append(Line(x + h*np.sin(self.theta)/2,
                               y - h*np.cos(self.theta)/2, w, theta, dissipation))
        self.lines.append(Line(x + w*np.cos(self.theta)/2,
                               y + w*np.sin(self.theta)/2, h, np.pi/2+theta, dissipation))
        self.lines.append(Line(x - w*np.cos(self.theta)/2,
                               y - w*np.sin(self.theta)/2, h, np.pi/2+theta, dissipation))
        
    def reflectMissile(self, missile, dt):
        for l in self.lines:
            l.reflectMissile(missile, dt)
        
    def display(self, screen):
        for l in self.lines:
            l.display(screen)