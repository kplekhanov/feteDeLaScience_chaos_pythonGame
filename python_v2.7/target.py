import pygame


class TargetArea(object):
    def __init__(self, pos=(0,0), width=0, height=0):
        self.width = int(width)
        self.height = int(height)
        self.x, self.y = pos
        self.getSurface()
        
    def getSurface(self):
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.rect.center = self.x, self.y
        self.surface.fill((247, 167, 111))
        for r in range(3, max(self.width, self.height), 6):
            #pygame.draw.circle(self.surface, (209, 108, 50), [int(self.x),int(self.y)], r, 3)
            pygame.gfxdraw.aacircle(self.surface, int(self.width/2), int(self.height/2), int(r-1), (209, 108, 50))
            pygame.gfxdraw.aacircle(self.surface, int(self.width/2), int(self.height/2), int(r), (209, 108, 50))
        pygame.draw.rect(self.surface, (209, 108, 50), (0, 0, self.width, self.height), 3)
    
    def catch(self, missile):
        pos = (missile.x, missile.y)
        if self.rect.collidepoint(pos):
            return True
        else:
            return False
    
    def display(self, screen):
        screen.blit(self.surface, self.rect)