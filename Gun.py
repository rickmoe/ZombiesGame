import pygame
import math
from Constants import *
pygame.init()

class Gun:

    LENGTH = 2.0                    # Multiplied by radius
    DRAW_DIST_FROM_CENTER = 0.9     # Percentage of the body before the gun is drawn

    def draw(self, win, x, y, r, theta):
        pass

    @staticmethod
    def getName():
        return "Gun"

    @staticmethod
    def getDrawStartPos(x, y, r, theta):
        circX, circY = getRectCordsOnCircleDeg(theta - 90, r)
        pos = (x + circX, y + circY)
        return pos

    @staticmethod
    def getDrawEndPos(x, y, r, theta, length):
        x, y = Gun.getDrawStartPos(x, y, r, theta)
        deltaX = length * math.cos(degreesToRadians(theta))
        deltaY = length * math.sin(degreesToRadians(theta))
        x += deltaX
        y -= deltaY
        return x, y

    def shoot(self, win, x, y, r, theta):
        Xi, Yi = self.getDrawEndPos(x, y, r, theta, self.LENGTH)
        Xv, Yv = math.cos(degreesToRadians(theta)), -math.sin(degreesToRadians(theta))
        pygame.draw.line(win, (255, 255, 255), (Xi, Yi), (Xi + Xv * 1.5 * max(WIDTH, HEIGHT), Yi + Yv * 1.5 * max(WIDTH, HEIGHT)), width=3)

def degreesToRadians(deg):
    return deg / 180 * math.pi

def radiansToDegrees(rad):
    return rad * 180 / math.pi

def getRectCordsOnCircleRad(rad, r):
    x, y = (r * math.cos(rad), r * math.sin(rad))
    return x, -y

def getRectCordsOnCircleDeg(deg, r):
    return getRectCordsOnCircleRad(degreesToRadians(deg), r)
