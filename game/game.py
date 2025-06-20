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


        tree_image_path = get_asset_path("tree.png")
        rock_image_path = get_asset_path("rock.png")
        bow_image_path = get_asset_path("bow.png")
        sword_image_path = get_asset_path("sword.png")
        axe_image_path = get_asset_path("axe.png")
        pickaxe_image_path = get_asset_path("pickaxe.png")
        tree_stump_image_path = get_asset_path("tree_stump.png")

        bush_image_path = get_asset_path("bush_dark.png")
        bush_image = pygame.image.load(bush_image_path).convert_alpha()
        bush_image = pygame.transform.smoothscale(bush_image, (32, 32))

        self.tree_sprites = []

        for y, row in enumerate(self.game_map.tiles):
            for x, tile in enumerate(row):
                tile_id = self.game_map.raw_map_data[y][x]
                if tile_id == 27:
                    sprite = Sprite(tree_image_path, x * TILE_SIZE, y * TILE_SIZE, offset_y=96)
                    self.tree_sprites.append((sprite, x, y))
                elif tile_id == 24:
                    Sprite(rock_image_path, x * TILE_SIZE, y * TILE_SIZE)
                elif tile_id == 28:
                    Sprite(bow_image_path, x * TILE_SIZE, y * TILE_SIZE)
                elif tile_id == 29:
                    Sprite(sword_image_path, x * TILE_SIZE, y * TILE_SIZE)
                elif tile_id == 30:
                    Sprite(axe_image_path, x * TILE_SIZE, y * TILE_SIZE)
                elif tile_id == 31:
                    Sprite(pickaxe_image_path, x * TILE_SIZE, y * TILE_SIZE)
                tile_name = self.tile_kinds[tile_id].name
                if tile_name == "chest":
                    pos = (x * TILE_SIZE, y * TILE_SIZE)
                    self.game_map.tiles[y][x] = ChestTile("chest", get_asset_path("chest2.png"), True, pos)

                if tile_name == "grass":
                    if random.random() < 0.15:  # 15% szansy na krzak
                        bush_sprite = Sprite(bush_image, x * TILE_SIZE, y * TILE_SIZE)


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
                    if event.key == pygame.K_e:
                        self.check_chest_interactions()
                        self.check_tree_interactions()

                    if event.key == pygame.K_UP:
                        self.camera.zoom = min(4.0, self.camera.zoom + 0.25)
                        self.game_map.rescale_tiles(self.camera.zoom)

                    if event.key == pygame.K_DOWN:
                        self.camera.zoom = max(0.25, self.camera.zoom - 0.25)
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



            # Renderowanie obrazu tylko dla widocznego obszaru.

            start_x = max(0, int(self.camera.camera.x // TILE_SIZE) + 5) # +2 jest dla testu (żeby bylo widac jak to dziala)
            start_y = max(0, int(self.camera.camera.y // TILE_SIZE) + 5) # +2 jest dla testu
            end_x = min(len(self.game_map.scaled_tiles[0]),
                        int((self.camera.camera.x + self.camera.width / self.camera.zoom) // TILE_SIZE) +1 - 4) # -2 jest dla testu
            end_y = min(len(self.game_map.scaled_tiles),
                        int((self.camera.camera.y + self.camera.height / self.camera.zoom) // TILE_SIZE) +1 - 4) # -2 jest dla testu

            for y in range(start_y, end_y):
                for x in range(start_x, end_x):
                    tile_image = self.game_map.scaled_tiles[y][x]
                    pos_x = (x * TILE_SIZE * self.camera.zoom) - self.camera.camera.x * self.camera.zoom
                    pos_y = (y * TILE_SIZE * self.camera.zoom) - self.camera.camera.y * self.camera.zoom
                    self.screen.blit(tile_image, (int(pos_x), int(pos_y)))


            # wyswietlanie Sprite
            for s in sprites:

                # sprawdzanie czy ma atrybut "picked_up" - wykorzystywane przy podnoszeniu itemow do ekwipunku
                if hasattr(s, "picked_up") and s.picked_up:
                    continue

                # gdzie sie zaczyna i konczy Sprite:
                left, top, right, bottom = s.get_tile_bounds()

                # Rysowanie Sprite gdy granica znajduje sie w zasiegu widzenia (kamery)
                if right >= start_x and left < end_x and bottom >= start_y and top < end_y:
                    s.draw(self.screen, self.camera)


            self.player.draw_inventory(self.screen, self.player.inventory)
            self.camera.update()

            pygame.display.flip()

        pygame.quit()