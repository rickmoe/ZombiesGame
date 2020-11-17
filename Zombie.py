import pygame
import math
from DelayedAction import DelayedAction
from Constants import *

pygame.init()

class Zombie:

    EYE_SIZE = 0.2
    EYE_DIST_CENTER = 0.8
    EYE_OFFSET_DEG = 30

    def __init__(self, x, y, health, speed, radius=20, facingDeg=180):
        self.x = x
        self.y = y
        self.health = health
        self.radius = radius
        self.facing = facingDeg                 # In Degrees
        self.speed = speed
        self.shot = False

    def draw(self, win, playerX, playerY):
        deltaX, deltaY = WIDTH / 2 - playerX, HEIGHT / 2 - playerY
        pygame.draw.circle(win, (64, 128, 32), (self.x + deltaX, self.y + deltaY), self.radius)
        pygame.draw.arc(win, (32, 64, 16), (self.x + deltaX - self.radius, self.y + deltaY - self.radius, self.radius * 2, self.radius * 2), degreesToRadians(self.facing + 60), degreesToRadians(self.facing - 60), width=self.radius)
        eyeX_L, eyeY_L = getRectCordsOnCircleDeg(self.facing - self.EYE_OFFSET_DEG, self.radius * self.EYE_DIST_CENTER)
        eyeX_R, eyeY_R = getRectCordsOnCircleDeg(self.facing + self.EYE_OFFSET_DEG, self.radius * self.EYE_DIST_CENTER)
        eyeY_L *= -1
        eyeY_R *= -1
        pygame.draw.circle(win, (160, 32, 32), (self.x + deltaX + eyeX_L, self.y + deltaY + eyeY_L), self.radius * self.EYE_SIZE)
        pygame.draw.circle(win, (160, 32, 32), (self.x + deltaX + eyeX_R, self.y + deltaY + eyeY_R), self.radius * self.EYE_SIZE)
        if self.shot:
            self.drawBloodSpurt(win, playerX, playerY, self.x, self.y)
            self.drawDamageText(win, playerX, playerY, self.dmg)

    def updatePos(self, playerX, playerY):
        targetPosDelta = (playerX - self.x, playerY - self.y)
        self.facing = getCordsDirectionDeg(targetPosDelta[0], -targetPosDelta[1])
        dir = getCordsDirectionDeg(*targetPosDelta)
        deltaX, deltaY = getRectCordsOnCircleDeg(dir, self.speed)
        self.x += deltaX
        self.y += deltaY

    def checkShot(self, shotVect, gun):
        self.shot = self.doesShotIntersect(shotVect)
        if self.shot:
            self.dmg = gun.getDamage()
            self.health -= self.dmg

    def doesShotIntersect(self, shotVect):
        if shotVect is not None:
            d = (shotVect[2] - shotVect[0], shotVect[3] - shotVect[1])
            f = (shotVect[0] - self.x, shotVect[1] - self.y)
            a = d[0] * d[0] + d[1] * d[1]
            b = 2 * (d[0] * f[0] + d[1] * f[1])
            c = f[0] * f[0] + f[1] * f[1] - self.radius * self.radius
            discriminant = b * b - 4 * a * c
            if discriminant >= 0:
                discriminant = math.sqrt(discriminant)
                t1, t2 = (-b - discriminant) / (2 * a), (-b + discriminant) / (2 * a)
                if 0 <= t1 <= 1:
                    return shotVect[0] * t1 + shotVect[2] * (1 - t1), shotVect[1] * t1 + shotVect[3] * (1 - t1)
                if 0 <= t2 <= 1:
                    return shotVect[0] * t2 + shotVect[2] * (1 - t2), shotVect[1] * t2 + shotVect[3] * (1 - t2)
        return False

    def drawBloodSpurt(self, win, playerX, playerY, x, y):
        x += WIDTH / 2 - playerX
        y += HEIGHT / 2 - playerY
        vals = [[1, 3, 2], [1, 6, 3], [3, 8, 6], [5, 9, 5], [8, 10, 2]]
        colors = [(96, 0, 0)]
        MULT_1D = 0.6
        for i, val in enumerate(vals):
            for color in colors:
                DelayedAction([
                               [i, pygame.draw.line, [win, color, (x - val[0], y - val[0]), (x - val[1], y - val[1]), val[2]]],
                               [i, pygame.draw.line, [win, color, (x - val[0], y + val[0]), (x - val[1], y + val[1]), val[2]]],
                               [i, pygame.draw.line, [win, color, (x + val[0], y - val[0]), (x + val[1], y - val[1]), val[2]]],
                               [i, pygame.draw.line, [win, color, (x + val[0], y + val[0]), (x + val[1], y + val[1]), val[2]]],
                               [i, pygame.draw.line, [win, color, (x, y - val[0] * MULT_1D), (x, y - val[1] * MULT_1D), val[2] - 2]],
                               [i, pygame.draw.line, [win, color, (x - val[0] * MULT_1D, y), (x - val[1] * MULT_1D, y), val[2] - 2]],
                               [i, pygame.draw.line, [win, color, (x, y + val[0] * MULT_1D), (x, y + val[1] * MULT_1D), val[2] - 2]],
                               [i, pygame.draw.line, [win, color, (x + val[0] * MULT_1D, y), (x + val[1] * MULT_1D, y), val[2] - 2]],
                ])

    def drawDamageText(self, win, playerX, playerY, damage):
        dmgFont = pygame.font.SysFont('arial', self.radius)
        dmgText = dmgFont.render('{:.0f}'.format(damage), False, (255, 32, 32))
        dmgText2 = dmgFont.render('{:.0f}'.format(damage), False, (32, 32, 32))
        dmgTextRect = dmgText.get_rect()
        dmgTextRect.bottomleft = (self.x + self.radius * 0.8 + WIDTH / 2 - playerX, self.y + HEIGHT / 2 - playerY)
        dmgTextRect2 = dmgText2.get_rect()
        dmgTextRect2.bottomleft = (dmgTextRect.bottomleft[0] + 1, dmgTextRect.bottomleft[1] + 2)
        for i in range(20):
            DelayedAction([[i, win.blit, [dmgText, dmgTextRect.move(0, -i)]],
                           [i, win.blit, [dmgText2, dmgTextRect2.move(0, -i)]],
                           ])

    def checkAlive(self):
        return self.health > 0


def degreesToRadians(deg):
    return deg / 180 * math.pi

def radiansToDegrees(rad):
    return rad * 180 / math.pi

def getRectCordsOnCircleRad(rad, r):
    cords = (r * math.cos(rad), r * math.sin(rad))
    return cords

def getRectCordsOnCircleDeg(deg, r):
    return getRectCordsOnCircleRad(degreesToRadians(deg), r)

def getCordsDirectionRad(x, y):
    return math.atan2(y, x)

def getCordsDirectionDeg(x, y):
    return radiansToDegrees(getCordsDirectionRad(x, y))
