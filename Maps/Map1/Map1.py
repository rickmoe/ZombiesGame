from Maps.Map import Map
from Maps.Map1.Rooms.SpawnRoom import SpawnRoom

class Map1(Map):

    def __init__(self):
        super().__init__()
        self.rooms = [SpawnRoom()]