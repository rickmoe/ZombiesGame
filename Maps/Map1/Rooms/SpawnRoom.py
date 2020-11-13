from Guns.FiveSeven import FiveSeven
from Maps.Map1.Patterns.WhiteTile import WhiteTile
from Maps.Room import Room
from Maps.Wall import Wall
from Maps.WallBuy import WallBuy

class SpawnRoom(Room):

    def __init__(self, doors):
        super().__init__(doors, [(-350, -200, 700, 400)])
        self.patterns = [WhiteTile()]
        self.doors = [door for door in doors if SpawnRoom in door.getRooms()]
        self.walls = self.doors
        for pointSet in self.generateWallPointsBetweenDoors():
            self.walls.append(Wall(pointSet))
        self.wallBuys = [WallBuy(FiveSeven, [(-290, -197), (-250, -197)], '+y', 1000, 500)]

    def getName(self):
        return "Spawn Room"
