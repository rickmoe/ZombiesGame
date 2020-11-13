import pygame
from Constants import *
pygame.init()

class WallBuy:

    BACK_PANEL_COLOR = (212, 175, 55)

    def __init__(self, gun, points, orientation, gunCost, ammoCost, width=3):
        self.gunType = gun
        self.gunReference = gun()
        self.gunReference.LENGTH = 0.8
        self.points = points
        if orientation == '+x':
            self.points.extend([(val[0] - width, val[1]) for val in reversed(self.points)])
            self.theta = 270
            maxYIndex, minYIndex = (0, 1) if self.points[0][1] > self.points[1][1] else (1, 0)
            self.drawStartPoint = (0.9 * self.points[maxYIndex][0] + 0.1 * self.points[minYIndex][0], 0.9 * self.points[maxYIndex][1] + 0.1 * self.points[minYIndex][1])
            self.length = self.points[maxYIndex][1] - self.points[minYIndex][1]
        elif orientation == '-x':
            self.points.extend([(val[0] + width, val[1]) for val in reversed(self.points)])
            self.theta = 90
            maxYIndex, minYIndex = (0, 1) if self.points[0][1] > self.points[1][1] else (1, 0)
            self.drawStartPoint = (0.9 * self.points[minYIndex][0] + 0.1 * self.points[maxYIndex][0], 0.9 * self.points[minYIndex][1] + 0.1 * self.points[maxYIndex][1])
            self.length = self.points[maxYIndex][1] - self.points[minYIndex][1]
        elif orientation == '-y':
            self.points.extend([(val[0], val[1] + width) for val in reversed(self.points)])
            self.theta = 180
            maxXIndex, minXIndex = (0, 1) if self.points[0][0] > self.points[1][0] else (1, 0)
            self.drawStartPoint = (0.9 * self.points[maxXIndex][0] + 0.1 * self.points[minXIndex][0], 0.9 * self.points[maxXIndex][1] + 0.1 * self.points[minXIndex][1])
            self.length = self.points[maxXIndex][0] - self.points[minXIndex][0]
        else:
            self.points.extend([(val[0], val[1] - width) for val in reversed(self.points)])
            self.theta = 0
            maxXIndex, minXIndex = (0, 1) if self.points[0][0] > self.points[1][0] else (1, 0)
            self.drawStartPoint = (0.9 * self.points[minXIndex][0] + 0.1 * self.points[maxXIndex][0], 0.9 * self.points[minXIndex][1] + 0.1 * self.points[maxXIndex][1])
            self.length = self.points[maxXIndex][0] - self.points[minXIndex][0]
        self.gunCost = gunCost
        self.ammoCost = ammoCost

    def draw(self, win, x, y):
        deltaX, deltaY = WIDTH / 2 - x, HEIGHT / 2 - y
        pygame.draw.polygon(win, self.BACK_PANEL_COLOR, [(x + deltaX, y + deltaY) for x, y in self.points])
        deltaY -= self.length - 3 if self.theta == 0 else 0
        deltaX -= self.length - 3 if self.theta == 90 else 0
        deltaY += self.length - 3 if self.theta == 180 else 0
        deltaX += self.length - 3 if self.theta == 270 else 0
        self.gunReference.drawGunBody(win, self.drawStartPoint[0] + deltaX, self.drawStartPoint[1] + deltaY, self.length, self.theta)

    def getGunReference(self):
        return self.gunReference

    def getGunCost(self):
        return self.gunCost

    def getAmmoCost(self):
        return self.ammoCost
