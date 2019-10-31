#!/usr/bin/env python3

import conf
from level import Level
from level_generator import LevelGenerator
import pygame
from pygame.locals import *
import datetime
from generators import DungeonValidator


floor_color = (40, 40, 40)
wall_color = (100, 150, 30)


def draw_node(node, surface, scale):
    color = (100, 100, 100)

    for child in node.children:
        draw_node(child, surface, scale)

    rect = node.rect
    pygame.draw.rect(surface, color, (
        rect.x * scale, rect.y * scale,
        rect.width * scale, rect.height * scale),
        width=1)


def draw_level(level, carver, surface, scale):
    global wall_color, floor_color

    for x in range(level.size[0]):
        for y in range(level.size[1]):
            tile = level.tile_at((x, y))
            if tile == carver.wall_tile:
                pygame.draw.rect(surface, wall_color,
                    (x * scale, y * scale, scale, scale),
                    width=0)
            elif tile == carver.empty_tile:
                pygame.draw.rect(surface, floor_color,
                    (x * scale, y * scale, scale, scale),
                    width=0)


def draw_errors(dead_ends, surface, scale):
    color = Color('red')
    r = 1.5

    for dead_end in dead_ends:
        pygame.draw.circle(surface, color, (
            (dead_end[0] + 0.5) * scale, (dead_end[1] + 0.5) * scale),
            r * scale,
            width=1)


def dump_stats(start_time, n):
    end_time = datetime.datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    elapsed_one_ms = elapsed * 1000 / n
    print(f'created {n} dungeons in {elapsed:.0f}s ({elapsed_one_ms:.2f}ms per dungeon)')


scale = 7
size = (80, 80)
screen_size = (
    size[0] * scale,
    size[1] * scale
)

pygame.init()
screen = pygame.display.set_mode(screen_size)
level = Level(size, None, None, None)
level_generator = LevelGenerator(level)
validator = DungeonValidator(level_generator.generator)
clock = pygame.time.Clock()

LEVEL_FNAME = 'level.json'

viewport_pos = (0, 0)
level_generator.create(viewport_pos)

done = False
needs_draw = True
auto_create = False
while not done:
    clock.tick(60)

    if needs_draw or auto_create:
        needs_draw = False
        screen.fill(Color('black'))
        if auto_create:
            n += 1
            level_generator.create(viewport_pos)
            if not validator.validates():
                auto_create = False
                print("dungeon doesn't validates!")
        draw_node(level_generator.generator.nodes, screen, scale)
        draw_level(level, level_generator.generator.carver, screen, scale)
        draw_errors(validator.errors, screen, scale)

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
            level_generator.create(viewport_pos)
            needs_draw = True

        if e.type == KEYUP and e.key == K_a:
            auto_create = not auto_create
            if auto_create:
                n = 0
                start_time = datetime.datetime.now()
            else:
                dump_stats(start_time, n)

if auto_create:
    dump_stats(start_time, n)

