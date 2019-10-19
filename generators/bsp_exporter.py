import json
import pygame


class Exporter:
    def __init__(self, generator):
        self.generator = generator

    def save(self, path):
        with open(path, 'w') as file:
            rooms = [[r.x, r.y, r.width, r.height] for r in self.generator.rooms]
            data = {
                'rooms': rooms,
                'corridors': self.generator.corridors,
            }
            json.dump(data, file)

    def load(self, path):
        with open(path) as file:
            rooms = [[r.x, r.y, r.width, r.height] for r in self.generator.rooms]
            data = {
                'rooms': rooms,
                'corridors': self.generator.corridors,
            }
            data = json.load(file)
            self.generator.corridors = data['corridors']
            self.generator.rooms = [pygame.Rect(c[0], c[1], c[2], c[3]) for c in data['rooms']]
