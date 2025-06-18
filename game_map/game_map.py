import pygame
from config import TILE_SIZE


class Tile:
    def __init__(self, name, image, is_solid):
        self.name = name
        if isinstance(image, str):
            self.image = pygame.image.load(image).convert_alpha()
        else:
            # image jest już pygame.Surface
            self.image = image
        self.is_solid = is_solid

class ChestTile(Tile):
    def __init__(self, name, image_path, is_solid, position):

        full_image = pygame.image.load(image_path).convert_alpha()


        self.closed_img = full_image.subsurface(pygame.Rect(0, 0, 32, 32))
        self.open_img = full_image.subsurface(pygame.Rect(32, 0, 32, 32))


        super().__init__(name, self.closed_img, is_solid)

        self.is_open = False
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], 32, 32)

    def toggle(self):
        self.is_open = not self.is_open
        self.image = self.open_img if self.is_open else self.closed_img
        print(f"Chest toggled: {'open' if self.is_open else 'closed'}")


class Map:

    def __init__(self, map_file, tile_kinds):
        self.tile_size = TILE_SIZE
        self.tiles = []
        self.raw_map_data = []

        with open(map_file, "r") as f:
            lines = f.readlines()

        for y, line in enumerate(lines):
            row = []
            raw_row = []
            line = line.strip()

            parts = line.split()
            for x, part in enumerate(parts):
                if part.isdigit():
                    index = int(part)
                    tile_kind = tile_kinds[min(index, len(tile_kinds) - 1)]
                    row.append(tile_kind)
                    raw_row.append(index)
                else:
                    tile_kind = tile_kinds[0]
                    row.append(tile_kind)
                    raw_row.append(0)
            self.tiles.append(row)
            self.raw_map_data.append(raw_row)

    def draw(self, surface,camera):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                pos_x = x * self.tile_size - camera.camera.x
                pos_y = y * self.tile_size - camera.camera.y
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
