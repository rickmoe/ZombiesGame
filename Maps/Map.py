class Map:

    def __init__(self):
        self.rooms = []

    def draw(self, win, x, y, mapFOV):
        Xi, Yi, Xf, Yf = x - mapFOV / 2, y - mapFOV / 2, x + mapFOV / 2, y + mapFOV / 2
        for room in self.rooms:
            if min(room.Xf, Xf) >= max(room.Xi, Xi) and min(room.Yf, Yf) >= max(room.Yi, Yi):
                room.draw(win, x, y, mapFOV)
            if room.Xi <= x <= room.Xf and room.Yi <= y <= room.Yf:
                room.drawRoomName(win)
