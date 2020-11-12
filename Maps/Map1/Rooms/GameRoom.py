from Maps.Map1.Patterns.WhiteTile import WhiteTile
from Maps.Room import Room
from Maps.Wall import Wall

class GameRoom(Room):

    def __init__(self, doors):
        super().__init__(doors, [(-900, -1900, 550, 600), (-350, -1700, 250, 400)])
        self.patterns = [WhiteTile()]
        self.doors = [door for door in doors if GameRoom in door.getRooms()]
        self.walls = self.doors
        for pointSet in self.generateWallPointsBetweenDoors():
            self.walls.append(Wall(pointSet))

    def getName(self):
        return "Game Room"
