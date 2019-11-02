from .bsp_corridor_pruner import CorridorPruner


class DungeonValidator:
    def __init__(self, generator):
        self.generator = generator

    def validates(self):
        self.dead_ends = set()
        self.unconstrained_floor = set()

        valid = self._check_dead_ends()
        if not self._check_reachability():
            valid = False

        return valid

    def _check_reachability(self):
        valid = True
        all_floor_tiles = set()
        level = self.generator.level

        for x in range(level.size[0]):
            for y in range(level.size[1]):
                pos = (x, y)
                tile = level.tile_at(pos)
                if tile == self.generator.carver.empty_tile:
                    all_floor_tiles.add(pos)

        visited = set()
        to_visit = set(all_floor_tiles)
        while len(to_visit) > 0:
            pos = to_visit.pop()
            visited.add(pos)

            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    neighbour = (pos[0] + dx, pos[1] + dy)
                    tile = level.tile_at(neighbour)
                    if tile == self.generator.carver.empty_tile:
                        if neighbour not in visited:
                            to_visit.add(neighbour)
                    elif tile == self.generator.carver.no_tile:
                        self.unconstrained_floor.add(pos)
                        valid = False

        return valid

    def _check_dead_ends(self):
        dead_ends = set()
        for corridor in self.generator.corridors:
            for pos in self._corridor_ends(corridor):
                r = CorridorPruner.find_room_with(pos, self.generator._rooms_dict)
                if r is None:
                    connected = self._has_corridor_at(corridor, pos)
                    if not connected:
                        dead_ends.add(pos)

        valid = (len(dead_ends) == 0)
        if not valid:
            print(f'dead ends: {dead_ends}')

        self.dead_ends = dead_ends

        return valid

    def _has_corridor_at(self, this_corridor, pos):
        found = False

        for corridor in self.generator.corridors:
            if corridor == this_corridor:
                continue

            for corridor_pos in self._corridor_ends(corridor):
                if corridor_pos == pos:
                    found = True

            if found:
                break

        return found

    def _corridor_ends(self, corridor):
        return ((corridor[0], corridor[1]), (corridor[2], corridor[3]))
