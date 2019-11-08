
class Carver:

    def __init__(self, generator, no_tile_pos):
        self.generator = generator
        self.wall_tile = (0, 13)
        self.empty_tile = (0, 0)
        self.no_tile = no_tile_pos

    def make_level(self):
        for x in range(self.generator.level.size[0]):
            for y in range(self.generator.level.size[0]):
                self.generator.level.set_tile((x, y), self.no_tile)

        for room in self.generator.rooms:
            self.carve_room(room)

        for corridor in self.generator.corridors:
            self.carve_corridor(corridor)

        self.carve_walls()

    def carve_walls(self):
        level = self.generator.level

        for x in range(level.size[0]):
            for y in range(level.size[0]):
                tile = level.tile_at((x, y))
                if tile == self.empty_tile:
                    self._set_walls_on_neighbours(x, y)

    def _set_walls_on_neighbours(self, x, y):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                self.set_tile_if_not_empty((x + dx, y + dy))

    def set_tile(self, pos, tile):
        level = self.generator.level

        if pos[0] < 0 or pos[0] >= level.size[0]:
            return
        if pos[1] < 0 or pos[1] >= level.size[1]:
            return

        level.set_tile(pos, tile)

    def set_tile_if_not_empty(self, pos):
        tile = self.generator.level.tile_at(pos)
        if tile != self.empty_tile:
            self.set_tile(pos, self.wall_tile)

    def carve_room(self, room):
        for x in range(room.x, room.right):
            for y in range(room.y, room.bottom):
                if x != room.x and x != room.right - 1:
                    if y != room.y and y != room.bottom - 1:
                        tile = self.empty_tile
                        self.set_tile((x, y), tile)

    def carve_corridor(self, corridor):
        vert_line = (corridor[0] == corridor[2])
        if vert_line:
            x = corridor[0]
            for y in range(corridor[1], corridor[3] + 1):
                self.set_tile((x, y), self.empty_tile)
        else:
            y = corridor[1]
            for x in range(corridor[0], corridor[2] + 1):
                self.set_tile((x, y), self.empty_tile)
