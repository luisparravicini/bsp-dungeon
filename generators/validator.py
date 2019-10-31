from .bsp_corridor_pruner import CorridorPruner


class DungeonValidator:
    def __init__(self, generator):
        self.generator = generator
        self.errors = set()

    def validates(self):
        self.errors.clear()
        valid = self._check_dead_ends()
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

        self.errors.update(dead_ends)

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
