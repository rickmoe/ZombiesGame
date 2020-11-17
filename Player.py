import pygame
pygame.init()
import math
from Constants import *
from Guns.M1911 import M1911
from Guns.DesertEagle import DesertEagle
from Guns.FiveSeven import FiveSeven
from Maps.Door import Door

class Player:

    visorRadiusOffsetPercent = 1.025
    VISOR_LEN_DEG = 90
    BASE_SPEED = 5.0
    SPRINT_SPEED = 7.5
    AWARENESS_RANGE = 4.0       # Multiplied By Radius To See How Far Away Player Can Detect Doors, Wall Buys, etc.
    MAX_SPRINT_FRAMES = 90
    SPRINT_CD_FRAMES = 45
    SPRINT_RUNOUT_CD_FRAMES = 90
    START_POINTS = 10000

    def __init__(self, x, y, radius=20, facingDeg=180):
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = facingDeg                 # In Degrees
        self.speed = self.BASE_SPEED
        self.gun1 = M1911()
        self.gun2 = None
        self.gun = self.gun1
        self.gunSwitchRisingEdge = True
        self.points = Player.START_POINTS
        self.sprintFrames = Player.MAX_SPRINT_FRAMES
        self.sprintCdFrames = 0
        self.shooting = False
        self.nearbyDoor = None
        self.nearbyWallBuy = None
        self.shotVect = None

    def draw(self, win, walls):
        pygame.draw.circle(win, (0, 0, 255), (WIDTH / 2, HEIGHT / 2), self.radius)
        arcRect = (int(WIDTH / 2 - self.radius * self.visorRadiusOffsetPercent), int(HEIGHT / 2 - self.radius * self.visorRadiusOffsetPercent),
                        int(self.radius * self.visorRadiusOffsetPercent * 2), int(self.radius * self.visorRadiusOffsetPercent * 2))
        pygame.draw.arc(win, (0, 255, 0), arcRect, degreesToRadians(self.facing) - degreesToRadians(self.VISOR_LEN_DEG) / 2,
                        degreesToRadians(self.facing) + degreesToRadians(self.VISOR_LEN_DEG) / 2, width=int(self.radius / 6))
        self.gun.draw(win, WIDTH / 2, HEIGHT / 2, self.radius, self.facing)
        if self.shooting:
            mouseX, mouseY = pygame.mouse.get_pos()
            self.shotVect = self.gun.shoot(win, WIDTH / 2, HEIGHT / 2, self.radius, self.facing, mouseX, mouseY, self.x, self.y, walls)
        else:
            self.shotVect = None
        if self.shotVect is not None:
            self.gun.drawLineOfFire(win, self.x, self.y, *self.shotVect)
            self.gun.drawWallHitmarker(win, self.x, self.y, *self.shotVect[2:])
            pygame.mixer.Channel(GUN_SHOT_CHANNEL).play(pygame.mixer.Sound(self.gun.SHOOT_SOUND), maxtime=self.gun.SHOOT_SOUND_MAXTIME)
        self.drawPoints(win)
        self.drawNearbyDoorCost(win)
        self.drawNearbyWallBuyCost(win)

    def getPos(self):
        return self.x, self.y

    def updatePos(self, walls, wallBuys):
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
                self.sprintFrames -= 1
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
        self.speed *= self.gun.getSpeedMult()
        if keys[pygame.K_r]:
            self.gun.reload()
        if self.isRunningIntoWall(self.x, self.y, vel[0] * (self.speed + self.radius), 0, walls):
            vel[0] = 0
        if self.isRunningIntoWall(self.x, self.y, 0, vel[1] * (self.speed + self.radius), walls):
            vel[1] = 0
        checkVels = [(0, self.radius * self.AWARENESS_RANGE), (0, -self.radius * self.AWARENESS_RANGE), (self.radius * self.AWARENESS_RANGE, 0), (-self.radius * self.AWARENESS_RANGE, 0)]
        for velocity in checkVels:
            if self.doorRunningInto(self.x, self.y, velocity[0], velocity[1], walls) is not None:
                self.nearbyDoor = self.doorRunningInto(self.x, self.y, velocity[0], velocity[1], walls)
                break
        else:
            self.nearbyDoor = None
        for velocity in checkVels:
            if self.wallBuyRunningInto(self.x, self.y, velocity[0], velocity[1], wallBuys) is not None:
                self.nearbyWallBuy = self.wallBuyRunningInto(self.x, self.y, velocity[0], velocity[1], wallBuys)
                break
        else:
            self.nearbyWallBuy = None
        if keys[pygame.K_x]:
            if self.gunSwitchRisingEdge:
                if self.gun is self.gun1:
                    self.gun = self.gun2 if self.gun2 is not None else self.gun
                elif self.gun is self.gun2:
                    self.gun = self.gun1 if self.gun1 is not None else self.gun
            self.gunSwitchRisingEdge = False
        else:
            self.gunSwitchRisingEdge = True
        velDir = getCordsDirectionDeg(vel[0], vel[1])
        deltaX, deltaY = getRectCordsOnCircleDeg(velDir, 0 if vel[0] == 0 and vel[1] == 0 else self.speed)
        self.x += deltaX
        self.y += deltaY
        mouseX, mouseY = pygame.mouse.get_pos()
        self.facing = radiansToDegrees(math.atan2(-(mouseY - HEIGHT / 2), mouseX - WIDTH / 2))
        self.gun.decrementShotCdFrames()

    def checkDoorBuy(self, currMap):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and self.nearbyDoor is not None and self.points >= self.nearbyDoor.getCost():
            if currMap.buyDoor(self.nearbyDoor):
                self.points -= self.nearbyDoor.getCost()

    def checkGunBuy(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and self.nearbyWallBuy is not None and self.points >= self.nearbyWallBuy.getGunCost():
            if not isinstance(self.gun1, self.nearbyWallBuy.gunType) and not isinstance(self.gun2, self.nearbyWallBuy.gunType):
                if self.gun2 is None:
                    self.gun2 = self.nearbyWallBuy.gunType()
                    self.gun = self.gun2
                    self.points -= self.nearbyWallBuy.getGunCost()
                    pygame.mixer.Channel(PURCHASE_SOUND_CHANNEL).play(pygame.mixer.Sound(BUY_SOUND), maxtime=1300)
                elif self.gun1 is None:
                    self.gun1 = self.nearbyWallBuy.gunType()
                    self.gun = self.gun1
                    self.points -= self.nearbyWallBuy.getGunCost()
                    pygame.mixer.Channel(PURCHASE_SOUND_CHANNEL).play(pygame.mixer.Sound(BUY_SOUND), maxtime=1300)
                else:
                    if self.gun is self.gun1:
                        self.gun1 = self.nearbyWallBuy.gunType()
                        self.gun = self.gun1
                    elif self.gun is self.gun2:
                        self.gun2 = self.nearbyWallBuy.gunType()
                        self.gun = self.gun2
                    self.points -= self.nearbyWallBuy.getGunCost()
                    pygame.mixer.Channel(PURCHASE_SOUND_CHANNEL).play(pygame.mixer.Sound(BUY_SOUND), maxtime=1300)
            else:
                if isinstance(self.gun1, self.nearbyWallBuy.gunType):
                    if not self.gun1.isMaxAmmo():
                        self.gun1.fillAmmo()
                        self.points -= self.nearbyWallBuy.getAmmoCost()
                        pygame.mixer.Channel(PURCHASE_SOUND_CHANNEL).play(pygame.mixer.Sound(BUY_SOUND), maxtime=1300)
                elif isinstance(self.gun2, self.nearbyWallBuy.gunType):
                    if not self.gun2.isMaxAmmo():
                        self.gun2.fillAmmo()
                        self.points -= self.nearbyWallBuy.getAmmoCost()
                        pygame.mixer.Channel(PURCHASE_SOUND_CHANNEL).play(pygame.mixer.Sound(BUY_SOUND), maxtime=1300)

    def drawPoints(self, win):
        pointFont = pygame.font.SysFont(GUN_FONT, 32)
        pointsText = pointFont.render(str(self.points), False, (128, 64, 64))
        pointsText2 = pointFont.render(str(self.points), False, (32, 32, 32))
        pointsTextRect = pointsText.get_rect()
        pointsTextRect2 = pointsText2.get_rect()
        pointsTextRect.bottomleft = (WIDTH * (1 / 80), HEIGHT * (18 / 20))
        pointsTextRect2.bottomright = (pointsTextRect.bottomright[0] + 3, pointsTextRect.bottomright[1] + 3)
        win.blit(pointsText2, pointsTextRect2)
        win.blit(pointsText, pointsTextRect)

    def drawNearbyDoorCost(self, win):
        if self.nearbyDoor is not None:
            costFont = pygame.font.SysFont(GUN_FONT, 32)
            costText = costFont.render('Door: {} Points'.format(self.nearbyDoor.getCost()), False, (255, 64, 64))
            costText2 = costFont.render('Door: {} Points'.format(self.nearbyDoor.getCost()), False, (32, 32, 32))
            costTextRect = costText.get_rect()
            costTextRect2 = costText2.get_rect()
            costTextRect.center = (WIDTH / 2, HEIGHT * (16 / 20))
            costTextRect2.center = (costTextRect.center[0] + 2, costTextRect.center[1] + 2)
            win.blit(costText2, costTextRect2)
            win.blit(costText, costTextRect)

    def drawNearbyWallBuyCost(self, win):
        if self.nearbyWallBuy is not None:
            costFont = pygame.font.SysFont(GUN_FONT, 32)
            costText = costFont.render('{}: {} Points'.format(self.nearbyWallBuy.getGunReference().getName(), self.nearbyWallBuy.getGunCost()), False, (255, 64, 64))
            costText2 = costFont.render('{}: {} Points'.format(self.nearbyWallBuy.getGunReference().getName(), self.nearbyWallBuy.getGunCost()), False, (32, 32, 32))
            ammoCostText = costFont.render('Ammo: {} Points'.format(self.nearbyWallBuy.getAmmoCost()), False, (255, 64, 64))
            ammoCostText2 = costFont.render('Ammo: {} Points'.format(self.nearbyWallBuy.getAmmoCost()), False, (32, 32, 32))
            costTextRect = costText.get_rect()
            costTextRect2 = costText2.get_rect()
            ammoCostTextRect = ammoCostText.get_rect()
            ammoCostTextRect2 = ammoCostText2.get_rect()
            costTextRect.center = (WIDTH / 2, HEIGHT * (31 / 40))
            costTextRect2.center = (costTextRect.center[0] + 2, costTextRect.center[1] + 2)
            ammoCostTextRect.center = (WIDTH / 2, HEIGHT * (33 / 40))
            ammoCostTextRect2.center = (ammoCostTextRect.center[0] + 2, ammoCostTextRect.center[1] + 2)
            win.blit(costText2, costTextRect2)
            win.blit(costText, costTextRect)
            win.blit(ammoCostText2, ammoCostTextRect2)
            win.blit(ammoCostText, ammoCostTextRect)

    def incrementSprintFrames(self):
        self.sprintFrames = min(self.sprintFrames + 1, self.MAX_SPRINT_FRAMES)

    def decrementSprintCdFrames(self):
        self.sprintCdFrames = max(self.sprintCdFrames - 1, 0)

    def checkShooting(self, events):
        self.shooting = False
        if not self.gun.automatic:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.shooting = True
        elif self.gun.automatic and events.mouse.get_pressed()[0]:
            self.shooting = True

    def isRunningIntoWall(self, x3, y3, xv, yv, walls):
        x4, y4 = x3 + xv, y3 + yv
        for wall in walls:
            for i in range(len(wall.points)):
                x1, y1, x2, y2 = wall.points[i][0], wall.points[i][1], wall.points[(i + 1) % len(wall.points)][0], wall.points[(i + 1) % len(wall.points)][1]
                denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
                if denominator != 0:
                    t = numerator / denominator
                    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
                    if 0 <= t <= 1 and 0 <= u <= 1:
                        return True
        return False

    def doorRunningInto(self, x3, y3, xv, yv, walls):
        x4, y4 = x3 + xv, y3 + yv
        for wall in walls:
            if isinstance(wall, Door):
                for i in range(len(wall.innerPoints) - 1):
                    x1, y1, x2, y2 = wall.innerPoints[i][0], wall.innerPoints[i][1], wall.innerPoints[i + 1][0], wall.innerPoints[i + 1][1]
                    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                    numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
                    if denominator != 0:
                        t = numerator / denominator
                        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
                        if 0 <= t <= 1 and 0 <= u <= 1:
                            return wall
        return None

    def wallBuyRunningInto(self, x3, y3, xv, yv, wallBuys):
        x4, y4 = x3 + xv, y3 + yv
        for wallBuy in wallBuys:
            for i in range(len(wallBuy.points) - 1):
                x1, y1, x2, y2 = wallBuy.points[i][0], wallBuy.points[i][1], wallBuy.points[i + 1][0], wallBuy.points[i + 1][1]
                denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
                if denominator != 0:
                    t = numerator / denominator
                    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
                    if 0 <= t <= 1 and 0 <= u <= 1:
                        return wallBuy
        return None

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
