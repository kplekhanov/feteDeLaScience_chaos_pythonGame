import pygame


class Message(object):
    def __init__(self, pos, text="", size=30, color=(10,10,10)):
        self.pos = pos
        self.text = text
        font = pygame.font.SysFont('impact', size)
        self.surface = font.render(text, 1, color)
        self.rect = self.surface.get_rect()
        self.rect.center = pos
        
    def update(self, text, size=30, color=(10,10,10)):
        self.text = text
        font = pygame.font.SysFont('impact', size)
        self.surface = font.render(text, 1, color)
        self.rect = self.surface.get_rect()
        self.rect.center = self.pos
        
    def display(self, screen):
        screen.blit(self.surface, self.rect)
        

class Button:
    message = Message
    surface = pygame.Surface
    rect = pygame.Rect
    state = 0
    
    def __init__(self, pos, width, height, text=""):
        self.surface = pygame.Surface((width, height))
        self.surface.fill((225, 225, 225))
        
        self.rect = self.surface.get_rect()
        self.rect.center = pos
        
        self.message = Message((width/2, height/2), text)
        self.message.display(self.surface)
        
    def checkSelected(self, pos):
        if self.state == 0 and self.rect.collidepoint(pos):
            self.surface.fill((155, 155, 155))
            self.message.display(self.surface)
            self.state = 1
        if self.state == 1 and not self.rect.collidepoint(pos):
            self.surface.fill((225, 225, 225))
            self.message.display(self.surface)
            self.state = 0
        
    def checkActivated(self, pos):
        return self.rect.collidepoint(pos)
        
    def display(self, screen):
        screen.blit(self.surface, self.rect)
    