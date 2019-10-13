#!/usr/bin/env python3

import random
import pygame
from pygame.locals import *
from sprite_sheet_manager import SpritesheetManager
from room import Room, RoomView
from level import Level
from player import Player, PlayerView
import conf


class Game:

    def setup(self):
        random.seed()

        pygame.init()
        self.screen = pygame.display.set_mode(conf.SCREEN_SIZE)
        self.bkg_surface = pygame.Surface(conf.SCREEN_SIZE)
        pygame.display.set_caption('..--..')
        self.sheet = SpritesheetManager('tiles.png')
        self.clock = pygame.time.Clock()

    def main(self):
        background_color = (40, 10, 40)

        self.level = Level((4, 4), self.bkg_surface, self.sheet, background_color)
        self.player = Player((5, 5))
        player_view = PlayerView(self.sheet, self.player, self.screen)
        fps_font = pygame.font.Font(None, 42)

        self.change_room_to((1, 1))

        done = 0
        show_fps = False
        while not done:
            self.clock.tick(60)

            self.screen.fill(background_color)

            room_view = self.level.room_at(self.cur_room)
            room_view.update(self.room_dirty)
            self.room_dirty = False
            self.screen.blit(self.bkg_surface, (0, 0))

            player_view.update()

            if show_fps:
                fps = fps_font.render(
                        str(int(self.clock.get_fps())),
                        False,
                        Color('white'),
                        Color('black')
                    )
                self.screen.blit(fps, (10, 10))

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

                if e.type == KEYDOWN and e.key == K_f:
                    show_fps = not show_fps
                if e.type == KEYDOWN and e.key == K_g:
                    tile_id = room_view.room.tile_at(self.player.pos)
                    print('tile at player', tile_id)

    def change_room_to(self, pos):
        self.cur_room = list(pos)
        self.room_dirty = True
        print('changed room', self.cur_room)

    def change_room(self, deltas):
        new_pos = (self.cur_room[0] + deltas[0], self.cur_room[1] + deltas[1])
        self.change_room_to(new_pos)

    def move_up(self):
        delta = (0, -1)
        pos_index = 1
        new_room_pos = (self.player.pos[0], conf.ROOM_SIZE[1] - 1)
        self.move_dec(delta, pos_index, new_room_pos)

    def move_left(self):
        delta = (-1, 0)
        pos_index = 0
        new_room_pos = (conf.ROOM_SIZE[0] - 1, self.player.pos[1])
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
        if self.player.pos[pos_index] < conf.ROOM_SIZE[pos_index] - 1:
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
