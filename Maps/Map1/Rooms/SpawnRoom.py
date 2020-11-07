from Maps.Map1.Patterns.WhiteTile import WhiteTile
from Maps.Room import Room
from Maps.Wall import Wall

class SpawnRoom(Room):

    def __init__(self):
        super().__init__(-300, -300, 300, 300)
        self.patterns = [WhiteTile()]
        self.walls = [Wall([(-300, 75), (-300, 300), (-75, 300), (-75, 310), (-310, 310), (-310, 75)]),
                      Wall([(-300, -75), (-300, -300), (125, -300), (125, -310), (-310, -310), (-310, -75)]),
                      Wall([(50, 300), (300, 300), (300, -300), (275, -300), (275, -310), (310, -310), (310, 310), (50, 310)])]

    def getName(self):
        return "Spawn Room"
