from Maps.Pattern import Pattern

class WhiteTile(Pattern):

    def __init__(self):
        super().__init__(50, 50)
        self.rectDimensions = [[50, 50]]
        self.rectColors = [(192, 192, 192)]
        self.lineDimensions = [[0, 0, 0, 50, 2], [0, 0, 50, 0, 2], [0, 50, 50, 50, 2], [50, 0, 50, 50, 2]]
        self.lineColors = [(128, 128, 128)] * 4
