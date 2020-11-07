import pygame

from Maps.Map1.Map1 import Map1
from Player import Player
from Constants import *

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption(WIN_NAME)
win = pygame.display.set_mode((WIDTH, HEIGHT))

players = [Player(0, 0)]
currMap = Map1()
mapFOV = FOV * max(WIDTH, HEIGHT)

def drawDisplay(window, events):
    window.fill((0, 0, 0))
    for player in players:
        player.updatePos(currMap.getRenderedWalls())
        x, y = player.getPos()
        currMap.draw(window, x, y, mapFOV)
        player.checkShooting(events)
        player.draw(window, currMap.getRenderedWalls())
    pygame.display.update()

running = True
while running:

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    drawDisplay(win, events)

    clock.tick(FPS)

pygame.quit()