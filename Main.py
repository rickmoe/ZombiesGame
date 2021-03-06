import pygame
from DelayedAction import DelayedAction
from Maps.Map1.Map1 import Map1
from Player import Player
from ZombieManager import ZombieManager
from Constants import *

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()

pygame.display.set_caption(WIN_NAME)
pygame.mixer.music.set_volume(0.3)
win = pygame.display.set_mode((WIDTH, HEIGHT))

players = [Player(0, 0)]
zm = ZombieManager()
currMap = Map1()
mapFOV = FOV * max(WIDTH, HEIGHT)

def drawDisplay(window, events):
    window.fill((0, 0, 0))
    for player in players:
        player.updatePos(currMap.getRenderedWalls(), currMap.getRenderedWallBuys())
        x, y = player.getPos()
        player.checkDoorBuy(currMap)
        player.checkGunBuy()
        currMap.draw(window, x, y, mapFOV)
        player.checkShooting(events)
        player.draw(window, currMap.getRenderedWalls())
        zm.tick(window, x, y, player.gun, player.getShotVect())
        for instance in DelayedAction.getInstances():
            instance.tick()
    if currMap.getCurrRoom() is not None:
        currMap.getCurrRoom().drawRoomName(window)
    fpsFont = pygame.font.SysFont('arial', 32)
    fpsText = fpsFont.render('{:.0f}'.format(clock.get_fps()), False, (0, 64, 0))
    fpsTextRect = fpsText.get_rect()
    fpsTextRect.topright = (WIDTH, 0)
    win.blit(fpsText, fpsTextRect)
    roundFont = pygame.font.SysFont(FONT, 96)
    roundText = roundFont.render('{}'.format(zm.getRound()), False, (160, 0, 0))
    roundText2 = roundFont.render('{}'.format(zm.getRound()), False, (48, 0, 0))
    roundTextRect = roundText.get_rect()
    roundTextRect.bottomleft = (15, HEIGHT - 10)
    roundTextRect2 = roundText.get_rect()
    roundTextRect2.bottomleft = (roundTextRect.bottomleft[0] + 3, roundTextRect.bottomleft[1] + 3)
    win.blit(roundText2, roundTextRect2)
    win.blit(roundText, roundTextRect)
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