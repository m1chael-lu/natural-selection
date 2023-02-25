import math, random, pygame
import numpy as np
import noise
from colors import *
from MatingCall import Particle

consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', "n", 'p', 'r', 'q', 'z', 'x']
vowel = ['a', 'e', 'i', 'o', 'u']


def randomSpecies():
    import random
    return consonants[random.randint(0, len(consonants) - 1)] + \
           vowel[random.randint(0, len(vowel) - 1)] + consonants[random.randint(0, len(consonants) - 1)]


def Distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


speciesName = randomSpecies()


class Species:
    def __init__(self, x, y, g, age=0):
        self.age = age
        self.size = 10
        if age != 0:
            self.size = ((20 * self.age) / 200) + 10
        self.weight = (30 - self.size) * math.log(random.randint(7, 12), 10)
        self.attractiveness = random.randint(50, 100)
        self.move = (0, 0)
        self.hunger = random.randint(500, 750)
        self.happiness = 0
        self.x = x
        self.y = y
        self.species = speciesName
        self.g = g
        self.mate = None
        self.calling = False
        self.mateTime = 60
        self.offspring = 0
        self.maleReprod = 0
        self.matetarget = None
        self.particles = []
        # genders
        # 0 - Male
        # 1 - Female
        if self.g == 1:
            self.color = (0, random.randint(100, 200), random.randint(150, 255))
        else:
            self.color = (0, random.randint(10, 80), random.randint(100, 200))

        self.xnoise1 = random.randint(0, 10000)
        self.xnoise2 = random.randint(0, 10000)
        self.ynoise1 = random.randint(0, 10000)
        self.ynoise2 = random.randint(0, 10000)
        self.increment = .001
        self.target = None
        self.speed = math.sqrt(self.weight) / 2
        self.foodtarget = None
        # 0-Hunger
        # 1-Leisure
        # 2-Exhaustion
        # 3-Reproduction
        self.mode = 1
        self.foodTimer = 30
        self.dead = False

        self.FoodV1 = random.randint(30, 50)
        self.FoodV2 = random.randint(0, 10)
        self.RepV1 = random.randint(-10, 10) / 10
        self.RepV2 = random.randint(-10, 10) / 10
        self.RepV3 = random.randint(-5, 5) / 10
        self.RepV4 = random.randint(-10, 10) / 10
        self.LeisureV = random.randint(20, 50)
        self.noFood = False
        self.particleTimer = 0

    def draw(self):
        from Main import gameDisplay, Organisms
        import pygame
        pygame.draw.ellipse(gameDisplay, self.color,
                            [self.x - self.size / 2, self.y - self.size / 2, self.size, self.size])
        # if self.mate is not None:
        #     pygame.draw.line(gameDisplay, black, (self.x, self.y), (Organisms[self.mate].x, Organisms[self.mate].y))

    def update(self):
        from Main import Foods, Organisms, windowSize
        if self.mode == 1 and self.matetarget is None:
            self.xnoise1 += self.increment
            self.ynoise1 += self.increment
            self.xnoise2 += self.increment
            self.ynoise2 += self.increment
            xChange = noise.snoise2(self.xnoise1, self.xnoise2, 2) * self.speed * 2
            yChange = noise.snoise2(self.ynoise1, self.ynoise2, 2) * self.speed * 2
            self.move = (xChange, yChange)

        if self.hunger <= 0:
            self.dead = True
            print('death by hunger at the age of ' + str(self.age))
        self.age += .05
        self.hunger -= .25
        self.size = ((20 * self.age) / 200) + 10
        self.weight = (30 - self.size) * math.log(random.randint(7, 12), 10)
        if self.weight < 0:
            self.weight = 0.01
        self.speed = math.sqrt(self.weight) / 2
        if self.move != (0, 0):
            self.hunger -= np.log(np.sqrt(np.square(self.move[0]) + np.square(self.move[1])))

        # Random Deaths

        if self.age == float(int(self.age)):
            if self.age < 150 + self.happiness:
                if random.randint(self.age, 150 + self.happiness) == self.age:
                    self.dead = True
                    print('death by age at the age of ' + str(self.age))
            else:
                self.dead = True
                print('death by age at the age of ' + str(self.age))

        # Movement

        self.x += self.move[0]
        self.y += self.move[1]

        if self.x < 0:
            self.x = 0
        elif self.x > windowSize:
            self.x = windowSize
        if self.y < 0:
            self.y = 0
        elif self.y > windowSize:
            self.y = windowSize

        # Eating
        if self.target is not None:
            if Distance(self.x, self.y, self.target[0], self.target[1]) <= 5:
                self.move = (0, 0)
            if self.move == (0, 0):
                self.foodTimer -= 1
                if Distance(self.x, self.y, self.target[0], self.target[1]) > 5:
                    if self.target[0] - self.x != 0:
                        self.x += ((self.target[0] - self.x) / (math.fabs(self.target[0] - self.x))) * random.randint(1,
                                                                                                                      2)
                    else:
                        self.x += random.randint(-1, 1)
                    if self.target[1] - self.y != 0:
                        self.y += ((self.target[1] - self.y) / (math.fabs(self.target[1] - self.y))) * random.randint(1,
                                                                                                                      2)
                    else:
                        self.y += random.randint(-1, 1)
                else:
                    self.x += random.randint(-2, 2)
                    self.y += random.randint(-2, 2)
                if self.foodTimer == 0:
                    for k in range(len(Organisms)):
                        if Organisms[k].foodtarget == self.foodtarget:
                            Organisms[k].target = None
                            Organisms[k].move = (0, 0)
                        if Organisms[k].foodtarget != None and Organisms[k].foodtarget > self.foodtarget:
                            Organisms[k].foodtarget -= 1
                    self.foodTimer = 30
                    self.target = None
                    self.hunger += Foods[self.foodtarget].size * 20
                    del Foods[self.foodtarget]
                    self.foodtarget = None
                    if self.hunger >= 750:
                        self.size += (self.hunger - 500) / 50

        # Mating
        if self.mode == 3:
            if self.mate is None and self.foodtarget is None:
                self.move = (0, 0)
                self.calling = True
                Matchfinder = []
                for k in range(len(Organisms)):
                    if Organisms[k].g == 0:
                        if Organisms[k].foodtarget is None:
                            if Organisms[k].matetarget is None:
                                ageDiff = 30 - math.fabs(Organisms[k].age - self.age)
                                Dist = Distance(self.x, self.y, Organisms[k].x, Organisms[k].y)
                                DistFact = (424 - Dist) / 5
                                if ageDiff < 0:
                                    ageDiff = 0
                                if ageDiff * 3 + Organisms[k].maleReprod * 2 + self.attractiveness + DistFact >= 240:
                                    Matchfinder.append(
                                        ageDiff * 3 + Organisms[k].maleReprod * 2 + self.attractiveness + DistFact)
                                else:
                                    Matchfinder.append(0)
                            else:
                                Matchfinder.append(0)
                        else:
                            Matchfinder.append(0)
                    else:
                        Matchfinder.append(0)
                if np.max(Matchfinder) != 0:
                    self.mate = np.argmax(Matchfinder)
                    Organisms[self.mate].matetarget = (self.x, self.y)
                    dist_x = (Organisms[self.mate].matetarget[0] - Organisms[self.mate].x)
                    dist_y = (Organisms[self.mate].matetarget[1] - Organisms[self.mate].y)
                    if dist_x == 0 and dist_y == 0:
                        velocity = 1
                    else:
                        velocity = (Organisms[self.mate].speed * (dist_x / math.sqrt(dist_x ** 2 + dist_y ** 2)),
                                    Organisms[self.mate].speed * (dist_y / math.sqrt(dist_x ** 2 + dist_y ** 2)))
                    Organisms[self.mate].move = velocity
            if self.mate is not None:
                if Distance(self.x, self.y, Organisms[self.mate].x, Organisms[self.mate].y) <= 5:
                    Organisms[self.mate].move = (0, 0)
                    self.mateTime -= 1
                    if self.mateTime == 0:
                        self.mateTime = 60
                        self.offspring += 1
                        Organisms[self.mate].offspring += 1
                        Organisms[self.mate].matetarget = None
                        self.mate = None
                        Organisms.append(Species(self.x, self.y, random.randint(0, 1)))

            # Particle Creation
            self.particleTimer += 1
            if self.particleTimer % 45 == 0:
                self.particles.append(Particle(self.x - self.size / 2, self.y - self.size / 2))
            for k in range(len(self.particles)):
                self.particles[k].update()
                self.particles[k].draw(self.x, self.y)

            deadIndexes = []
            for k in range(len(self.particles)):
                if self.particles[k].dead:
                    deadIndexes.append(k)
            for k in range(len(deadIndexes)):
                del self.particles[deadIndexes[-k - 1]]

    def importance(self):
        from Main import showStats, gameDisplay
        old = self.mode
        FoodImportance = (-1 * ((self.hunger / self.FoodV1) ** 2)) + 100 - self.FoodV2
        if FoodImportance < 0:
            FoodImportance /= 5
        LeisureImportance = self.LeisureV - self.age / 3
        RestImportance = -100
        ReproductionImportance = -100
        TwoGraphs = []
        TwoGraphs.append((-math.sqrt((85 + self.RepV1) * self.age) + 70 + self.RepV2) * 2)
        TwoGraphs.append(((self.age / (5 + self.RepV3)) ** 2 - 15 + self.RepV4) * 2)
        if self.g == 1:
            ReproductionImportance = np.min(TwoGraphs) - self.offspring * 10
        else:
            self.maleReprod = np.min(TwoGraphs) - self.offspring * 10

        self.mode = np.argmax([FoodImportance, LeisureImportance, RestImportance, ReproductionImportance])
        if showStats == True:
            Copy = [FoodImportance, LeisureImportance, RestImportance, ReproductionImportance]
            if self.g == 0:
                Copy[3] = self.maleReprod
            mini = np.min(Copy)
            for k in range(len(Copy)):
                Copy[k] = Copy[k] + np.abs(mini)
            Flength = (Copy[0] / np.sum(Copy)) * 30
            LLength = (Copy[1] / np.sum(Copy)) * 30
            Elength = (Copy[2] / np.sum(Copy)) * 30
            RLength = (Copy[3] / np.sum(Copy)) * 30
            pygame.draw.rect(gameDisplay, (35, 130, 19), [self.x - 15, self.y - 25, Flength, 3])
            pygame.draw.rect(gameDisplay, (230, 230, 0), [self.x - 15 + Flength, self.y - 25, LLength, 3])
            pygame.draw.rect(gameDisplay, (12, 12, 255), [self.x - 15 + Flength + LLength, self.y - 25, Elength, 3])
            pygame.draw.rect(gameDisplay, (255, 12, 12),
                             [self.x - 15 + Flength + LLength + Elength, self.y - 25, RLength, 3])

        if old == 3 and self.mode == 1 and self.mate is not None:
            self.mode = old
        if old == 3 and self.mode == 0 and self.mate is not None:
            self.mode = old
        if old != 3 and self.g == 0 and self.mode == 3:
            self.mode = old
        if self.noFood:
            if self.mode == 0:
                self.mode = np.argmax([LeisureImportance, RestImportance, ReproductionImportance]) + 1
