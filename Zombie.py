import pygame
import math
from Constants import *
pygame.init()

class Zombie:

    EYE_SIZE = 0.2
    EYE_DIST_CENTER = 0.8
    EYE_OFFSET_DEG = 30

    def __init__(self, x, y, health, radius=20, facingDeg=180, speed=4.0):
        self.x = x
        self.y = y
        self.health = health
        self.radius = radius
        self.facing = facingDeg                 # In Degrees
        self.speed = speed
        self.sprintCdFrames = 0

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

    def updatePos(self, playerX, playerY):
        targetPosDelta = (playerX - self.x, playerY - self.y)
        self.facing = radiansToDegrees(math.atan2(-targetPosDelta[1], targetPosDelta[0]))

def degreesToRadians(deg):
    return deg / 180 * math.pi

def radiansToDegrees(rad):
    return rad * 180 / math.pi

def getRectCordsOnCircleRad(rad, r):
    cords = (r * math.cos(rad), r * math.sin(rad))
    return cords

def getRectCordsOnCircleDeg(deg, r):
    return getRectCordsOnCircleRad(degreesToRadians(deg), r)