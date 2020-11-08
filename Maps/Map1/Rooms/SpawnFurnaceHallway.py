from Maps.Map1.Patterns.WhiteTile import WhiteTile
from Maps.Room import Room
from Maps.Wall import Wall
from Maps.Door import Door

class SpawnFurnaceHallway(Room):

    def __init__(self):
        super().__init__(-650, -125, -350, 125)
        self.patterns = [WhiteTile()]
        self.walls = [Door([(-650, -75), (-650, 75)], '+x', 500),
                      Door([(-350, 75), (-350, -75)], '-y', 750)]
        for pointSet in self.generateWallPointsBetweenDoors():
            self.walls.append(Wall(pointSet))

    def getName(self):
        return "Hallway"
