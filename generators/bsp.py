import random
import pygame
from .bsp_carver import Carver
from .bsp_exporter import Exporter
from .bsp_corridor_pruner import CorridorPruner
from .bsp_corridors_manager import CorridorsManager


class TreeNode:
    def __init__(self, rect):
        self.rect = rect
        self.children = ()

    def has_children(self):
        return len(self.children) > 0


class BSPGenerator:
    def __init__(self, level, no_tile_pos):
        self.level = level
        self.iterations = 5
        self.min_room = (5, 5)
        self.carver = Carver(self, no_tile_pos)
        self.exporter = Exporter(self)
        self.corridor_pruner = CorridorPruner(self)
        self.corridor_manager = CorridorsManager(self)

    def create(self, center_pos):
        self.nodes = list()
        self._rooms_dict = dict()
        self.corridors = list()

        self.do_split()
        self.put_rooms()
        self.corridor_manager.connect_rooms(self.nodes)
        self.corridor_pruner.prune()

        self.carver.make_level()

        self.rooms = list(self._rooms_dict.values())

    def save(self, path):
        self.exporter.save(path)

    def load(self, path):
        self.exporter.load(path)

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

        self._rooms_dict[node] = room

    def do_split(self):
        size = self.level.size
        node = TreeNode(pygame.Rect(0, 0, size[0], size[1]))
        iterations_left = 5
        split_vert = random.random() > 0.5
        self.split(node, iterations_left, split_vert)
        self.nodes = node

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
