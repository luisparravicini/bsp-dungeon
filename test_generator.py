#!/usr/bin/env python3

import conf
from level import Level
from level_generator import LevelGenerator
import pygame
from pygame.locals import *


def draw_node(node, surface, scale):
    color = (100, 100, 100)

    for child in node.children:
        draw_node(child, surface, scale)

    rect = node.rect
    pygame.draw.rect(surface, color, (
        rect.x * scale,
        rect.y * scale,
        rect.width * scale,
        rect.height * scale)
    , width=1)


def draw_rooms(rooms, surface, scale):
    color = (99, 148, 30)

    for room in rooms:
        pygame.draw.rect(surface, color, (
            room.x * scale,
            room.y * scale,
            room.width * scale,
            room.height * scale)
        , width=0)


def draw_corridors(corridors, surface, scale):
    color = Color('green')

    for corridor in corridors:
        pygame.draw.line(surface, color, (
            corridor[0] * scale,
            corridor[1] * scale),
            (corridor[2] * scale,
            corridor[3] * scale)
        , width=1)


level = Level((80, 80), None, None, None)
level_generator = LevelGenerator(level)

viewport_pos = (
    int(level.size[0] / 2 - conf.ROOM_SIZE[0] / 2),
    int(level.size[1] / 2 - conf.ROOM_SIZE[1] / 2),
)

pygame.init()
scale = 7
screen_size = (
    level.size[0] * scale,
    level.size[1] * scale
)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

LEVEL_FNAME = 'level.json'

level_generator.create(viewport_pos)

done = False
needs_draw = True
n = 0
auto_create = False
while not done:
    clock.tick(60)

    if needs_draw or auto_create:
        needs_draw = False
        screen.fill(Color('black'))
        if auto_create:
            n += 1
            level_generator.create(viewport_pos)
        draw_node(level_generator.generator.nodes, screen, scale)
        draw_rooms(level_generator.generator.rooms, screen, scale)
        draw_corridors(level_generator.generator.corridors, screen, scale)

    pygame.display.update()

    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
            done = 1
            break

        if e.type == KEYUP and e.key == K_s:
            level_generator.generator.save(LEVEL_FNAME)

        if e.type == KEYUP and e.key == K_l:
            level_generator.generator.load(LEVEL_FNAME)
            needs_draw = True

        if e.type == KEYUP and e.key == K_g:
            n += 1
            level_generator.create(viewport_pos)
            needs_draw = True

        if e.type == KEYUP and e.key == K_a:
            auto_create = not auto_create

print('created', n, 'dungeons')
