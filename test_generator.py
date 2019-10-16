#!/usr/bin/env python3

import conf
from level import Level
from level_generator import LevelGenerator
import pygame
from pygame.locals import *


def draw_node(node, surface, scale):
    color = Color('white')

    if node.children is None:
        rect = node.rect
        pygame.draw.rect(surface, color, (
            rect.x * scale,
            rect.y * scale,
            rect.width * scale,
            rect.height * scale)
        , width=1)

    if node.children is not None:
        draw_node(node.children[0], surface, scale)
        draw_node(node.children[1], surface, scale)


level = Level((80, 80), None, None, None)
level_generator = LevelGenerator(level)

viewport_pos = (
    int(level.size[0] / 2 - conf.ROOM_SIZE[0] / 2),
    int(level.size[1] / 2 - conf.ROOM_SIZE[1] / 2),
)
level_generator.create(viewport_pos)

pygame.init()
screen = pygame.display.set_mode(conf.SCREEN_SIZE)
clock = pygame.time.Clock()

scale = 7

done = False
needs_gen = True
while not done:
    clock.tick(60)

    if needs_gen:
        needs_gen = False
        level_generator.create(viewport_pos)
        screen.fill(Color('black'))
        draw_node(level_generator.generator.nodes, screen, scale)

    pygame.display.update()

    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
            done = 1
            break
        if e.type == KEYUP and e.key == K_g:
            needs_gen = True