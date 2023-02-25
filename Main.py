import pygame, random, numpy as np
from Species import Species
from Sun import Sun
from Food import Food
import math
from colors import *

pygame.init()

windowSize = 600
gameDisplay = pygame.display.set_mode((windowSize, windowSize))

gameExit = False

showStats = False
Foods = []
Sun1 = Sun()
Organisms = []
for x in range(50):
    Organisms.append(Species(random.randint(0, windowSize), random.randint(0, windowSize), x % 2, random.randint(0, 40)))
Clock = pygame.time.Clock()

def Distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


while not gameExit:
    gameDisplay.fill((0, 50+((Sun1.time/Sun1.inittime) - 1)/2, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print(Organisms[0].age)
            if event.key == pygame.K_s:
                if showStats == True:
                    showStats = False
                else:
                    showStats = True


    if random.randint(1, 2 + int(np.round(1.5 * len(Foods)))) == 1:
        Foods.append(Food())
    for z in range(len(Foods)):
        Foods[z].draw()

    for z in range(len(Organisms)):
        Organisms[z].draw()
        Organisms[z].update()
        Organisms[z].importance()
        if Organisms[z].target is None:
            if Organisms[z].mode == 0 and len(Foods) > 0:
                if Organisms[z].matetarget is None and Organisms[z].mate is None:
                    Organisms[z].move = (0, 0)
                    FoodDis = []
                    for k in range(len(Foods)):
                        FoodDis.append(Distance(Organisms[z].x, Organisms[z].y, Foods[k].x, Foods[k].y))
                        if Foods[k].targeted:
                            FoodDis[-1] = 10000
                    if np.min(FoodDis) != 10000:
                        index = int(np.argmin(FoodDis))
                        Foods[index].targeted = True
                        Organisms[z].noFood = False
                        Organisms[z].foodtarget = index
                        Organisms[z].target = (Foods[index].x, Foods[index].y)
                        dist_x = (Organisms[z].target[0] - Organisms[z].x)
                        dist_y = (Organisms[z].target[1] - Organisms[z].y)
                        velocity = (Organisms[z].speed * (dist_x / math.sqrt(dist_x ** 2 + dist_y ** 2)),
                                    Organisms[z].speed * (dist_y / math.sqrt(dist_x ** 2 + dist_y ** 2)))
                        Organisms[z].move = velocity
                    else:
                        Organisms[z].noFood = True

        # Marks Food Item:
        # if Organisms[z].target != None:
        #     pygame.draw.rect(gameDisplay, (255, 0, 0), [Organisms[z].target[0], Organisms[z].target[1], 4, 4])

    deadIndexes = []
    for k in range(len(Organisms)):
        if Organisms[k].dead:
            deadIndexes.append(k)
            if Organisms[k].mate is not None:
                Organisms[Organisms[k].mate].matetarget = None
                Organisms[Organisms[k].mate].move = (0, 0)
    for k in range(len(deadIndexes)):
        for z in range(len(Organisms)):
            if Organisms[z].mate is not None:
                if Organisms[z].mate > deadIndexes[-k - 1]:
                    Organisms[z].mate -= 1
        if Organisms[deadIndexes[-k - 1]].foodtarget is not None:
            Foods[Organisms[deadIndexes[-k - 1]].foodtarget].targeted = False
        del Organisms[deadIndexes[-k - 1]]




    Sun1.update()



    pygame.display.update()
    Clock.tick(60)
pygame.quit()
quit()