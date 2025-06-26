from agent.agent import Agent
from config import TILE_SIZE
import pygame
from config import get_asset_path, SPRITE_TILES
import random

def render_sprites(tiles, tile_kinds, Sprite):
    assets = SPRITE_TILES

    bush_image = pygame.image.load(get_asset_path("bush_dark.png")).convert_alpha()
    bush_image = pygame.transform.smoothscale(bush_image, (32, 32))

    tree_sprites = []
    all_sprites = []

    for y, row in enumerate(tiles):
        for x, tile_id in enumerate(row):
            pos = (x * TILE_SIZE, y * TILE_SIZE)

            # Dodawanie sprite'ów z assets
            if tile_id in assets:
                if tile_id == 27:  # drzewo
                    sprite = Sprite(assets[tile_id], *pos, offset_y=96)
                    tree_sprites.append((sprite, x, y))
                else:
                    sprite = Sprite(assets[tile_id], *pos)
                all_sprites.append(sprite)

            # Dodatkowe dekoracje na trawie
            tile_name = tile_kinds[tile_id].name
            if tile_name == "grass" and random.random() < 0.15:
                bush_sprite = Sprite(bush_image, *pos)
                all_sprites.append(bush_sprite)

    return all_sprites, tree_sprites