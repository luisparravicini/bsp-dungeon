import random
import pygame


class TreeNode:
    def __init__(self, rect):
        self.rect = rect
        self.children = ()

    def has_children(self):
        return len(self.children) > 0


class BSPGenerator:
    """
        Based on
        http://www.roguebasin.com/index.php?title=Basic_BSP_Dungeon_generation
    """
    def __init__(self, level):
        self.level = level
        self.iterations = 5
        self.min_room = (5, 5)

    def create(self, center_pos):
        self.nodes = list()
        self.rooms = dict()
        self.corridors = list()

        self.do_split()
        self.put_rooms()
        self.connect_rooms(self.nodes)
        self.prune_corridors()

        self.make_level()
        # self.text_dump()

    def prune_corridors(self):
        i = 0
        while i < len(self.corridors):
            i += 1

    def connect_rooms(self, node=None):
        for child in node.children:
            self.connect_rooms(child)

        if node.has_children():
            self.connect_children(*node.children)

    def choose_room(self, node):
        if not node.has_children():
            return self.rooms.get(node, None)

        rooms = list()
        for child in node.children:
            r = self.choose_room(child)
            if r is not None:
                rooms.append(r)

        if len(rooms) > 0:
            return random.choice(rooms)

        return None

    def connect_children(self, a, b):
        room_a = self.choose_room(a)
        room_b = self.choose_room(b)

        if room_a is None or room_b is None:
            return

        options = list()
        corridor = self.gen_corridor_y(room_a, room_b)
        if corridor is not None:
            options.append(corridor)
        corridor = self.gen_corridor_x(room_a, room_b)
        if corridor is not None:
            options.append(corridor)
        if len(options) == 0:
            corridor = self.gen_corridor_xy(room_a, room_b)
            options.append(corridor)

        corridor = random.choice(options)
        self.corridors.extend(corridor) 

    def gen_corridor_xy(self, room_a, room_b):
        x = random.randint(room_a.x, room_a.right)
        min_y = min(room_a.centery, room_b.centery)
        max_y = max(room_a.centery, room_b.centery)

        corridor = list()
        corridor.append((x, min_y, x, max_y))
        corridor.append((x, max_y, room_b.centerx, max_y))
        return corridor

    def gen_corridor_y(self, room_a, room_b):
        intersect = (
            max(room_a.y, room_b.y) + 1,
            min(room_a.bottom, room_b.bottom) - 1
        )
        if intersect[0] > intersect[1]:
            return None

        y = random.randint(intersect[0], intersect[1])

        corridor = (room_a.centerx, y, room_b.centerx, y)
        return [corridor]

    def gen_corridor_x(self, room_a, room_b):
        intersect = (
            max(room_a.x, room_b.x) + 1,
            min(room_a.right, room_b.right) - 1
        )
        if intersect[0] > intersect[1]:
            return None

        x = random.randint(intersect[0], intersect[1])

        corridor = (x, room_a.centery, x, room_b.centery)
        return [corridor]

    def put_rooms(self, node=None):
        if node is None:
            self.put_rooms(self.nodes)
            return

        for child in node.children:
            if child.has_children():
                self.put_rooms(child)
            else:
                self.put_room(child)

    def put_room(self, node):
        rect = node.rect
        border = 2
        if rect.width <= self.min_room[0] + border or rect.height <= self.min_room[1] + border:
            return

        room = node.rect.copy()
        room.width = random.randint(self.min_room[0], room.width - 2)
        room.height = random.randint(self.min_room[0], room.height - 2)
        room.x += random.randint(1, rect.width - room.width)
        room.y += random.randint(1, rect.height - room.height)

        self.rooms[node] = room

    def do_split(self):
        size = self.level.size
        node = TreeNode(pygame.Rect(0, 0, size[0], size[1]))
        iterations_left = 5
        split_vert = random.random() > 0.5
        self.split(node, iterations_left, split_vert)
        self.nodes = node

    def make_level(self):
        wall_tile = (0, 13)
        empty_tile = (0, 0)

        for x in range(self.level.size[0]):
            for y in range(self.level.size[0]):
                self.level.set_tile((x, y), empty_tile)

        for corridor in self.corridors:
            self.carve_corridor(corridor, wall_tile, empty_tile)

        for room in self.rooms.values():
            self.carve_room(room, wall_tile, empty_tile)

    def set_tile(self, pos, tile):
        if pos[0] < 0 or pos[0] >= self.level.size[0]:
            return
        if pos[1] < 0 or pos[1] >= self.level.size[1]:
            return

        self.level.set_tile(pos, tile)

    def carve_room(self, room, wall_tile, empty_tile):
        for x in range(room.x, room.right):
            for y in range(room.y, room.bottom):
                if x == room.x or x == room.right - 1:
                    tile = wall_tile
                else:
                    if y == room.y or y == room.bottom - 1:
                        tile = wall_tile
                    else:
                        tile = empty_tile

                self.set_tile((x, y), tile)

    def carve_corridor(self, corridor, wall_tile, empty_tile):
        vert_line = (corridor[0] == corridor[2])
        if vert_line:
            x = corridor[0]
            for y in range(corridor[1], corridor[3]):
                self.set_tile((x - 1, y), wall_tile)
                self.set_tile((x + 1, y), wall_tile)
                self.set_tile((x, y), empty_tile)
        else:
            y = corridor[0]
            for x in range(corridor[0], corridor[2]):
                self.set_tile((x, y - 1), wall_tile)
                self.set_tile((x, y + 1), wall_tile)
                self.set_tile((x, y), empty_tile)

    def split(self, node, iterations_left, split_vert):
        rect = node.rect
        max_min = (0.3, 0.7)
        v = random.uniform(max_min[0], max_min[1])
        if split_vert:
            # vert
            y = int(v * rect.height)
            rectA = pygame.Rect(rect.x, rect.y, rect.width, y)
            rectB = pygame.Rect(rect.x, rect.y + y, rect.width, rect.height - y)
        else:
            # horiz
            x = int(v * rect.width)
            rectA = pygame.Rect(rect.x, rect.y, x, rect.height)
            rectB = pygame.Rect(rect.x + x, rect.y, rect.width - x, rect.height)

        childA = TreeNode(rectA)
        childB = TreeNode(rectB)
        node.children = (childA, childB)

        if iterations_left > 1:
            self.split(childA, iterations_left - 1, not split_vert)
            self.split(childB, iterations_left - 1, not split_vert)

    def text_dump_node(self, node, level=0):
        print(" " * level * 4, node.rect)
        for child in node.children:
            self.text_dump_node(child, level + 1)

    def text_dump(self):
        print()
        print("divisions")
        self.text_dump_node(self.nodes, 0)

        print("\nrooms")
        for room in self.rooms:
            print(room)
