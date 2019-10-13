#!/usr/bin/env python3

import random
import pygame
from pygame.locals import *
import spritesheet

WIN_SIZE = [320, 200]
SCALE = 3
TILE_SIZE = 16 * SCALE
SCREEN_SIZE = [WIN_SIZE[0] * SCALE, WIN_SIZE[1] * SCALE]
ROOM_SIZE = [int(v / TILE_SIZE) for v in SCREEN_SIZE]


class Room:
    def __init__(self):
        pass

    def update(self):
        pass


class Level:
    def __init__(self, size):
        self.size = size
        self.rooms = tuple(Room() for x in range(size[0] * size[1]))

    def room_at(self, pos):
        index = pos[0] + pos[1] * self.size[1]
        return self.rooms[index]


class Player:
    def __init__(self, room_pos):
        self.pos = list(room_pos)

    def move(self, delta):
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]

    def move_to(self, pos):
        self.pos = list(pos)


class PlayerView:
    def __init__(self, spritesheet, player, surface):
        self.player = player
        self.sprite = spritesheet.tile_at((18, 7))
        self.surface = surface
        self.looking_left = False

    def update(self):
        self._blit(self.surface)

    def _blit(self, surface):
        global TILE_SIZE

        surface_pos = tuple(v * TILE_SIZE for v in self.player.pos)
        sprite = pygame.transform.flip(self.sprite, self.looking_left, False)
        surface.blit(sprite, surface_pos)


class SpritesheetManager:
    def __init__(self, path):
        global SCALE

        self.sheet = spritesheet.spritesheet('tiles-color.png')
        size = tuple(v * SCALE for v in self.sheet.sheet.get_size())
        self.sheet.sheet = pygame.transform.scale(self.sheet.sheet, size)

    def tile_at(self, pos):
        global TILE_SIZE

        cell_size = TILE_SIZE + 1 * SCALE
        rect = tuple(v * cell_size for v in pos) + (TILE_SIZE,) * 2
        # colorkey = Color('black')
        colorkey = (71, 45, 60)
        return self.sheet.image_at(rect, colorkey=colorkey)


class Game:

    def setup(self):
        random.seed()

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('..--..')
        self.sheet = SpritesheetManager('tiles.png')

    def main(self):
        global TILE_SIZE

        background_color = (40, 10, 40)

        self.level = Level((4, 4))
        self.player = Player((5, 5))
        player_view = PlayerView(self.sheet, self.player, self.screen)

        self.change_room_to((1, 1))

        done = 0
        while not done:
            self.screen.fill(background_color)

            room = self.level.room_at(self.cur_room)
            room.update()

            player_view.update()

            pygame.display.update()

            for e in pygame.event.get():
                if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                    done = 1
                    break

                if e.type == KEYDOWN and e.key == K_RIGHT:
                    self.move_right()
                    player_view.looking_left = False
                if e.type == KEYDOWN and e.key == K_LEFT:
                    self.move_left()
                    player_view.looking_left = True
                if e.type == KEYDOWN and e.key == K_UP:
                    self.move_up()
                if e.type == KEYDOWN and e.key == K_DOWN:
                    self.move_down()

    def change_room_to(self, pos):
        self.cur_room = list(pos)
        print('changed room', self.cur_room)

    def change_room(self, deltas):
        new_pos = (self.cur_room[0] + deltas[0], self.cur_room[1] + deltas[1])
        self.change_room_to(new_pos)

    def move_up(self):
        delta = (0, -1)
        pos_index = 1
        new_room_pos = (self.player.pos[0], ROOM_SIZE[1] - 1)
        self.move_dec(delta, pos_index, new_room_pos)

    def move_left(self):
        delta = (-1, 0)
        pos_index = 0
        new_room_pos = (ROOM_SIZE[0] - 1, self.player.pos[1])
        self.move_dec(delta, pos_index, new_room_pos)


    def move_down(self):
        delta = (0, 1)
        pos_index = 1
        new_room_pos = (self.player.pos[0], 0)
        self.move_inc(delta, pos_index, new_room_pos)

    def move_right(self):
        delta = (1, 0)
        pos_index = 0
        new_room_pos = (0, self.player.pos[1])
        self.move_inc(delta, pos_index, new_room_pos)

    def move_inc(self, delta, pos_index, new_room_pos):
        if self.player.pos[pos_index] < ROOM_SIZE[pos_index] - 1:
            self.player.move(delta)
            return

        if self.cur_room[pos_index] < self.level.size[pos_index] - 1:
            self.player.move_to(new_room_pos)
            self.change_room(delta)

    def move_dec(self, delta, pos_index, new_room_pos):
        if self.player.pos[pos_index] > 0:
            self.player.move(delta)
            return

        if self.cur_room[pos_index] > 0:
            self.player.move_to(new_room_pos)
            self.change_room(delta)


if __name__ == '__main__':
    game = Game()
    game.setup()
    game.main()
