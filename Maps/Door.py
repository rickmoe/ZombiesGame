from Maps.Wall import Wall

class Door(Wall):

    COLOR = (139, 69, 19)

    def __init__(self, points, orientation, cost, rooms, width=10):
        self.points = points
        if orientation == '+x':
            self.points.extend([(val[0] - width, val[1]) for val in reversed(self.points)])
        elif orientation == '-x':
            self.points.extend([(val[0] + width, val[1]) for val in reversed(self.points)])
        elif orientation == '-y':
            self.points.extend([(val[0], val[1] + width) for val in reversed(self.points)])
        else:
            self.points.extend([(val[0], val[1] - width) for val in reversed(self.points)])
        super().__init__(points, 4)
        self.cost = cost
        self.rooms = rooms

    def getCost(self):
        return self.cost

    def getRooms(self):
        return self.rooms
