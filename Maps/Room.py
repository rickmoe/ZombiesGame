class Room:

    def __init__(self, Xi=0, Yi=0, Xf=0, Yf=0):
        self.Xi, self.Yi, self.Xf, self.Yf = Xi, Yi, Xf, Yf
        self.patterns = []

    def draw(self, win):
        for i in range(len(self.patterns)):
            self.patterns[i].drawRect(win, self.Xi, self.Yi, self.Xf, self.Yf)