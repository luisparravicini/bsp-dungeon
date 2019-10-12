#!/usr/bin/env python

"""Based on pygame's example 'starts'"""


import random
import math
import pygame
from time import time
from pygame.locals import *

# constants
WINSIZE = [320, 200]
SCREEN_SIZE = [WINSIZE[0]*2, WINSIZE[1]*2]
WINCENTER = [WINSIZE[0] / 2, WINSIZE[1] / 2]
CENTER_RADIUS = 25
NUMSTARS = 150


def print_fps(clock):
    print('FPS:', clock.get_fps())


def init_star():
    "creates new star values"
    dir = random.randrange(100000)
    velmult = random.random()*.6+.4
    vel = [math.sin(dir) * velmult, math.cos(dir) * velmult]
    pos = WINCENTER[:]

    return vel, pos


def initialize_stars():
    "creates a new starfield"
    stars = []
    for x in range(NUMSTARS):
        star = init_star()
        vel, pos = star
        steps = random.randint(0, WINCENTER[0])
        pos[0] = pos[0] + (vel[0] * steps)
        pos[1] = pos[1] + (vel[1] * steps)
        vel[0] = vel[0] * (steps * .09)
        vel[1] = vel[1] * (steps * .09)
        stars.append(star)
    move_stars(stars)
    return stars


def draw_stars(surface, stars, color):
    "used to draw (and clear) the stars"
    for vel, pos in stars:
        pos = (int(pos[0]), int(pos[1]))
        pygame.draw.line(surface, color, WINCENTER, pos)
        # surface.set_at(pos, color)


def move_stars(stars):
    "animate the star values"
    for vel, pos in stars:
        pos[0] = pos[0] + vel[0]
        pos[1] = pos[1] + vel[1]
        if not 0 <= pos[0] <= WINSIZE[0] or not 0 <= pos[1] <= WINSIZE[1]:
            vel[:], pos[:] = init_star()
        else:
            vel[0] = vel[0] * 1.05
            vel[1] = vel[1] * 1.05


def main():
    # create our starfield
    random.seed()
    stars = initialize_stars()
    clock = pygame.time.Clock()
    # initialize and prepare screen
    pygame.init()
    pygame.key.set_repeat(20)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    buffer = pygame.Surface(WINSIZE)
    pygame.display.set_caption('Stars')
    white = 255, 240, 200
    black = 20, 20, 40
    screen.fill(black)
    speed = 1
    speed_up = speed_down = False

    # main game loop
    done = 0
    frames = 0
    while not done:
        if frames % speed == 0:
            draw_stars(buffer, stars, black)
        move_stars(stars)
        draw_stars(buffer, stars, white)

        pygame.transform.scale2x(buffer, screen)
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == KEYUP and e.key == K_f:
                print_fps(clock)

            if e.type == KEYDOWN and e.key == K_UP:
                speed_up = True
            elif e.type == KEYDOWN and e.key == K_DOWN:
                speed_down = True

            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = 1
                break
            elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                WINCENTER[:] = list(e.pos)

        if speed_up:
            speed += 4
            speed_up = False
        else:
            ds = 2
            if speed_down:
                ds *= 2
            speed = max(speed - ds, 1)

        clock.tick(50)
        frames += 1

    print_fps(clock)


# if python says run, then we should run
if __name__ == '__main__':
    main()
