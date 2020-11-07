import pygame
pygame.init()
from Constants import *

class Wall:

    COLOR = (64, 64, 64)

    def __init__(self, points, innerPointCount=0):
        if innerPointCount == 0:
            innerPointCount = int((len(points) / 2))
        self.points = points
        self.innerPoints = self.points[0:innerPointCount]

    def draw(self, win, x, y, fov):
        deltaX, deltaY = WIDTH / 2 - x, HEIGHT / 2 - y
        points = [(a + deltaX, b + deltaY) for a, b in self.points]
        pygame.draw.polygon(win, self.COLOR, points)