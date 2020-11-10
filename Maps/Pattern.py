import pygame
pygame.init()

class Pattern:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.contourCords = [[]]
        self.contourColors = []

    def drawRect(self, win, Xi, Yi, Xf, Yf, fov):
        for i in range(len(self.contourCords)):
            y = Yi
            while y < Yf:
                x = Xi
                while x < Xf:
                    contPoints = [(min(x + self.contourCords[i][j][0], Xf), min(y + self.contourCords[i][j][1], Yf)) for j in range(len(self.contourCords[i]) - 1)]
                    if len(contPoints) > 2:
                        pygame.draw.polygon(win, self.contourColors[i], contPoints, self.contourCords[i][len(self.contourCords) - 1])
                    elif len(contPoints) == 2:
                        pygame.draw.line(win, self.contourColors[i], contPoints[0], contPoints[1], self.contourCords[i][2])
                    x += self.width
                y += self.height