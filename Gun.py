import pygame
import math
from Constants import *
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
    ammoClip = AMMO_CLIP
    ammoReserve = AMMO_RESERVE
    shotCdFrames = SHOT_CD_FRAMES

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
                pygame.draw.line(win, (255, 255, 255), self.getDrawEndPos(x, y, r, theta, self.LENGTH * r), (finalX, finalY), 3)
                self.drawWallHitmarker(win, finalX, finalY)
                self.ammoClip -= 1
                self.shotCdFrames = self.SHOT_CD_FRAMES
                pygame.mixer.music.load(self.SHOOT_SOUND)
                pygame.mixer.music.play()
        else:
            pygame.mixer.music.load(self.CLICK_SOUND)
            pygame.mixer.music.play()

    def reload(self):
        if self.ammoReserve > 0 and self.ammoClip < self.AMMO_CLIP:
            loadBullets = min(self.AMMO_CLIP - self.ammoClip, self.ammoReserve)
            self.ammoReserve -= loadBullets
            self.ammoClip += loadBullets
            self.shotCdFrames = self.SHOT_CD_RELOAD_FRAMES
            pygame.mixer.music.load(self.RELOAD_SOUND)
            pygame.mixer.music.play()

    def decrementShotCdFrames(self):
        self.shotCdFrames = 0 if self.shotCdFrames <= 0 else self.shotCdFrames - 1

    def drawWallHitmarker(self, win, x, y):
        pygame.draw.line(win, (128, 64, 0), (x - 6, y - 6), (x + 6, y + 6), 10)
        pygame.draw.line(win, (128, 64, 0), (x - 6, y + 6), (x + 6, y - 6), 10)
        pygame.draw.line(win, (128, 64, 0), (x, y - 8), (x, y + 8), 10)
        pygame.draw.line(win, (128, 64, 0), (x - 8, y), (x + 8, y), 10)

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
        for i in range(len(wall.innerPoints) - 1):
            x1, y1, x2, y2 = wall.innerPoints[i][0], wall.innerPoints[i][1], wall.innerPoints[i + 1][0], wall.innerPoints[i + 1][1]
            denominator = (x1 - x2) * (Yi - Yf) - (y1 - y2) * (Xi - Xf)
            numerator = (x1 - Xi) * (Yi - Yf) - (y1 - Yi) * (Xi - Xf)
            if denominator != 0:
                t = numerator / denominator
                u = -((x1 - x2) * (y1 - Yi) - (y1 - y2) * (x1 - Xi)) / denominator
                if 0 <= t <= 1 and 0 <= u <= 1:
                    xCol, yCol = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
                    return xCol, yCol
    return Xf, Yf
