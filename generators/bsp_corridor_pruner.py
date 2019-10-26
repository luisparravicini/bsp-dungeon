import math


class CorridorPruner:
    def __init__(self, generator):
        self.generator = generator

    def prune(self):
        return

        # new_corridors = list()
        # for corridor in self.generator.corridors:
        #     segments = self.segmentize_corridor(corridor)
        #     if segments is None:
        #         new_corridors.append(corridor)
        #     else:
        #         new_corridors.extend(segments)
        # self.generator.corridors = new_corridors

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

    def check_dead_ends(self):
        dead_ends = set()
        for corridor in self.generator.corridors:
            for pos in self._corridor_ends(corridor):
                r = self._find_room_with(pos)
                if r is None:
                    connected = self._has_corridor_at(corridor, pos)
                    if not connected:
                        dead_ends.add(pos)

        if len(dead_ends) > 0:
            print(f'dead ends: {dead_ends}')
        return dead_ends

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

    def segmentize_corridor(self, corridor):
        segments = list()

        start_pos = [corridor[0], corridor[1]]
        end_pos = [corridor[2], corridor[3]]

        delta = [0, 0]
        for i in range(0, 2):
            if end_pos[i] != start_pos[i]:
                delta[i] = int(math.copysign(1, end_pos[i] - start_pos[i]))

        room = self._find_room_with(start_pos)
        start_inside_room = inside_room = (room is not None)

        pos = list(start_pos)
        last_pos = list(pos)
        while True:
            last_pos[0] = pos[0]
            last_pos[1] = pos[1]
            pos[0] += delta[0]
            pos[1] += delta[1]

            room = self._find_room_with(pos)
            new_inside_room = (room is not None)

            if new_inside_room ^ inside_room:
                if not inside_room:
                    segments.append(start_pos + pos)
                else:
                    start_pos = list(pos)

                inside_room = new_inside_room

            if pos == end_pos:
                break

        if len(segments) == 0:
            return None
        else:
            return segments

    def adjust_corridor_border(self, start_pos, end_pos):
        room = self._find_room_with(start_pos)
        if room is None:
            # print("no room for", start_pos)
            return
        # assert(room is not None)

        delta = [0, 0]
        for i in range(0, 2):
            if end_pos[i] != start_pos[i]:
                delta[i] = int(math.copysign(1, end_pos[i] - start_pos[i]))

        pos = list(start_pos)
        last_pos = list(pos)
        while room.collidepoint(pos) and pos != end_pos:
            last_pos[0] = pos[0]
            last_pos[1] = pos[1]
            pos[0] += delta[0]
            pos[1] += delta[1]

        return last_pos

    def _find_room_with(self, pos):
        for r in self.generator._rooms_dict.values():
            if r.collidepoint(pos):
                return r
        return None
