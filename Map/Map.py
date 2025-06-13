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
        self.raw_map_data = []

        with open(map_file, "r") as f:
            lines = f.readlines()

        for y, line in enumerate(lines):
            row = []
            raw_row = []
            line = line.strip()
            for x, char in enumerate(line):
                if char.isdigit():
                    index = int(char)
                    tile_kind = tile_kinds[min(index, len(tile_kinds) - 1)]
                    row.append(tile_kind)
                    raw_row.append(index)
                else:
                    tile_kind = tile_kinds[0]
                    row.append(tile_kind)
                    raw_row.append(0)
            self.tiles.append(row)
            self.raw_map_data.append(raw_row)

    def draw(self, surface):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                pos_x = x * self.tile_size
                pos_y = y * self.tile_size
                surface.blit(tile.image, (pos_x, pos_y))

    def check_collision(self, rect, dx, dy):
        new_rect = rect.move(dx, 0)
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile.is_solid:
                    tile_rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    if new_rect.colliderect(tile_rect):
                        if dx > 0:
                            new_rect.right = tile_rect.left
                        elif dx < 0:
                            new_rect.left = tile_rect.right
        rect.x = new_rect.x

        new_rect = rect.move(0, dy)
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile.is_solid:
                    tile_rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    if new_rect.colliderect(tile_rect):
                        if dy > 0:
                            new_rect.bottom = tile_rect.top
                        elif dy < 0:
                            new_rect.top = tile_rect.bottom
        rect.y = new_rect.y
        return rect.x, rect.y
