import pygame
pygame.init()
import math
from Guns.M1911 import M1911

class Player:

    visorRadiusOffsetPercent = 1.025

    def __init__(self, x, y, radius=20, facingDeg=180, visorLengthDeg=90, speed=2):
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = facingDeg                 # In Degrees
        self.visorLength = visorLengthDeg       # In Degrees
        self.speed = speed
        self.gun = M1911()
        self.shooting = False

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 255), (self.x, self.y), self.radius)
        arcRect = (int(self.x - self.radius * self.visorRadiusOffsetPercent), int(self.y - self.radius * self.visorRadiusOffsetPercent),
                        int(self.radius * self.visorRadiusOffsetPercent * 2), int(self.radius * self.visorRadiusOffsetPercent * 2))
        pygame.draw.arc(win, (0, 255, 0), arcRect, degreesToRadians(self.facing) - degreesToRadians(self.visorLength) / 2,
                        degreesToRadians(self.facing) + degreesToRadians(self.visorLength) / 2, width=int(self.radius / 6))
        self.gun.draw(win, self.x, self.y, self.radius, self.facing)
        if self.shooting:
            self.gun.shoot(win, self.x, self.y, self.radius, self.facing)

    def updatePos(self):
        keys = pygame.key.get_pressed()
        vel = [0, 0]
        if keys[pygame.K_w]:
            vel[1] += 1
        if keys[pygame.K_a]:
            vel[0] -= 1
        if keys[pygame.K_s]:
            vel[1] -= 1
        if keys[pygame.K_d]:
            vel[0] += 1
        velDir = getCordsDirectionDeg(vel[0], vel[1])
        deltaX, deltaY = getRectCordsOnCircleDeg(velDir, 0 if vel[0] == 0 and vel[1] == 0 else self.speed)
        self.x += deltaX
        self.y -= deltaY        # y-axis is inverted on pygame
        mouseX, mouseY = pygame.mouse.get_pos()
        self.facing = radiansToDegrees(math.atan2(-(mouseY - self.y), mouseX - self.x))

    def checkShooting(self, events):
        self.shooting = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.shooting = True

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