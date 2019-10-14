
class LevelGenerator:

    def __init__(self, level):
        self.level = level
        pass

    def create(self, center_pos):
        self._put_room((center_pos[0] + 8, center_pos[1] + 2), (5, 8))

    def _put_room(self, pos, size):
        wall_tile = (0, 13)
        door_closed_tile = (3, 9)

        for dx in range(size[0]):
            self.level.set_tile((pos[0] + dx, pos[1]), wall_tile)
            self.level.set_tile((pos[0] + dx, pos[1] + size[1] - 1), wall_tile)

        for dy in range(size[1]):
            self.level.set_tile((pos[0], pos[1] + dy), wall_tile)
            if dy != size[1] - 2:
                tile = wall_tile
            else:
                tile = door_closed_tile
            self.level.set_tile((pos[0] + size[0] - 1, pos[1] + dy), tile)
