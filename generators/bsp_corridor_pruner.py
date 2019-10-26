import math

class CorridorPruner:
    def __init__(self, generator):
        self.generator = generator

    def prune(self):
        new_corridors = list()
        for corridor in self.generator.corridors:
            segments = self.segmentize_corridor(corridor)
            if segments is None:
                new_corridors.append(corridor)
            else:
                new_corridors.extend(segments)
        self.generator.corridors = new_corridors

        for corridor in self.generator.corridors:
            start_pos = (corridor[0], corridor[1])
            end_pos = (corridor[2], corridor[3])
            pos = self.adjust_corridor_border(start_pos, end_pos)
            if pos is not None:
                start_pos = pos
                corridor[0] = start_pos[0]
                corridor[1] = start_pos[1]

            end_pos = self.adjust_corridor_border(end_pos, start_pos)
            if end_pos is not None:
                corridor[2] = end_pos[0]
                corridor[3] = end_pos[1]

    def segmentize_corridor(self, corridor):
        return None

    def adjust_corridor_border(self, start_pos, end_pos):
        room = self._find_room_with(start_pos)
        if room is None:
            print("no room for", start_pos)
            return
        # assert(room is not None)

        delta = [0, 0]
        for i in range(0, 2):
            if end_pos[i] != start_pos[i]:
                delta[i] = int(math.copysign(1, end_pos[i] - start_pos[i]))

        pos = list(start_pos)
        last_point = list(pos)
        while room.collidepoint(pos) and pos != end_pos:
            last_point[0] = pos[0]
            last_point[1] = pos[1]
            pos[0] += delta[0]
            pos[1] += delta[1]

        return last_point

    def _find_room_with(self, pos):
        for r in self.generator._rooms_dict.values():
            if r.collidepoint(pos):
                return r
        return None
