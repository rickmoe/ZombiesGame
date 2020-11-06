import pygame
from Player import Player
from Constants import *

pygame.init()

WIDTH = 800
HEIGHT = 800

clock = pygame.time.Clock()
fps = 60

pygame.display.set_caption(WIN_NAME)
win = pygame.display.set_mode((WIDTH, HEIGHT))

players = [Player(WIDTH / 2, HEIGHT / 2)]

def drawDisplay(window, events):
    window.fill((0, 0, 0))
    for player in players:
        player.updatePos()
        player.checkShooting(events)
        player.draw(window)
    pygame.display.update()

running = True
while running:

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    drawDisplay(win, events)

    clock.tick(fps)

pygame.quit()