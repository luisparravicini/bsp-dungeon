
class LevelGenerator:

    def __init__(self, level):
        self.level = level
        pass

    def create(self, first_room_pos):
        room = self.level.room_at(first_room_pos).room

        self._put_roomtje(room, (2, 2), (5, 8))

    def _put_roomtje(self, room, pos, size):
        wall_tile = (0, 13)

        for dx in range(size[0]):
            room.set_tile((pos[0] + dx, pos[1]), wall_tile)
            room.set_tile((pos[0] + dx, pos[1] + size[1] - 1), wall_tile)

        for dy in range(size[1]):
            room.set_tile((pos[0], pos[1] + dy), wall_tile)
            room.set_tile((pos[0] + size[0] - 1, pos[1] + dy), wall_tile)
