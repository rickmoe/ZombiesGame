from Maps.Pattern import Pattern

class WhiteTile(Pattern):

    def __init__(self):
        super().__init__(50, 50)
        self.contourCords = [[(0, 0), (0, 50), (50, 0), 0], [(50, 0), (50, 50), (0, 50), 0], [(0, 0), (0, 50), 2], [(0, 0), (50, 0), 2], [(0, 50), (50, 50), 2], [(50, 0), (50, 50), 2]]
        self.contourColors = [(128, 128, 128), (112, 112, 112), (96, 96, 96), (96, 96, 96), (96, 96, 96), (96, 96, 96)]