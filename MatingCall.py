import pygame, numpy as np

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.time = 0
        self.dead = False

    def draw(self, x, y):
        from Main import gameDisplay, Sun1
        width = (5 - ((self.time/90.0) * 4)) + 1
        color = (30, 50 + ((Sun1.time / Sun1.inittime) - 1) / 2, 0)
        pygame.draw.ellipse(gameDisplay, color, [self.x, self.y, (x - self.x) * 2, (y - self.y) * 2],
                            int(np.round(width)))

    def update(self):
        self.time += 1
        self.x -= self.time/15
        self.y -= self.time/15
        if self.time == 90:
            self.dead = True
