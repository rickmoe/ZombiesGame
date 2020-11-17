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
zombies = [[-200, -100, 150, 1.0], [-200, 100, 150, 1.0], [200, -100, 150, 1.0], [200, 100, 150, 1.0]]
# (zm.spawn(x, y, h) for x, y, h in zombies)
for i in range(len(zombies)):
    zm.spawn(*zombies[i])
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