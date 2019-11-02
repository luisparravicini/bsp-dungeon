import spritesheet
import pygame
import conf


class SpritesheetManager:
    def __init__(self, path):
        self.sheet = spritesheet.spritesheet('tiles-color.png')
        size = tuple(v * conf.SCALE for v in self.sheet.sheet.get_size())
        self.sheet.sheet = pygame.transform.scale(self.sheet.sheet, size)

        self.empty_tile = pygame.Surface((conf.TILE_SIZE, conf.TILE_SIZE))
        self.empty_tile.fill(pygame.Color('black'))

    def blit_tile_at(self, surface, surface_pos, tile_pos):
        if tile_pos == conf.NO_TILE_POS:
            surface.blit(self.empty_tile, surface_pos)
        else:
            tile_rect = self._tile_rect_at(tile_pos)
            surface.blit(self.sheet.sheet, surface_pos, area=tile_rect)

    def _tile_rect_at(self, pos):
        cell_size = conf.TILE_SIZE + 1 * conf.SCALE
        return tuple(v * cell_size for v in pos) + (conf.TILE_SIZE,) * 2

    def tile_at(self, pos):
        # colorkey = Color('black')
        # colorkey = (71, 45, 60)

        return self.sheet.image_at(
            self._tile_rect_at(pos)
            # colorkey=colorkey
        )
