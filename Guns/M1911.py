import pygame
from Gun import Gun
pygame.init()

class M1911(Gun):

    LENGTH = 1.2                    # Multiplied by radius
    DRAW_DIST_FROM_CENTER = 0.9     # Percentage of the body before the gun is drawn

    def __init__(self):
        pass

    def draw(self, win, x, y, r, theta):
        r *= self.DRAW_DIST_FROM_CENTER
        pygame.draw.line(win, (64, 64, 64), self.getDrawStartPos(x, y, r, theta), self.getDrawEndPos(x , y , r, theta, self.LENGTH * r), width=4)

    @staticmethod
    def getName():
        return "M1911"
