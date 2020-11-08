from Maps.Map1.Patterns.WhiteTile import WhiteTile
from Maps.Room import Room
from Maps.Wall import Wall
from Maps.Door import Door

class SpawnRoom(Room):

    def __init__(self):
        super().__init__(-350, -200, 350, 200)
        self.patterns = [WhiteTile()]
        self.walls = [Door([(-350, -75), (-350, 75)], '+x', 500),
                      Door([(-50, 200), (75, 200)], '-y', 750),
                      Door([(300, -200), (150, -200)], '+y', 1000)]
        for pointSet in self.generateWallPointsBetweenDoors():
            self.walls.append(Wall(pointSet))

    def getName(self):
        return "Spawn Room"
