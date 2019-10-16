#!/usr/bin/env python3

import conf
from level import Level
from level_generator import LevelGenerator
import pygame
from pygame.locals import *


def draw_node(node, surface, scale):
    color = Color('white')

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
    color = Color('green')

    for room in rooms:
        pygame.draw.rect(surface, color, (
            room.x * scale,
            room.y * scale,
            room.width * scale,
            room.height * scale)
        , width=1)


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
n = 0
auto_create = False
while not done:
    clock.tick(60)

    if needs_gen or auto_create:
        needs_gen = False
        n += 1
        level_generator.create(viewport_pos)
        screen.fill(Color('black'))
        draw_node(level_generator.generator.nodes, screen, scale)
        draw_rooms(level_generator.generator.rooms, screen, scale)

    pygame.display.update()

    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
            done = 1
            break
        if e.type == KEYUP and e.key == K_g:
            needs_gen = True

        if e.type == KEYUP and e.key == K_a:
            auto_create = not auto_create

print('created', n, 'dungeons')
