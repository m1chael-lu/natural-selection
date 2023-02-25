from colors import *
import random
import pygame

class Food:
    def __init__(self):
        from Main import windowSize
        self.size = random.randint(5, 7)
        self.color = yellow
        self.x = random.randint(0, windowSize)
        self.y = random.randint(0, windowSize)
        self.dead = False
        self.targeted = False

    def draw(self):
        from Main import gameDisplay
        pygame.draw.rect(gameDisplay, self.color, [self.x - self.size/2, self.y - self.size/2, self.size, self.size])
        if self.targeted == True:
            pygame.draw.rect(gameDisplay, red, [self.x, self.y, 4, 4])