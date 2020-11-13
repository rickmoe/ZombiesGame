import pygame
import math
from Constants import *
from DelayedAction import DelayedAction
pygame.init()
pygame.mixer.init()

class Gun:

    LENGTH = 2.0                    # Multiplied by radius
    DRAW_DIST_FROM_CENTER = 0.9     # Percentage of the body before the gun is drawn
    MAX_BULLET_LENGTH = 1.5 * max(WIDTH, HEIGHT)
    SHOOT_SOUND = ''
    CLICK_SOUND = ''
    RELOAD_SOUND = ''
    AMMO_CLIP = 0
    AMMO_RESERVE = 0
    SHOT_CD_FRAMES = 0
    SHOT_CD_RELOAD_FRAMES = 0
    SHOOT_SOUND_MAXTIME = 0
    ammoClip = AMMO_CLIP
    ammoReserve = AMMO_RESERVE
    shotCdFrames = 0
    reloadCdFrames = 0
    automatic = False

    @classmethod
    def drawGUI(cls, win, ammoClip, ammoRes):
        gunFont = pygame.font.SysFont(GUN_FONT, 56)
        gunFontSmall = pygame.font.SysFont(GUN_FONT, 32)
        nameText = gunFont.render(cls.getName(), False, (128, 64, 64))
        nameText2 = gunFont.render(cls.getName(), False, (32, 32, 32))
        ammoText = gunFontSmall.render('{}/{}'.format(ammoClip, ammoRes), False, (96, 48, 48))
        ammoText2 = gunFontSmall.render('{}/{}'.format(ammoClip, ammoRes), False, (32, 32, 32))
        nameTextRect = nameText.get_rect()
        nameTextRect2 = nameText2.get_rect()
        nameTextRect.bottomright = (WIDTH, HEIGHT)
        nameTextRect2.bottomright = (nameTextRect.bottomright[0] + 3, nameTextRect.bottomright[1] + 3)
        ammoTextRect = ammoText.get_rect()
        ammoTextRect2 = ammoText2.get_rect()
        ammoTextRect.bottomright = nameTextRect.topright
        ammoTextRect2.bottomright = (ammoTextRect.bottomright[0] + 3, ammoTextRect.bottomright[1] + 3)
        win.blit(nameText2, nameTextRect2)
        win.blit(nameText, nameTextRect)
        win.blit(ammoText2, ammoTextRect2)
        win.blit(ammoText, ammoTextRect)

    @staticmethod
    def getName():
        return ""

    def getAmmoClip(self):
        return self.ammoClip

    def getAmmoReserve(self):
        return self.ammoReserve

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

    def shoot(self, win, x, y, r, theta, mouseX, mouseY, playerX, playerY, walls):
        if self.ammoClip > 0:
            if self.shotCdFrames <= 0:
                Xi, Yi = self.getDrawEndPos(playerX, playerY, r, theta, self.LENGTH * r)
                shotAngle = radiansToDegrees(math.atan2(-(mouseY - HEIGHT / 2), mouseX - WIDTH / 2))
                Xv, Yv = math.cos(degreesToRadians(shotAngle)), -math.sin(degreesToRadians(shotAngle))
                finalX, finalY = tuple(getWallIntersection(Xi, Yi, Xv, Yv, walls))
                finalX += WIDTH / 2 - playerX
                finalY += HEIGHT / 2 - playerY
                self.drawLineOfFire(win, x, y, finalX, finalY, r, theta)
                self.drawWallHitmarker(win, finalX, finalY)
                self.ammoClip -= 1
                self.shotCdFrames = self.SHOT_CD_FRAMES
                pygame.mixer.Channel(GUN_SHOT_CHANNEL).play(pygame.mixer.Sound(self.SHOOT_SOUND), maxtime=self.SHOOT_SOUND_MAXTIME)
        else:
            if self.shotCdFrames <= 0:
                pygame.mixer.Channel(GUN_SHOT_CHANNEL).play(pygame.mixer.Sound(self.CLICK_SOUND))

    def reload(self):
        if self.ammoReserve > 0 and self.ammoClip < self.AMMO_CLIP and self.reloadCdFrames <= 0:
            bullets = min(self.AMMO_CLIP - self.ammoClip, self.ammoReserve)
            DelayedAction([[self.SHOT_CD_RELOAD_FRAMES, self.takeFromReserve, [bullets]], [self.SHOT_CD_RELOAD_FRAMES, self.addToClip, [bullets]]])
            self.shotCdFrames = self.SHOT_CD_RELOAD_FRAMES
            self.reloadCdFrames = self.SHOT_CD_RELOAD_FRAMES
            pygame.mixer.music.load(self.RELOAD_SOUND)
            pygame.mixer.music.play()

    def decrementShotCdFrames(self):
        self.shotCdFrames = 0 if self.shotCdFrames <= 0 else self.shotCdFrames - 1
        self.reloadCdFrames = 0 if self.reloadCdFrames <= 0 else self.reloadCdFrames - 1

    def drawWallHitmarker(self, win, x, y):
        vals = [[1, 2, 2], [2, 3, 3], [3, 5, 6], [4, 6, 5], [6, 7, 2]]
        colors = [(128, 64, 0), (128, 16, 0)]
        MULT_1D = 1.8
        for i, val in enumerate(vals):
            for color in colors:
                DelayedAction([[i, pygame.draw.line, [win, color, (x - val[0], y - val[0]), (x - val[1], y - val[1]), val[2]]],
                               [i, pygame.draw.line, [win, color, (x - val[0], y + val[0]), (x - val[1], y + val[1]), val[2]]],
                               [i, pygame.draw.line, [win, color, (x + val[0], y - val[0]), (x + val[1], y - val[1]), val[2]]],
                               [i, pygame.draw.line, [win, color, (x + val[0], y + val[0]), (x + val[1], y + val[1]), val[2]]],
                               [i, pygame.draw.line, [win, color, (x, y - val[0] * MULT_1D), (x, y - val[1] * MULT_1D), val[2] - 2]],
                               [i, pygame.draw.line, [win, color, (x - val[0] * MULT_1D, y), (x - val[1] * MULT_1D, y), val[2] - 2]],
                               [i, pygame.draw.line, [win, color, (x, y + val[0] * MULT_1D), (x, y + val[1] * MULT_1D), val[2] - 2]],
                               [i, pygame.draw.line, [win, color, (x + val[0] * MULT_1D, y), (x + val[1] * MULT_1D, y), val[2] - 2]]])

    def drawLineOfFire(self, win, Xi, Yi, Xf, Yf, r, theta):
        DelayedAction([[0, pygame.draw.line, [win, (255, 255, 255), self.getDrawEndPos(Xi, Yi, r, theta, self.LENGTH * r), (Xf, Yf), 2]],
                       [1, pygame.draw.line, [win, (255, 255, 255), self.getDrawEndPos(Xi, Yi, r, theta, self.LENGTH * r), (Xf, Yf), 2]],
                       ])

    def takeFromReserve(self, bullets):
        self.ammoReserve -= bullets

    def addToClip(self, bullets):
        self.ammoClip += bullets

