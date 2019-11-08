#!/usr/bin/env python3

import conf
from level import Level
from level_generator import LevelGenerator
import pygame
from pygame.locals import *
import datetime
from generators import DungeonValidator


floor_color = (60, 60, 60)
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


def draw_selected_pos(pos, surface, scale):
    if pos is not None:
        color = (240, 154, 0, 128)
        pygame.draw.rect(surface, color,
            (pos[0] * scale, pos[1] * scale, scale, scale),
            width=0)


def draw_corridors(level, corridors, surface, scale):
    color = (95, 128, 142)
    for corridor in corridors:
        if corridor[0] == corridor[2]:
            deltas = (0.5, 0)
        else:
            deltas = (0, 0.5)
        pygame.draw.line(surface, color, (
            (corridor[0] + deltas[0]) * scale, (corridor[1] + deltas[1]) * scale),
            ((corridor[2]  + deltas[0]) * scale, (corridor[3] + deltas[1]) * scale),
            width=1)

def draw_errors(errors, surface, scale, color):
    r = 1.5

    for dead_end in errors:
        pygame.draw.circle(surface, color, (
            (dead_end[0] + 0.5) * scale, (dead_end[1] + 0.5) * scale),
            r * scale,
            width=2)


def dump_stats(start_time, n):
    end_time = datetime.datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    elapsed_one_ms = elapsed * 1000 / n
    print(f'created {n} dungeons in {elapsed:.0f}s ({elapsed_one_ms:.2f}ms per dungeon)')


def generate(level_generator):
    level_generator.create()
    return validator.validates()


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

valid = generate(level_generator)

done = False
needs_draw = True
auto_create = False
n = 0
selected_level_pos = last_level_pos = None
while not done:
    clock.tick(60)

    if needs_draw or auto_create:
        needs_draw = False

        if auto_create:
            n += 1
            valid = generate(level_generator)

        if not valid:
            auto_create = False
            print("dungeon doesn't validates!")

        if n % 25 == 0 or not valid or needs_draw:
            screen.fill(Color('black'))
            draw_node(level_generator.generator.nodes, screen, scale)
            draw_level(level, level_generator.generator.carver, screen, scale)
            draw_corridors(level, level_generator.generator.corridors, screen, scale)
            draw_errors(validator.dead_ends, screen, scale, (176, 0, 32))
            draw_errors(validator.unconstrained_floor, screen, scale, (98, 0, 238))
            draw_selected_pos(selected_level_pos, screen, scale)

    pygame.display.update()

    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
            done = 1
            break

        if e.type == KEYUP and e.key == K_s:
            print('saving level to', LEVEL_FNAME)
            level_generator.generator.save(LEVEL_FNAME)

        if e.type == KEYUP and e.key == K_l:
            print('loading level from', LEVEL_FNAME)
            level_generator.generator.load(LEVEL_FNAME)
            needs_draw = True

        if e.type == KEYUP and e.key == K_g:
            valid = generate(level_generator)
            needs_draw = True

        if e.type == KEYUP and e.key == K_a:
            auto_create = not auto_create
            if auto_create:
                n = 0
                start_time = datetime.datetime.now()
            else:
                needs_draw = True
                dump_stats(start_time, n)

        if e.type == MOUSEMOTION:
            selected_level_pos = (e.pos[0] // scale, e.pos[1] // scale)
            if (last_level_pos != selected_level_pos):
                last_level_pos = tuple(selected_level_pos)
                print('level pos:', selected_level_pos)
                needs_draw = True

if auto_create:
    dump_stats(start_time, n)
