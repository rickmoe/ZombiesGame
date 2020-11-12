from Maps.Map import Map
from Maps.Door import Door
from Maps.Map1.Rooms.SpawnRoom import SpawnRoom
from Maps.Map1.Rooms.SpawnFurnaceHallway import SpawnFurnaceHallway
from Maps.Map1.Rooms.FurnaceRoom import FurnaceRoom
from Maps.Map1.Rooms.SpawnGameHallway import SpawnGameHallway
from Maps.Map1.Rooms.GameRoom import GameRoom
from Maps.Map1.Rooms.FurnaceGameHallway import FurnaceGameHallway

class Map1(Map):

    def __init__(self):
        super().__init__()
        self.doors = [Door([(-350, -75), (-350, 75)], '+x', 500, [SpawnRoom, SpawnFurnaceHallway]),
                      Door([(-50, 200), (75, 200)], '-y', 750, [SpawnRoom]),
                      Door([(300, -200), (150, -200)], '+y', 1000, [SpawnRoom, SpawnGameHallway]),
                      Door([(-640, -74), (-640, 74)], '+x', 500, [SpawnFurnaceHallway, FurnaceRoom]),
                      Door([(-1100, -250), (-1250, -250)], '+y', 750, [FurnaceRoom, FurnaceGameHallway]),
                      Door([(-350, -1300), (-200, -1300)], '-y', 1250, [SpawnGameHallway, GameRoom]),
                      Door([(-900, -1475), (-900, -1325)], '+x', 750, [GameRoom, FurnaceGameHallway]),
                      ]
        self.rooms = [SpawnRoom(self.doors), SpawnFurnaceHallway(self.doors), FurnaceRoom(self.doors), SpawnGameHallway(self.doors), GameRoom(self.doors), FurnaceGameHallway(self.doors)]
