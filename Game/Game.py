import pygame
from pygame import FULLSCREEN
import random
from Player import Player
from Sprite import sprites,Sprite
from Map.Map import Map,Tile,ChestTile
from camera import Camera



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
            Tile("grass", "../Images/grass.png", False),  # 0
            Tile("rock_tile", "../Images/rock_tile.png", True),  # 1
            Tile("water", "../Images/water.png", True),  # 2
            Tile("wood", "../Images/wood.png", False),  # 3
            Tile("tree", "../Images/grass_dark.png", True),  # 4
            Tile("rock", "../Images/grass.png", True),  # 5
            Tile("sand", "../Images/sand.png", False),  # 6
            Tile("dirt", "../Images/dirt.png", False),  # 7
            Tile("ice", "../Images/ice.png", False),  # 8
            Tile("lava", "../Images/lava.png", False),  # 9

            Tile("bow", "../Images/grass.png", True),  # 10
            Tile("sword", "../Images/grass.png", True),  # 11
            Tile("axe", "../Images/grass_dark.png", True),  # 12
            Tile("pickaxe", "../Images/grass_dark.png", True),  # 13

            Tile("grass_dark", "../Images/grass_dark.png", False),  # 14
            Tile("water_bright", "../Images/water_bright.png", True),  # 15
            Tile("wood_red", "../Images/wood_red.png", False),  # 16
            Tile("dirt_dark", "../Images/dirt_dark.png", False),  # 17
            Tile("grass_bright", "../Images/grass_bright.png", False),  # 18
            Tile("water_dark", "../Images/water_dark.png", True),  # 19
            Tile("inny_wood", "../Images/inny_wood.png", False),  # 20
            Tile("rock_tile_dark", "../Images/rock_tile_dark.png", True),  # 21

            # Twoje nowe warianty z efektami
            Tile("grass_inverted", "../Images/grass_inverted.png", False),  # 22
            Tile("water_high_contrast", "../Images/water_high_contrast.png", True),  # 23
            Tile("wood_vibrant", "../Images/wood_vibrant.png", False),  # 24
            Tile("dirt_desaturated", "../Images/dirt_desaturated.png", False),  # 25
            Tile("rock_tile_glow", "../Images/rock_tile_glow.png", True),  # 26
            Tile("chest", "../Images/chest2.png", True),  # 27

        ]


        self.game_map = Map("../Map/Maps_Storage/map_1.map", self.tile_kinds, 32)


        tree_image_path = "../Images/tree.png"
        rock_image_path = "../Images/rock.png"
        bow_image_path = "../Images/bow.png"
        sword_image_path = "../Images/sword.png"
        axe_image_path = "../Images/axe.png"
        pickaxe_image_path = "../Images/pickaxe.png"

        tree_stump_image_path = "../Images/tree_stump.png"



        tile_size = self.game_map.tile_size
        self.tree_sprites = []

        for y, row in enumerate(self.game_map.tiles):
            for x, tile in enumerate(row):
                tile_id = self.game_map.raw_map_data[y][x]
                if tile_id == 4:
                    sprite = Sprite(tree_image_path, x * tile_size, y * tile_size, offset_y=96)
                    self.tree_sprites.append((sprite, x, y))
                elif tile_id == 5:
                    Sprite(rock_image_path, x * tile_size, y * tile_size)
                elif tile_id == 10:
                    Sprite(bow_image_path, x * tile_size, y * tile_size)
                elif tile_id == 11:
                    Sprite(sword_image_path, x * tile_size, y * tile_size)
                elif tile_id == 12:
                    Sprite(axe_image_path, x * tile_size, y * tile_size)
                elif tile_id == 13:
                    Sprite(pickaxe_image_path, x * tile_size, y * tile_size)
                tile_name = self.tile_kinds[tile_id].name
                if tile_name == "chest":
                    pos = (x * tile_size, y * tile_size)
                    self.game_map.tiles[y][x] = ChestTile("chest", "../Images/chest2.png", True, pos)

        map_width_px = len(self.game_map.raw_map_data[0]) * 32 #TODO zmienic 32 na tile_size, aby zbyla zmienna, dynamiczna
        map_height_px = len(self.game_map.raw_map_data) * 32

        player_start_x = map_width_px // 2
        player_start_y = map_height_px // 2

        self.player = Player("../Images/DarkRanger.png", player_start_x, player_start_y, a=0.5, game_map=self.game_map) #TODO Ogarnac bounding boxy

        self.Reset_Game()

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
                sprite.change_image("../Images/tree_stump.png")

    def Reset_Game(self):
        pass

    def is_key_pressed(self, key):
        return key in self.keys_down

    def Run_Game(self):
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

            dt = clock.tick(60) / 1000

            self.screen.fill(self.clear_color)  # <-- czyść ekran na samym początku!

            self.player.Update(self.camera, dt)

            for y, row in enumerate(self.game_map.tiles):
                for x, tile in enumerate(row):
                    tile_pos = (x * self.game_map.tile_size, y * self.game_map.tile_size)
                    screen_pos = self.camera.apply(tile_pos)
                    tile_image = self.camera.apply_surface(tile.image)
                    self.screen.blit(tile_image, screen_pos)

            for s in sprites:
                s.draw(self.screen, self.camera)

            self.player.draw(self.screen, self.camera)  # Rysuj gracza **raz** na końcu

            pygame.display.flip()

        pygame.quit()


game = Game()
game.Run_Game()

