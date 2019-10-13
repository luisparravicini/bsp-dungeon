from room import RoomView


class Level:
    def __init__(self, size, surface, sheet, background_color):
        self.size = size
        self.rooms = tuple(RoomView(surface, sheet, background_color) for x in range(size[0] * size[1]))

    def room_at(self, pos):
        index = pos[0] + pos[1] * self.size[1]
        return self.rooms[index]
