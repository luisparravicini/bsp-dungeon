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


class Player:
    def __init__(self, room_pos):
        self.room_pos = room_pos

    def move(self, delta):
        self.room_pos[0] += delta[0]
        self.room_pos[1] += delta[1]


class PlayerView:
    def __init__(self, sheet, player, surface):
        self.player = player
        self.sprite = tile_at((18, 7))
        self.surface = surface

    def update(self):
        self._blit(self.surface)

    def _blit(self, surface):
        global tile_size

        surface_pos = (
            self.player.room_pos[0] * tile_size,
            self.player.room_pos[1] * tile_size
        )
        surface.blit(self.sprite, surface_pos)


def tile_at(pos):
    global sheet, black, tile_size

    cell_size = 17
    rect = (pos[0] * cell_size, pos[1] * cell_size, tile_size, tile_size)
    return sheet.image_at(rect, colorkey=black)


def main():
    global sheet, black, tile_size

    random.seed()

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    buffer = pygame.Surface(WINSIZE)
    pygame.display.set_caption('..--..')
    background_color = (40, 10, 40)

    sheet = spritesheet.spritesheet('tiles.png')
    player = Player([5, 5])
    player_view = PlayerView(sheet, player, buffer)

    done = 0
    while not done:
        buffer.fill(background_color)
        # for y in range(12):
        #     for x in range(20):
        #         image = tile_at((x, y))
        #         buffer.blit(image, (x*tile_size, y*tile_size))

        player_view.update()

        pygame.transform.scale2x(buffer, screen)
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = 1
                break

            if e.type == KEYDOWN and e.key == K_RIGHT:
                player.move((1, 0))
            if e.type == KEYDOWN and e.key == K_LEFT:
                player.move((-1, 0))
            if e.type == KEYDOWN and e.key == K_UP:
                player.move((0, -1))
            if e.type == KEYDOWN and e.key == K_DOWN:
                player.move((0, 1))


if __name__ == '__main__':
    main()
