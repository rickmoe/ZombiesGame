import pygame
pygame.init()

class Pattern:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rectDimensions = [[]]
        self.rectColors = []
        self.lineDimensions = [[]]
        self.lineColors = []

    def drawRect(self, win, Xi, Yi, Xf, Yf):
        for i in range(len(self.rectDimensions)):
            y = Yi
            while y < Yf:
                x = Xi
                while x < Xf:
                    pygame.draw.rect(win, self.rectColors[i], (x, y, self.rectDimensions[i][0], self.rectDimensions[i][1]))
                    x += self.width
                y += self.height
        for i in range(len(self.lineDimensions)):
            y = Yi
            while y < Yf:
                x = Xi
                while x < Xf:
                    pygame.draw.line(win, self.lineColors[i], (x + self.lineDimensions[i][0], y + self.lineDimensions[i][1]),
                                     (x + self.lineDimensions[i][2], (y + self.lineDimensions[i][3])), width=self.lineDimensions[i][4])
                    x += self.width
                y += self.height