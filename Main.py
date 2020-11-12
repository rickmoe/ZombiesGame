import pygame
from DelayedAction import DelayedAction
from Maps.Map1.Map1 import Map1
from Player import Player
from Constants import *
pygame.init()
pygame.font.init()

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
        player.checkDoorBuy(currMap)
        currMap.draw(window, x, y, mapFOV)
        player.checkShooting(events)
        player.draw(window, currMap.getRenderedWalls())
        for instance in DelayedAction.getInstances():
            instance.tick()
    fpsFont = pygame.font.SysFont('arial', 32)
    fpsText = fpsFont.render('{:.0f}'.format(clock.get_fps()), False, (0, 64, 0))
    fpsTextRect = fpsText.get_rect()
    fpsTextRect.topright = (WIDTH, 0)
    win.blit(fpsText, fpsTextRect)
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