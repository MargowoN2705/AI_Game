from agent.agent import Agent
from config import TILE_SIZE
import pygame
from config import get_asset_path, SPRITE_TILES
import random

def render_visible_area(camera, game_map, screen, sprites):

    # gdzie sie zaczyna i konczy widoczny obszar (kamera)
    start_x = max(0, int(camera.camera.x // TILE_SIZE) + 5)  # +2 jest dla testu (żeby bylo widac jak to dziala)
    start_y = max(0, int(camera.camera.y // TILE_SIZE) + 5)  # +2 jest dla testu
    end_x = min(len(game_map.scaled_tiles[0]),
                int((camera.camera.x + camera.width / camera.zoom) // TILE_SIZE) + 1 - 4)  # -2 jest dla testu
    end_y = min(len(game_map.scaled_tiles),
                int(( camera.camera.y + camera.height / camera.zoom) // TILE_SIZE) + 1 - 4)  # -2 jest dla testu

    # wyswietlanie Tile'ow dla widocznego obszaru (kamery)
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            tile_image = game_map.scaled_tiles[y][x]
            pos_x = (x * TILE_SIZE * camera.zoom) - camera.camera.x * camera.zoom
            pos_y = (y * TILE_SIZE * camera.zoom) - camera.camera.y * camera.zoom
            screen.blit(tile_image, (int(pos_x), int(pos_y)))

    # wyswietlanie Sprite
    for s in sprites:

        if hasattr(s, "picked_up") and s.picked_up:
            continue

        # gdzie sie zaczyna i konczy Sprite:

        left, top, right, bottom = s.get_bounds()

        # Rysowanie Sprite gdy granica znajduje sie w zasiegu widzenia (kamery)
        if right >= start_x and left < end_x and bottom >= start_y and top < end_y:
            s.draw(screen, camera)





def render_sprites(tiles, tile_kinds, Sprite):

    assets = {tile_id: pygame.image.load(get_asset_path(name)).convert_alpha()
              for tile_id, name in SPRITE_TILES.items()}

    bush_image = pygame.image.load(get_asset_path("bush_dark.png")).convert_alpha()
    bush_image = pygame.transform.smoothscale(bush_image, (32, 32))

    tree_sprites = []
    all_sprites = []

    for y, row in enumerate(tiles):
        for x, tile_id in enumerate(row):
            pos = (x * TILE_SIZE, y * TILE_SIZE)

            # Dodawanie sprite'ów po tile_id
            if tile_id in assets:
                if tile_id == 27:  # tree
                    sprite = Sprite(assets[tile_id], *pos, offset_y=96)
                    tree_sprites.append((sprite, x, y))
                else:
                    sprite = Sprite(assets[tile_id], *pos)
                all_sprites.append(sprite)

            # Sprawdzenie nazwy kafelka
            tile_name = tile_kinds[tile_id].name


            if tile_name == "chest":
                pass #game_map.tiles[y][x] = ChestTile("chest", get_asset_path("chest2.png"), True, pos)

            elif tile_name == "grass" and random.random() < 0.15:
                bush_sprite = Sprite(bush_image, *pos)
                all_sprites.append(bush_sprite)

    return all_sprites, tree_sprites