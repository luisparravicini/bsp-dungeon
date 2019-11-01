
class Carver:

    def __init__(self, generator):
        self.generator = generator
        self.wall_tile = (0, 13)
        self.empty_tile = (0, 0)
        self.no_tile = (5, 5)

    def make_level(self):

        for x in range(self.generator.level.size[0]):
            for y in range(self.generator.level.size[0]):
                self.generator.level.set_tile((x, y), self.no_tile)

        for room in self.generator._rooms_dict.values():
            self.carve_room(room)

        for corridor in self.generator.corridors:
            self.carve_corridor(corridor)

    def set_tile(self, pos, tile):
        level = self.generator.level

        if pos[0] < 0 or pos[0] >= level.size[0]:
            return
        if pos[1] < 0 or pos[1] >= level.size[1]:
            return

        level.set_tile(pos, tile)

    def carve_room(self, room):
        for x in range(room.x, room.right):
            for y in range(room.y, room.bottom):
                if x == room.x or x == room.right - 1:
                    tile = self.wall_tile
                else:
                    if y == room.y or y == room.bottom - 1:
                        tile = self.wall_tile
                    else:
                        tile = self.empty_tile

                self.set_tile((x, y), tile)

    def carve_corridor(self, corridor):
        vert_line = (corridor[0] == corridor[2])
        if vert_line:
            x = corridor[0]
            for y in range(corridor[1], corridor[3] + 1):
                self.set_tile((x - 1, y), self.wall_tile)
                self.set_tile((x + 1, y), self.wall_tile)
                self.set_tile((x, y), self.empty_tile)
        else:
            y = corridor[1]
            for x in range(corridor[0], corridor[2] + 1):
                self.set_tile((x, y - 1), self.wall_tile)
                self.set_tile((x, y + 1), self.wall_tile)
                self.set_tile((x, y), self.empty_tile)
