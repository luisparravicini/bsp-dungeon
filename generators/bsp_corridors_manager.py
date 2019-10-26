import random


class CorridorsManager:
    def __init__(self, generator):
        self.generator = generator

    def connect_rooms(self, node=None):
        for child in node.children:
            self.connect_rooms(child)

        if node.has_children():
            self._connect_children(*node.children)

    def _choose_room(self, node):
        if not node.has_children():
            return self.generator._rooms_dict.get(node, None)

        rooms = list()
        for child in node.children:
            r = self._choose_room(child)
            if r is not None:
                rooms.append(r)

        if len(rooms) > 0:
            return random.choice(rooms)

        return None

    def _connect_children(self, a, b):
        room_a = self._choose_room(a)
        room_b = self._choose_room(b)

        if room_a is None or room_b is None:
            return

        options = list()
        corridor = self._gen_corridor_y(room_a, room_b)
        if corridor is not None:
            options.append(corridor)
        corridor = self._gen_corridor_x(room_a, room_b)
        if corridor is not None:
            options.append(corridor)
        if len(options) == 0:
            corridor = self._gen_corridor_xy(room_a, room_b)
            options.append(corridor)

        corridor = random.choice(options)
        self.generator.corridors.extend(corridor)

    def _gen_corridor_xy(self, room_a, room_b):
        x = random.randint(room_a.x, room_a.right - 1)
        min_y = min(room_a.centery, room_b.centery)
        max_y = max(room_a.centery, room_b.centery)

        corridor = list()
        corridor.append([x, min_y, x, max_y])
        corridor.append([x, max_y, room_b.centerx, max_y])
        return corridor

    def _gen_corridor_y(self, room_a, room_b):
        intersect = (
            max(room_a.y, room_b.y) + 1,
            min(room_a.bottom - 1, room_b.bottom - 1) - 1
        )
        if intersect[0] > intersect[1]:
            return None

        y = random.randint(intersect[0], intersect[1])

        corridor = [room_a.centerx, y, room_b.centerx, y]
        return [corridor]

    def _gen_corridor_x(self, room_a, room_b):
        intersect = (
            max(room_a.x, room_b.x) + 1,
            min(room_a.right - 1, room_b.right - 1) - 1
        )
        if intersect[0] > intersect[1]:
            return None

        x = random.randint(intersect[0], intersect[1])

        corridor = [x, room_a.centery, x, room_b.centery]
        return [corridor]