def degreesToRadians(deg):
    return deg / 180 * math.pi

def radiansToDegrees(rad):
    return rad * 180 / math.pi

def getRectCordsOnCircleRad(rad, r):
    x, y = (r * math.cos(rad), r * math.sin(rad))
    return x, -y

def getRectCordsOnCircleDeg(deg, r):
    return getRectCordsOnCircleRad(degreesToRadians(deg), r)

def getWallIntersection(Xi, Yi, Xv, Yv, walls):
    Xf, Yf = Xi + Xv * Gun.MAX_BULLET_LENGTH, Yi + Yv * Gun.MAX_BULLET_LENGTH
    for wall in walls:
        for i in range(len(wall.points)):
            x1, y1, x2, y2 = wall.points[i][0], wall.points[i][1], wall.points[(i + 1) % len(wall.points)][0], wall.points[(i + 1) % len(wall.points)][1]
            denominator = (x1 - x2) * (Yi - Yf) - (y1 - y2) * (Xi - Xf)
            numerator = (x1 - Xi) * (Yi - Yf) - (y1 - Yi) * (Xi - Xf)
            if denominator != 0:
                t = numerator / denominator
                u = -((x1 - x2) * (y1 - Yi) - (y1 - y2) * (x1 - Xi)) / denominator
                if 0 <= t <= 1 and 0 <= u <= 1:
                    Xf, Yf = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
    return Xf, Yf
