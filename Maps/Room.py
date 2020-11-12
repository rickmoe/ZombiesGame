from shapely.geometry import Polygon
import pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()
from Constants import *

class Room:

    def __init__(self, doors, rects):
        self.rects = rects
        self.points = self.findRoomPoints(self.rects)
        self.Xi = min([x for x, y, w, h in self.rects])
        self.Yi = min([y for x, y, w, h in self.rects])
        self.Xf = max([x + w for x, y, w, h in self.rects])
        self.Yf = max([y + h for x, y, w, h in self.rects])
        self.patterns = []
        self.walls = []
        self.doors = []
        self.openedDoorPoints = []

    def draw(self, win, x, y, mapFOV):
        fov = mapFOV / max(WIDTH, HEIGHT)
        deltaX, deltaY = WIDTH / 2 - x, HEIGHT / 2 - y
        for i in range(len(self.patterns)):
            self.patterns[i].tileRect(win, [(x + deltaX, y + deltaY, w, h) for x, y, w, h in self.rects], fov)
        for i in range(len(self.walls)):
            self.walls[i].draw(win, x, y, fov)
        for pointSet in self.openedDoorPoints:
            xVals = [point[0] for point in pointSet]
            yVals = [point[1] for point in pointSet]
            pygame.draw.rect(win, (96, 96, 96), (min(xVals) + deltaX, min(yVals) + deltaY, max(xVals) - min(xVals), max(yVals) - min(yVals)))

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
                self.openedDoorPoints.append(w.points)
                return True
        return False

    @staticmethod
    def findRoomPoints(rects):
        poly = Polygon([(rects[0][0], rects[0][1]), (rects[0][0], rects[0][1] + rects[0][3]),
                        (rects[0][0] + rects[0][2], rects[0][1] + rects[0][3]), (rects[0][0] + rects[0][2], rects[0][1])])
        for i in range(1, len(rects)):
            poly = Polygon([(rects[i][0], rects[i][1]), (rects[i][0], rects[i][1] + rects[i][3]),
                            (rects[i][0] + rects[i][2], rects[i][1] + rects[i][3]), (rects[i][0] + rects[i][2], rects[i][1])]).union(poly)
        return list(poly.exterior.coords)[:-1]

    def generateWallPointsBetweenDoors(self, width=10):
        roomCorners = self.points
        roomPoly = Polygon(roomCorners)
        inflatedPoly = Polygon(self.findRoomPoints([(x - width, y - width, w + width * 2, h + width * 2) for x, y, w, h in self.rects]))
        for wall in self.walls:
            roomPoly = roomPoly.union(Polygon(wall.points))
        walls = inflatedPoly.difference(roomPoly)
        if isinstance(walls, Polygon):
            walls = [walls]
        else:
            walls = list(walls)
        walls = [list(s.exterior.coords)[:-1] for s in walls]
        return walls
