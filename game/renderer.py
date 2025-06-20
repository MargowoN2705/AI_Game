from config import TILE_SIZE


def render_visible_area(camera, game_map, screen, sprites):

    # gdzie sie zaczyna i konczy widoczny obszar (kamera)
    start_x = max(0, int(camera.camera.x // TILE_SIZE) + 5)  # +2 jest dla testu (żeby bylo widac jak to dziala)
    start_y = max(0, int(camera.camera.y // TILE_SIZE) + 5)  # +2 jest dla testu
    end_x = min(len(game_map.scaled_tiles[0]),
                int((
                                camera.camera.x + camera.width / camera.zoom) // TILE_SIZE) + 1 - 4)  # -2 jest dla testu
    end_y = min(len(game_map.scaled_tiles),
                int((
                                camera.camera.y + camera.height / camera.zoom) // TILE_SIZE) + 1 - 4)  # -2 jest dla testu

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
        left, top, right, bottom = s.get_tile_bounds()

        # Rysowanie Sprite gdy granica znajduje sie w zasiegu widzenia (kamery)
        if right >= start_x and left < end_x and bottom >= start_y and top < end_y:
            s.draw(screen, camera)
