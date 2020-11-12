from Maps.Map import Map
from Maps.Door import Door
from Maps.Map1.Rooms.SpawnRoom import SpawnRoom
from Maps.Map1.Rooms.SpawnFurnaceHallway import SpawnFurnaceHallway
from Maps.Map1.Rooms.FurnaceRoom import FurnaceRoom

class Map1(Map):

    def __init__(self):
        super().__init__()
        self.doors = [Door([(-350, -75), (-350, 75)], '+x', 500, [SpawnRoom, SpawnFurnaceHallway]),
                      Door([(-50, 200), (75, 200)], '-y', 750, [SpawnRoom]),
                      Door([(300, -200), (150, -200)], '+y', 1000, [SpawnRoom]),
                      Door([(-640, -74), (-640, 74)], '+x', 500, [SpawnFurnaceHallway, FurnaceRoom]),
                      Door([(-1000, -250), (-1150, -250)], '+y', 750, [FurnaceRoom]),
                      ]
        self.rooms = [SpawnRoom(self.doors), SpawnFurnaceHallway(self.doors), FurnaceRoom(self.doors)]
