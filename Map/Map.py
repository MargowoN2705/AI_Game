import pygame

class Tile:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image = pygame.image.load(image).convert_alpha()
        self.is_solid = is_solid

class Map:
    def __init__(self, map_file, tile_kinds, tile_size):
        self.tile_size = tile_size
        self.tiles = []

        with open(map_file, "r") as f:
            lines = f.readlines()

        for y, line in enumerate(lines):
            row = []
            line = line.strip()
            for x, char in enumerate(line):
                if char.isdigit():
                    index = int(char)
                    tile_kind = tile_kinds[index]
                    row.append(tile_kind)
                else:
                    tile_kind = tile_kinds[0]  # grass
                    row.append(tile_kind)
            self.tiles.append(row)

    def draw(self, surface):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                pos_x = x * self.tile_size
                pos_y = y * self.tile_size
                surface.blit(tile.image, (pos_x, pos_y))

