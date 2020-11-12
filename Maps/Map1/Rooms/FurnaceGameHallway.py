from Maps.Map1.Patterns.WhiteTile import WhiteTile
from Maps.Room import Room
from Maps.Wall import Wall

class FurnaceGameHallway(Room):

    def __init__(self, doors):
        super().__init__(doors, [(-1275, -1500, 200, 1240), (-1075, -1500, 165, 200)])
        self.patterns = [WhiteTile()]
        self.doors = [door for door in doors if FurnaceGameHallway in door.getRooms()]
        self.walls = self.doors
        for pointSet in self.generateWallPointsBetweenDoors():
            self.walls.append(Wall(pointSet))

    def getName(self):
        return "Hallway"
