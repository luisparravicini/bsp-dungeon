import conf


class Level:
    def __init__(self, size, surface, sheet, background_color):
        self.size = size
        self.tiles = list(None for _ in range(size[0] * size[1]))
        self.surface = surface
        self.sheet = sheet
        self.background_color = background_color

    def update(self, viewport_pos):
        # if needs_redraw:
        self._blit(viewport_pos)

    def has_floor_at(self, pos):
        return self.tile_at(pos) == (0,0)

    def _blit(self, viewport_pos):
        self.surface.fill(self.background_color)

        surface_pos = [None, None]
        for y in range(conf.ROOM_SIZE[1]):
            for x in range(conf.ROOM_SIZE[0]):
                pos = (viewport_pos[0] + x, viewport_pos[1] + y)
                tile_pos = self.tile_at(pos)
                if tile_pos is None:
                    continue

                surface_pos[0] = x * conf.TILE_SIZE
                surface_pos[1] = y * conf.TILE_SIZE
                self.sheet.blit_tile_at(self.surface, surface_pos, tile_pos)

    def set_tile(self, pos, tile_pos):
        index = self._tile_index(pos)
        if index is not None:
            self.tiles[index] = tile_pos

    def tile_at(self, pos):
        index = self._tile_index(pos)
        if index is None:
            return None
        return self.tiles[index]

    def _tile_index(self, pos):
        if 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]:
            return pos[0] + pos[1] * self.size[1]
        else:
            return None
