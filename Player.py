import pygame
pygame.init()
import math
from Constants import *
from Guns.M1911 import M1911

class Player:

    visorRadiusOffsetPercent = 1.025
    BASE_SPEED = 4.0
    SPRINT_SPEED = 6.0
    MAX_SPRINT_FRAMES = 90
    SPRINT_CD_FRAMES = 45
    SPRINT_RUNOUT_CD_FRAMES = 90

    def __init__(self, x, y, radius=20, facingDeg=180, visorLengthDeg=90, speed=3):
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = facingDeg                 # In Degrees
        self.visorLength = visorLengthDeg       # In Degrees
        self.speed = speed
        self.gun = M1911()
        self.sprintFrames = Player.MAX_SPRINT_FRAMES
        self.sprintCdFrames = 0
        self.shooting = False

    def draw(self, win, walls):
        pygame.draw.circle(win, (0, 0, 255), (WIDTH / 2, HEIGHT / 2), self.radius)
        arcRect = (int(WIDTH / 2 - self.radius * self.visorRadiusOffsetPercent), int(HEIGHT / 2 - self.radius * self.visorRadiusOffsetPercent),
                        int(self.radius * self.visorRadiusOffsetPercent * 2), int(self.radius * self.visorRadiusOffsetPercent * 2))
        pygame.draw.arc(win, (0, 255, 0), arcRect, degreesToRadians(self.facing) - degreesToRadians(self.visorLength) / 2,
                        degreesToRadians(self.facing) + degreesToRadians(self.visorLength) / 2, width=int(self.radius / 6))
        self.gun.draw(win, WIDTH / 2, HEIGHT / 2, self.radius, self.facing)
        if self.shooting:
            mouseX, mouseY = pygame.mouse.get_pos()
            self.gun.shoot(win, WIDTH / 2, HEIGHT / 2, self.radius, self.facing, mouseX, mouseY, self.x, self.y, walls)

    def getPos(self):
        return self.x, self.y

    def updatePos(self, walls):
        keys = pygame.key.get_pressed()
        vel = [0, 0]
        if keys[pygame.K_w]:
            vel[1] -= 1
        if keys[pygame.K_a]:
            vel[0] -= 1
        if keys[pygame.K_s]:
            vel[1] += 1
        if keys[pygame.K_d]:
            vel[0] += 1
        if keys[pygame.K_LSHIFT]:
            if self.sprintFrames > 0:
                self.speed = self.SPRINT_SPEED
                self.sprintFrames -=1
                self.sprintCdFrames = self.SPRINT_RUNOUT_CD_FRAMES if self.sprintFrames == 0 else self.SPRINT_CD_FRAMES
            else:
                self.speed = self.BASE_SPEED
                self.decrementSprintCdFrames()
                if self.sprintCdFrames <= 0:
                    self.incrementSprintFrames()
        else:
            self.speed = self.BASE_SPEED
            self.decrementSprintCdFrames()
            if self.sprintCdFrames <= 0:
                self.incrementSprintFrames()
        if keys[pygame.K_r]:
            self.gun.reload()
        if self.isRunningIntoWall(self.x, self.y, vel[0] * (self.speed + self.radius), 0, walls):
            vel[0] = 0
        if self.isRunningIntoWall(self.x, self.y, 0, vel[1] * (self.speed + self.radius), walls):
            vel[1] = 0
        velDir = getCordsDirectionDeg(vel[0], vel[1])
        deltaX, deltaY = getRectCordsOnCircleDeg(velDir, 0 if vel[0] == 0 and vel[1] == 0 else self.speed)
        self.x += deltaX
        self.y += deltaY
        mouseX, mouseY = pygame.mouse.get_pos()
        self.facing = radiansToDegrees(math.atan2(-(mouseY - HEIGHT / 2), mouseX - WIDTH / 2))
        self.gun.decrementShotCdFrames()

    def incrementSprintFrames(self):
        self.sprintFrames = min(self.sprintFrames + 1, self.MAX_SPRINT_FRAMES)

    def decrementSprintCdFrames(self):
        self.sprintCdFrames = max(self.sprintCdFrames - 1, 0)

    def checkShooting(self, events):
        self.shooting = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.shooting = True

    def isRunningIntoWall(self, x3, y3, xv, yv, walls):
        x4, y4 = x3 + xv, y3 + yv
        for wall in walls:
            for i in range(len(wall.innerPoints) - 1):
                x1, y1, x2, y2 = wall.innerPoints[i][0], wall.innerPoints[i][1], wall.innerPoints[i + 1][0], wall.innerPoints[i + 1][1]
                denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
                if denominator != 0:
                    t = numerator / denominator
                    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
                    if 0 <= t <= 1 and 0 <= u <= 1:
                        return True
        return False

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
