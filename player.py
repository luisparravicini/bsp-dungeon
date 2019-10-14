import conf
import pygame


class Player:
    def __init__(self, room_pos):
        self.pos = list(room_pos)

    def move(self, delta):
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]


class PlayerView:
    def __init__(self, spritesheet, player, surface):
        self.player = player
        self.sprite = spritesheet.tile_at((18, 7))
        self.surface = surface
        self.looking_left = False

    def update(self, viewport_pos):
        self._blit(viewport_pos)

    def _blit(self, viewport_pos):
        surface_pos = (
            # tuple(v * conf.TILE_SIZE for v in self.player.pos)
            (self.player.pos[0] - viewport_pos[0]) * conf.TILE_SIZE,
            (self.player.pos[1] - viewport_pos[1]) * conf.TILE_SIZE,
        )
        sprite = pygame.transform.flip(self.sprite, self.looking_left, False)
        self.surface.blit(sprite, surface_pos)
