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
        self.tiles = []
        self.raw_map_data = []
        self.scaled_tiles = []  # dla cull rendering (w budowie)
        #self.width_px
        #self.height_px

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

            # dlugosc i wysokosc mapy w px
            self.width_px = len(self.raw_map_data[0]) * TILE_SIZE
            self.height_px = len(self.raw_map_data) * TILE_SIZE

    def draw(self, surface, camera):
        map_width_tiles = len(self.tiles[0])
        map_height_tiles = len(self.tiles)

        start_x, end_x, start_y, end_y = camera.get_visible_tile_range(TILE_SIZE, map_width_tiles,
                                                                       map_height_tiles)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.tiles[y][x]
                pos_x = (x * TILE_SIZE - camera.camera.x) * camera.zoom
                pos_y = (y * TILE_SIZE - camera.camera.y) * camera.zoom

                tile_image = camera.apply_surface(tile.image)
                surface.blit(tile_image, (int(pos_x), int(pos_y)))

    def check_collision(self, rect, dx, dy):
        new_rect = rect.move(dx, 0)
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile.is_solid:
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
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
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if new_rect.colliderect(tile_rect):
                        if dy > 0:
                            new_rect.bottom = tile_rect.top
                        elif dy < 0:
                            new_rect.top = tile_rect.bottom
        rect.y = new_rect.y
        return rect.x, rect.y


    # dla cull rendering (w budowie)
    def rescale_tiles(self, zoom):
        self.scaled_tiles = []
        for row in self.tiles:
            scaled_row = []
            for tile in row:
                w = int(tile.image.get_width() * zoom)
                h = int(tile.image.get_height() * zoom)
                scaled_image = pygame.transform.scale(tile.image, (w, h))
                scaled_row.append(scaled_image)
            self.scaled_tiles.append(scaled_row)