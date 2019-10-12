#!/usr/bin/env python

"""Based on pygame's example 'starts'"""


import random
import math
import pygame
from time import time
from pygame.locals import *
import spritesheet

# constants
WINSIZE = [320, 200]
SCREEN_SIZE = [WINSIZE[0]*2, WINSIZE[1]*2]
WINCENTER = [WINSIZE[0] / 2, WINSIZE[1] / 2]
CENTER_RADIUS = 25
NUMSTARS = 150


sheet = None
black = Color('black')
tile_size = 16


def tile_at(pos):
    global sheet, black, tile_size

    cell_size = 17
    rect = (pos[0] * cell_size, pos[1] * cell_size, tile_size, tile_size)
    return sheet.image_at(rect, colorkey=black)


def main():
    global sheet, black, tile_size

    random.seed()
    # initialize and prepare screen
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    buffer = pygame.Surface(WINSIZE)
    pygame.display.set_caption('..--..')
    background_color = (60, 30, 60)

    sheet = spritesheet.spritesheet('tiles.png')

    done = 0
    while not done:
        buffer.fill(background_color)
        for y in range(12):
            for x in range(20):
                image = tile_at((x, y))
                buffer.blit(image, (x*tile_size, y*tile_size))
        pygame.transform.scale2x(buffer, screen)
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = 1
                break

if __name__ == '__main__':
    main()
