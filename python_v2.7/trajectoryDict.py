import pygame


class TrajectoryDict(dict):
    def appendTrajectory(self, missiles):
        for m in missiles:
            if m in self.keys():
                self[m].append((int(m.x), int(m.y)))
                if len(self[m]) > 1000:
                    self[m] = self[m][1:]
            else:
                self[m] = [(int(m.x), int(m.y))]
        
    def display(self, screen):
        for trajectory in self.values():
            if len(trajectory) != 1:
                pygame.draw.lines(screen, (0, 109, 193), False, trajectory, 1)