import pygame
from pygame import FULLSCREEN
import random
from .player import Player
from .sprite import sprites,Sprite
from game_map.game_map import Map,Tile,ChestTile
from .camera import Camera
from config import get_asset_path, TILE_KINDS, GAME_CONFIG, TILE_SIZE
from .item import Item, ItemEntity, Inventory
from .team_manager import TeamManager


class Game:

    def __init__(self):
        pygame.init()

        self.font = pygame.font.SysFont(None, 24)

        self.camera = Camera()

        self.clear_color = GAME_CONFIG['clear_color']

        infoObject = pygame.display.Info()
        screen_width = infoObject.current_w
        screen_height = infoObject.current_h

        self.screen = self.camera.create_screen(screen_width, screen_height, GAME_CONFIG["title"], pygame.FULLSCREEN)

        self.keys_down = set()
        self.GAME_SPEED = GAME_CONFIG['game_speed']

        self.tile_kinds = [
            Tile(t["name"], get_asset_path(t["name"] + ".png"), t["solid"])
            for t in TILE_KINDS
        ]


        self.game_map = Map(GAME_CONFIG["game_map"], self.tile_kinds)

        # tworzejnie sprites
        self.sprites, self.tree_sprites = Sprite.from_tiles(self.game_map.raw_map_data, self.tile_kinds)

        player_start_x = self.game_map.width_px // 2
        player_start_y = self.game_map.height_px // 2


        self.player = Player(get_asset_path("../images/DarkRanger.png"), player_start_x, player_start_y, a=0.5, game_map=self.game_map) #TODO Ogarnac bounding boxy

        self.team_manager = TeamManager(self.game_map, self.player)
        self.camera.follow(self.player)

        # Przedmioty
        self.items = [
            Item("sword", get_asset_path("sword.png")),
            # Item("axe", "axe.png"),
        ]

        # Przedmioty w świecie
        self.item_entities = [
            ItemEntity(self.items[0], self.player.x, self.player.y),
            # ItemEntity(self.items[1], (10, 3)),
        ]

        self.game_map.rescale_tiles(self.camera.zoom) # ladowanie w inicie przeskalowanych obrazkow (lepsza wydajnosc)

        self.reset_game()

    def check_chest_interactions(self):
        for row in self.game_map.tiles:
            for tile in row:
                if isinstance(tile, ChestTile):
                    if self.player.rect.colliderect(tile.rect):
                        tile.toggle()

    def check_tree_interactions(self):
        for sprite, x, y in self.tree_sprites:
            tile_x = x * TILE_SIZE
            tile_y = y * TILE_SIZE

            sprite_rect = pygame.Rect(tile_x, tile_y, 32, 32)
            if self.player.rect.colliderect(sprite_rect):
                sprite.change_image(get_asset_path("tree_stump.png"))

    def reset_game(self):
        pass

    def is_key_pressed(self, key):
        return key in self.keys_down

    def run_game(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(self.GAME_SPEED)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.keys_down.add(event.key)
                    self.player.handle_key_down(event.key)
                elif event.type == pygame.KEYUP:
                    self.keys_down.discard(event.key)
                    self.player.handle_key_up(event.key)
                   # if event.key == pygame.K_e:
                     #   self.check_chest_interactions()
                     #   self.check_tree_interactions()

                    if event.key == pygame.K_UP:
                        self.camera.zoom = min(GAME_CONFIG['zoom_max'], self.camera.zoom + GAME_CONFIG['zoom_step'])
                        self.game_map.rescale_tiles(self.camera.zoom)

                    if event.key == pygame.K_DOWN:
                        self.camera.zoom = max(GAME_CONFIG['zoom_min'], self.camera.zoom - GAME_CONFIG['zoom_step'])
                        self.game_map.rescale_tiles(self.camera.zoom)

                    if event.key == pygame.K_q:
                        dropped_item = self.player.inventory.drop_item()
                        if dropped_item:
                            self.item_entities.append(ItemEntity(dropped_item, self.player.x, self.player.y))


                    if event.key == pygame.K_e:
                        for entity in self.item_entities:
                            if not entity.picked_up and self.player.rect.colliderect(entity.rect):
                                if self.player.inventory.add_item(entity.item):
                                    entity.picked_up = True
                                break

                    if event.key == pygame.K_1:
                        self.player.inventory.selected_index = 0

                    if event.key == pygame.K_2:
                        self.player.inventory.selected_index = 1

                    if event.key == pygame.K_3:
                        self.player.inventory.selected_index = 2

                    if event.key == pygame.K_4:
                        self.player.inventory.selected_index = 3

                    if event.key == pygame.K_5:
                        self.player.inventory.selected_index = 4

            dt = clock.tick(60) / 1000

            self.screen.fill(self.clear_color)  # <-- czyść ekran na samym początku!

            self.team_manager.update(dt)

            #render_visible_area(self.camera, self.game_map, self.screen, sprites)
            self.game_map.draw(self.screen, self.camera)

            for s in sprites:

                if hasattr(s, "picked_up") and s.picked_up:
                    continue

                # gdzie sie zaczyna i konczy Sprite:

                left, top, right, bottom = s.get_bounds()

                # Rysowanie Sprite gdy granica znajduje sie w zasiegu widzenia (kamery)
                start_x, end_x, start_y, end_y = self.camera.get_visible_tile_range(len(self.game_map.tiles[0]),
                                                                                    len(self.game_map.tiles))
                if right >= start_x and left < end_x and bottom >= start_y and top < end_y:
                    s.draw(self.screen, self.camera)

            self.player.draw_inventory(self.screen, self.player.inventory)
            self.camera.update()

            fps = clock.get_fps()
            fps_text = self.font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
            text_rect = fps_text.get_rect()
            text_rect.topright = (self.screen.get_width() - 10, 10)

            self.screen.blit(fps_text, text_rect)

            pygame.display.flip()

        pygame.quit()