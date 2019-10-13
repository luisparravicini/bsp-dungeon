import conf


class Room:
    def __init__(self):
        self.tiles = list(None for _ in range(conf.ROOM_SIZE[0] * conf.ROOM_SIZE[1]))

        import random
        self.tiles = list((random.randint(0, 31), random.randint(0, 31)) for x in self.tiles)

    def update(self):
        pass

    def tile_at(self, pos):
        return self.tiles[pos[0] + pos[1] * conf.ROOM_SIZE[1]]


class RoomView:
    def __init__(self, surface, sheet, background_color):
        self.room = Room()
        self.surface = surface
        self.sheet = sheet
        self.background_color = background_color

    def update(self, needs_redraw):
        self.room.update()
        if needs_redraw:
            self._blit()

    def _blit(self):
        self.surface.fill(self.background_color)

        surface_pos = [0, 0]
        for y in range(conf.ROOM_SIZE[1]):
            for x in range(conf.ROOM_SIZE[0]):
                tile_pos = self.room.tile_at((x, y))
                if tile_pos is None:
                    continue

                surface_pos[0] = x * conf.TILE_SIZE
                surface_pos[1] = y * conf.TILE_SIZE
                self.sheet.blit_tile_at(self.surface, surface_pos, tile_pos)
