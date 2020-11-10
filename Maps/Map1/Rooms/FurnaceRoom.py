from Maps.Map1.Patterns.WhiteTile import WhiteTile
from Maps.Room import Room
from Maps.Wall import Wall

class FurnaceRoom(Room):

    def __init__(self, doors):
        super().__init__(doors, -1320, -250, -650, 100)
        self.patterns = [WhiteTile()]
        self.doors = [door for door in doors if FurnaceRoom in door.getRooms()]
        self.walls = self.doors
        for pointSet in self.generateWallPointsBetweenDoors():
            self.walls.append(Wall(pointSet))

    def getName(self):
        return "Furnace Room"
