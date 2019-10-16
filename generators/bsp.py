import random
import pygame


class TreeNode:
    def __init__(self, rect):
        self.rect = rect
        self.children = None


class BSPGenerator:
    def __init__(self, level):
        self.level = level
        self.iterations = 4
        self.nodes = None
        self.max_room = (8, 8)

    def create(self, center_pos):
        size = self.level.size
        node = TreeNode(pygame.Rect(0, 0, size[0], size[1]))

        iterations_left = 4
        self.split(node, iterations_left)

        self.text_dump(node)
        self.nodes = node

        self.make_level()

    def make_level(self):
        wall_tile = (0, 13)

        for x in range(self.level.size[0]):
            for y in range(self.level.size[0]):
                self.level.set_tile((x, y), wall_tile)

    def split(self, node, iterations_left):
        rect = node.rect
        split_vert = random.random() > 0.5
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
            self.split(childA, iterations_left - 1)
            self.split(childB, iterations_left - 1)

    def text_dump(self, node, level=0):
        print(" " * level * 4, node.rect)
        if node.children is not None:
            self.text_dump(node.children[0], level + 1)
            self.text_dump(node.children[1], level + 1)

