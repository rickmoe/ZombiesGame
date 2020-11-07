import pygame
pygame.init()
pygame.font.init()
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
