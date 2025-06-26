import pygame
from config import TILE_SIZE, SPRITE_TILES, get_asset_path
import random

sprites = []
loaded = {}

class Sprite:
    def __init__(self, image, x, y, offset_y=0):
        if isinstance(image, pygame.Surface):
            self.image = image
        else:
            if image in loaded:
                self.image = loaded[image]
            else:
                self.image = pygame.image.load(image).convert_alpha()
                loaded[image] = self.image
        self.x = x
        self.y = y
        self.offset_y = offset_y
        sprites.append(self)

    @classmethod
    def from_tiles(cls, tiles, tile_kinds):
        assets = SPRITE_TILES
        bush_image = pygame.image.load(get_asset_path("bush_dark.png")).convert_alpha()
        bush_image = pygame.transform.smoothscale(bush_image, (32, 32))

        all_sprites = []
        tree_sprites = []

        for y, row in enumerate(tiles):
            for x, tile_id in enumerate(row):
                pos = (x * TILE_SIZE, y * TILE_SIZE)

                if tile_id in assets:
                    if tile_id == 27:
                        sprite = cls(assets[tile_id], *pos, offset_y=96)
                        tree_sprites.append((sprite, x, y))
                    else:
                        sprite = cls(assets[tile_id], *pos)
                    all_sprites.append(sprite)

                if tile_kinds[tile_id].name == "grass" and random.random() < 0.15:
                    bush_sprite = cls(bush_image, *pos)
                    all_sprites.append(bush_sprite)

        return all_sprites, tree_sprites

    def destroy(self):
        if self in sprites:
            sprites.remove(self)

    def get_bounds(self):
        render_y = self.y - self.offset_y  # uwzględnij przesunięcie
        left = self.x // TILE_SIZE
        top = render_y // TILE_SIZE
        right = (self.x + self.image.get_width()) // TILE_SIZE
        bottom = (render_y + self.image.get_height()) // TILE_SIZE
        return int(left), int(top), int(right), int(bottom)


    def draw(self, screen, camera):
        pos = (self.x, self.y - self.offset_y)
        pos = camera.apply(pos)  # przesuwamy i skalujemy pozycję

        scaled_image = camera.apply_surface(self.image)  # skalujemy obrazek

        screen.blit(scaled_image, pos)


    def draw_inventory(self, screen, inventory):
        slot_size = 40
        margin = 10
        start_x = (screen.get_width() - (slot_size + margin) * len(inventory.slots)) // 2
        y = screen.get_height() - slot_size - 10

        #font = pygame.font.SysFont(None, 18)

        for i, item in enumerate(inventory.slots):
            x = start_x + i * (slot_size + margin)
            color = (255, 255, 0) if i == inventory.selected_index else (100, 100, 100)
            pygame.draw.rect(screen, color, (x, y, slot_size, slot_size), 2)

            if item:
                scaled_img = pygame.transform.scale(item.image, (32, 32))
                screen.blit(scaled_img, (x + 4, y + 4))


    def change_image(self, new_image_path):
        self.image = pygame.image.load(new_image_path).convert_alpha()