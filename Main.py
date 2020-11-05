import pygame

pygame.init()

WIDTH = 800
HEIGHT = 800

clock = pygame.time.Clock()
fps = 60

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombies")

def drawDisplay(window):
    window.fill((0, 0, 0))
    pygame.display.update()

running = True
while running:

    drawDisplay(win)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(fps)

pygame.quit()