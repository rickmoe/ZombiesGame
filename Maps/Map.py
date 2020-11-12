import pygame
from Constants import *
pygame.init()

class Map:

    def __init__(self):
        self.rooms = []
        self.renderedWalls = []
        self.doors = []
        self.currRoom = None

    def draw(self, win, x, y, mapFOV):
        self.renderedWalls = []
        self.currRoom = None
        Xi, Yi, Xf, Yf = x - mapFOV / 2, y - mapFOV / 2, x + mapFOV / 2, y + mapFOV / 2
        for room in self.rooms:
            if min(room.Xf, Xf) >= max(room.Xi, Xi) and min(room.Yf, Yf) >= max(room.Yi, Yi):
                room.draw(win, x, y, mapFOV)
                self.renderedWalls.extend(room.walls)
            for rect in room.rects:
                if rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]:
                    self.currRoom = room

    def getRenderedWalls(self):
        return self.renderedWalls

    def getCurrRoom(self):
        return self.currRoom

    def buyDoor(self, door):
        for d in self.doors:
            if d.points == door.points:
                self.doors.remove(d)
                for r in door.getRooms():
                    for room in self.rooms:
                        if isinstance(room, r):
                            room.removeWall(d)
                pygame.mixer.Channel(PURCHASE_SOUND_CHANNEL).play(pygame.mixer.Sound(BUY_SOUND), maxtime=1300)
                return True
        return False