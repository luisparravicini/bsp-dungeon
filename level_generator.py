from generators import BSPGenerator
import conf


class LevelGenerator:

    def __init__(self, level):
        self.level = level
        self.generator = BSPGenerator(self.level, conf.NO_TILE_POS)

    def create(self):
        self.generator.create()
