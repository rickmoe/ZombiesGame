from Maps.Map import Map
from Maps.Map1.Rooms.SpawnRoom import SpawnRoom
from Maps.Map1.Rooms.SpawnFurnaceHallway import SpawnFurnaceHallway
from Maps.Map1.Rooms.FurnaceRoom import FurnaceRoom

class Map1(Map):

    def __init__(self):
        super().__init__()
        self.rooms = [SpawnRoom()]#, SpawnFurnaceHallway(), FurnaceRoom()]
