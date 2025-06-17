import pygame
from pygame import FULLSCREEN
import random
from .player import Player
from .sprite import sprites,Sprite
from game_map.game_map import Map,Tile,ChestTile
from .camera import Camera
from config import get_asset_path
from .item import Item, ItemEntity, Inventory
from .team_manager import TeamManager

class Game:

    def __init__(self):
        pygame.init()


        self.camera = Camera()

        self.clear_color = (0, 0, 0)

        infoObject = pygame.display.Info()
        screen_width = infoObject.current_w
        screen_height = infoObject.current_h

        self.screen = self.camera.create_screen(screen_width, screen_height, 'GameAI', pygame.FULLSCREEN)

        self.keys_down = set()
        self.GAME_SPEED = 60

        self.tile_kinds = [
            # 0–9: podstawowe podłoża i warianty
            Tile("grass", get_asset_path("grass.png"), False),  # 0
            Tile("grass_dark", get_asset_path("grass_dark.png"), False),  # 1
            Tile("grass_bright", get_asset_path("grass_bright.png"), False),  # 2
            Tile("grass_dark_1", get_asset_path("grass_dark_1.png"), False),  # 3
            Tile("grass_dark_2", get_asset_path("grass_dark_2.png"), False),  # 4
            Tile("grass_dark_3", get_asset_path("grass_dark_3.png"), False),  # 5
            Tile("grass_dark_4", get_asset_path("grass_dark_4.png"), False),  # 6
            Tile("grass_dark_5", get_asset_path("grass_dark_5.png"), False),  # 7
            Tile("rock_tile", get_asset_path("rock_tile.png"), True),  # 8
            Tile("rock_tile_dark", get_asset_path("rock_tile_dark.png"), True),  # 9

            # 10–14: woda i warianty
            Tile("water", get_asset_path("water.png"), True),  # 10
            Tile("water_bright", get_asset_path("water_bright.png"), True),  # 11
            Tile("water_dark", get_asset_path("water_dark.png"), True),  # 12
            Tile("water_high_contrast", get_asset_path("water_high_contrast.png"), True),  # 13

            # 15–17: drewno i warianty
            Tile("wood", get_asset_path("wood.png"), False),  # 14
            Tile("wood_red", get_asset_path("wood_red.png"), False),  # 15
            Tile("wood_vibrant", get_asset_path("wood_vibrant.png"), False),  # 16
            Tile("inny_wood", get_asset_path("inny_wood.png"), False),  # 17

            # 18–19: ziemia i warianty
            Tile("dirt", get_asset_path("dirt.png"), False),  # 18
            Tile("dirt_dark", get_asset_path("dirt_dark.png"), False),  # 19
            Tile("dirt_desaturated", get_asset_path("dirt_desaturated.png"), False),  # 20

            # 21–24: inne naturalne elementy
            Tile("sand", get_asset_path("sand.png"), False),  # 21
            Tile("ice", get_asset_path("ice.png"), False),  # 22
            Tile("lava", get_asset_path("lava.png"), False),  # 23
            Tile("rock", get_asset_path("grass.png"), True),  # 24

            # 25–28: efekty specjalne
            Tile("grass_inverted", get_asset_path("grass_inverted.png"), False),  # 25
            Tile("rock_tile_glow", get_asset_path("rock_tile_glow.png"), True),  # 26

            # 29–33: obiekty interaktywne
            Tile("tree", get_asset_path("grass_dark.png"), True),  # 27
            Tile("bow", get_asset_path("grass.png"), True),  # 28
            Tile("sword", get_asset_path("grass.png"), True),  # 29
            Tile("axe", get_asset_path("grass_dark.png"), True),  # 30
            Tile("pickaxe", get_asset_path("grass_dark.png"), True),  # 31
            Tile("chest", get_asset_path("chest2.png"), True),  # 32
        ]

        self.game_map = Map(get_asset_path("game_map", "maps_storage", "simple_map.map", own_path=True), self.tile_kinds, 32)


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


        tile_size = self.game_map.tile_size
        self.tree_sprites = []

        for y, row in enumerate(self.game_map.tiles):
            for x, tile in enumerate(row):
                tile_id = self.game_map.raw_map_data[y][x]
                if tile_id == 27:
                    sprite = Sprite(tree_image_path, x * tile_size, y * tile_size, offset_y=96)
                    self.tree_sprites.append((sprite, x, y))
                elif tile_id == 24:
                    Sprite(rock_image_path, x * tile_size, y * tile_size)
                elif tile_id == 28:
                    Sprite(bow_image_path, x * tile_size, y * tile_size)
                elif tile_id == 29:
                    Sprite(sword_image_path, x * tile_size, y * tile_size)
                elif tile_id == 30:
                    Sprite(axe_image_path, x * tile_size, y * tile_size)
                elif tile_id == 31:
                    Sprite(pickaxe_image_path, x * tile_size, y * tile_size)
                tile_name = self.tile_kinds[tile_id].name
                if tile_name == "chest":
                    pos = (x * tile_size, y * tile_size)
                    self.game_map.tiles[y][x] = ChestTile("chest", get_asset_path("chest2.png"), True, pos)

                if tile_name == "grass":
                    if random.random() < 0.15:  # 15% szansy na krzak
                        bush_sprite = Sprite(bush_image, x * tile_size, y * tile_size)

        map_width_px = len(self.game_map.raw_map_data[0]) * 32 #TODO zmienic 32 na tile_size, aby zbyla zmienna, dynamiczna
        map_height_px = len(self.game_map.raw_map_data) * 32

        player_start_x = map_width_px // 2
        player_start_y = map_height_px // 2



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

        self.reset_game()

    def check_chest_interactions(self):
        for row in self.game_map.tiles:
            for tile in row:
                if isinstance(tile, ChestTile):
                    if self.player.rect.colliderect(tile.rect):
                        tile.toggle()

    def check_tree_interactions(self):
        for sprite, x, y in self.tree_sprites:
            tile_x = x * self.game_map.tile_size
            tile_y = y * self.game_map.tile_size

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

                    if event.key == pygame.K_DOWN:
                        self.camera.zoom = max(0.25, self.camera.zoom - 0.25)

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

            for y, row in enumerate(self.game_map.tiles):
                for x, tile in enumerate(row):
                    tile_pos = (x * self.game_map.tile_size, y * self.game_map.tile_size)
                    screen_pos = self.camera.apply(tile_pos)
                    tile_image = self.camera.apply_surface(tile.image)
                    self.screen.blit(tile_image, screen_pos)

            for s in sprites:
                if hasattr(s, "picked_up") and s.picked_up:
                    continue
                s.draw(self.screen, self.camera)

            self.team_manager.draw(self.screen, self.camera)
            self.player.draw_inventory(self.screen, self.player.inventory)
            self.camera.update()

            pygame.display.flip()

        pygame.quit()


game = Game()
game.run_game()

