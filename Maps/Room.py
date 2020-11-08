import pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()
from Constants import *

class Room:

    def __init__(self, Xi=0, Yi=0, Xf=0, Yf=0):
        self.Xi, self.Yi, self.Xf, self.Yf = Xi, Yi, Xf, Yf
        self.patterns = []
        self.walls = []

    def draw(self, win, x, y, mapFOV):
        fov = mapFOV / max(WIDTH, HEIGHT)
        deltaX, deltaY = WIDTH / 2 - x, HEIGHT / 2 - y
        for i in range(len(self.patterns)):
            self.patterns[i].drawRect(win, self.Xi + deltaX, self.Yi + deltaY, self.Xf + deltaX, self.Yf + deltaY, fov)
        for i in range(len(self.walls)):
            self.walls[i].draw(win, x, y, fov)

    def getName(self):
        return ""

    def drawRoomName(self, win):
        myfont = pygame.font.SysFont(FONT, 48)
        text = myfont.render(self.getName(), False, (128, 64, 64))
        text2 = myfont.render(self.getName(), False, (255, 0, 0))
        win.blit(text2, (9, 10))
        win.blit(text, (8, 8))

    def removeWall(self, wall):
        for w in self.walls:
            if w.points == wall.points:
                self.walls.remove(w)
                pygame.mixer.Channel(PURCHASE_SOUND_CHANNEL).play(pygame.mixer.Sound(BUY_SOUND), maxtime=1300)

    def generateWallPointsBetweenDoors(self, width=10):
        roomCorners = [(self.Xi, self.Yi), (self.Xi, self.Yf), (self.Xf, self.Yf), (self.Xf, self.Yi)]
        wallPoints = [[]] * len(self.walls)
        for i in range(len(self.walls)):        # Doors Must Rotate Around Room Clockwise
            wallInnerPoints = []
            wallOuterPoints = []
            x1, y1 = self.walls[i].innerPoints[1]
            x2, y2 = self.walls[(i + 1) % len(self.walls)].innerPoints[0]
            wallInnerPoints.append((x1, y1))
            if x1 == self.Xi:
                wallOuterPoints.append((x1 - width, y1))
            elif x1 == self.Xf:
                wallOuterPoints.append((x1 + width, y1))
            elif y1 == self.Yi:
                wallOuterPoints.append((x1, y1 - width))
            elif y1 == self.Yf:
                wallOuterPoints.append((x1, y1 + width))
            while x1 != x2 and y1 != y2:        # While no flat line exists between (x1, y1) and (x2, y2)
                if (x1 == self.Xi or x1 == self.Xf) and (y1 == self.Yi or y1 == self.Yf):       # If at a corner
                    if x1 == self.Xi and y1 == self.Yi:
                        y1 = self.Yf
                        wallOuterPoints.append((x1 - width, y1 + width))
                    elif x1 == self.Xi and y1 == self.Yf:
                        x1 = self.Xf
                        wallOuterPoints.append((x1 + width, y1 + width))
                    elif x1 == self.Xf and y1 == self.Yf:
                        y1 = self.Yi
                        wallOuterPoints.append((x1 + width, y1 - width))
                    elif x1 == self.Xf and y1 == self.Yi:
                        x1 = self.Xi
                        wallOuterPoints.append((x1 - width, y1 - width))
                else:           # If on a wall, not a corner, rotate to next clockwise corner
                    if x1 == self.Xi:
                        y1 = self.Yf
                        wallOuterPoints.append((x1 - width, y1 + width))
                    elif x1 == self.Xf:
                        y1 = self.Yi
                        wallOuterPoints.append((x1 + width, y1 - width))
                    elif y1 == self.Yi:
                        x1 = self.Xi
                        wallOuterPoints.append((x1 - width, y1 - width))
                    elif y1 == self.Yf:
                        x1 = self.Xf
                        wallOuterPoints.append((x1 + width, y1 + width))
                wallInnerPoints.append((x1, y1))
            wallInnerPoints.append((x2, y2))
            if x2 == self.Xi:
                wallOuterPoints.append((x2 - width, y2))
            elif x2 == self.Xf:
                wallOuterPoints.append((x2 + width, y2))
            elif y2 == self.Yi:
                wallOuterPoints.append((x2, y2 - width))
            elif y2 == self.Yf:
                wallOuterPoints.append((x2, y2 + width))
            wallPoints[i] = wallInnerPoints
            wallPoints[i].extend(reversed(wallOuterPoints))
        return wallPoints
