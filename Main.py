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

def drawDisplay(window):
    window.fill((0, 0, 0))
    for player in players:
        player.updatePos()
        player.draw(window)
    pygame.display.update()

running = True
while running:

    drawDisplay(win)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(fps)

pygame.quit()