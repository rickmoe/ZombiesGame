from Maps.Map1.Patterns.WhiteTile import WhiteTile
from Maps.Room import Room
from Maps.Wall import Wall

class SpawnGameHallway(Room):

    def __init__(self, doors):
        super().__init__(doors, [(125, -800, 200, 590), (-375, -800, 500, 200), (-375, -1290, 200, 490)])
        self.patterns = [WhiteTile()]
        self.doors = [door for door in doors if SpawnGameHallway in door.getRooms()]
        self.walls = self.doors
        for pointSet in self.generateWallPointsBetweenDoors():
            self.walls.append(Wall(pointSet))

    def getName(self):
        return "Hallway"
