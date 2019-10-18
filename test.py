#!/usr/bin/env python3

import random
import pygame
from pygame.locals import *
from sprite_sheet_manager import SpritesheetManager
from level import Level
from player import Player, PlayerView
from level_generator import LevelGenerator
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
        self.ghost_mode = True

    def main(self):
        background_color = (40, 10, 40)

        self.level = Level((80, 80), self.bkg_surface, self.sheet, background_color)
        self.viewport_pos = (
            int(self.level.size[0] / 2 - conf.ROOM_SIZE[0] / 2),
            int(self.level.size[1] / 2 - conf.ROOM_SIZE[1] / 2),
        )
        self.level_generator = LevelGenerator(self.level)

        center = tuple((int(v / 2) for v in self.level.size))
        self.player = Player(center)
        player_view = PlayerView(self.sheet, self.player, self.screen)

        self.fps_font = pygame.font.Font(None, 22)

        self.no_scroll_size = (14, 8)
        self.no_scroll_area = pygame.Rect(
            int((conf.ROOM_SIZE[0] - self.no_scroll_size[0]) / 2),
            int((conf.ROOM_SIZE[1] - self.no_scroll_size[1]) / 2),
            self.no_scroll_size[0],
            self.no_scroll_size[1],
        )
        self.no_scroll_screen_area = tuple(x * conf.TILE_SIZE for x in self.no_scroll_area)

        self.level_generator.create(self.viewport_pos)

        done = 0
        show_debug = False
        while not done:
            self.clock.tick(60)

            self.screen.fill(background_color)

            self.level.update(self.viewport_pos)
            self.screen.blit(self.bkg_surface, (0, 0))

            player_view.update(self.viewport_pos)

            if show_debug:
                self.show_debug_info()

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

                if e.type == KEYDOWN and e.key == K_d:
                    show_debug = not show_debug

    def show_debug_info(self):
        fps = int(self.clock.get_fps())
        msg = f'viewport:{self.viewport_pos} player:{self.player.pos} no_scroll_area:{self.no_scroll_area} fps:{fps}'
        msg_surface = self.fps_font.render(
                msg,
                False,
                Color('white'),
                Color('black')
            )
        self.screen.blit(msg_surface, (10, 10))

        pygame.draw.rect(
            self.screen,
            Color('white'),
            self.no_scroll_screen_area,
            width=1
        )

    def move_up(self):
        delta = (0, -1)
        pos_index = 1
        self.move(delta, pos_index)

    def move_left(self):
        delta = (-1, 0)
        pos_index = 0
        self.move(delta, pos_index)

    def move_down(self):
        delta = (0, 1)
        pos_index = 1
        self.move(delta, pos_index)

    def move_right(self):
        delta = (1, 0)
        pos_index = 0
        self.move(delta, pos_index)

    def move(self, delta, pos_index):
        pos_in_screen = (
            self.player.pos[0] - self.viewport_pos[0] + delta[0],
            self.player.pos[1] - self.viewport_pos[1] + delta[1],
        )
        new_player_pos = (
            self.player.pos[0] + delta[0],
            self.player.pos[1] + delta[1],
        )
        if self.no_scroll_area.collidepoint(pos_in_screen):
            if self.level.empty_at(new_player_pos):
                self.player.move(delta)
                return

        pos_in_level = [
            self.viewport_pos[0] + delta[0],
            self.viewport_pos[1] + delta[1],
        ]
        if delta[pos_index] > 0:
            pos_in_level[0] += conf.ROOM_SIZE[0]
            pos_in_level[1] += conf.ROOM_SIZE[1]

        if pos_in_level[pos_index] >= 0 and pos_in_level[pos_index] < self.level.size[pos_index]:
            if self.ghost_mode or self.level.empty_at(new_player_pos):
                self.player.move(delta)
                self.viewport_pos = (
                    self.viewport_pos[0] + delta[0],
                    self.viewport_pos[1] + delta[1],
                )


if __name__ == '__main__':
    game = Game()
    game.setup()
    game.main()
