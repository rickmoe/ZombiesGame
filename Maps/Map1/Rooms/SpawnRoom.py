from Maps.Map1.Patterns.WhiteTile import WhiteTile
from Maps.Room import Room

class SpawnRoom(Room):

    def __init__(self):
        super().__init__(100, 100, 700, 700)
        self.patterns = [WhiteTile()]
