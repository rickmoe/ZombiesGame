from Maps.Map1.Patterns.WhiteTile import WhiteTile
from Maps.Room import Room
from Maps.Wall import Wall
from Maps.Door import Door

class FurnaceRoom(Room):

    def __init__(self):
        super().__init__(-1300, -250, -650, 100)
        self.patterns = [WhiteTile()]
        self.walls = [Door([(-650, -75), (-650, 75)], '-x', 500),
                      Door([(-1000, -250), (-1150, -250)], '+y', 750)]
        for pointSet in self.generateWallPointsBetweenDoors():
            self.walls.append(Wall(pointSet))

    def getName(self):
        return "Furnace Room"
