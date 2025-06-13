import pygame
from pygame import FULLSCREEN
import random
from Player import Player
from Sprite import sprites,Sprite
from Map.Map import Map,Tile


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("GameAI")

        screen_info = pygame.display.Info()
        width, height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((width, height), FULLSCREEN)

        self.clear_color = (30, 150, 50)
        self.screen = screen
        self.keys_down = set()
        self.GAME_SPEED = 60


        self.tile_kinds = [
            Tile("grass", "../Images/grass.png", False),
            Tile("wall", "../Images/rock.png", True),
            Tile("water", "../Images/water.png", True),
            Tile("wood", "../Images/wood.png", False),
            Tile("sand", "../Images/sand.png", False),
        ]


        self.game_map = Map("../Map/Maps_Storage/map_1.map", self.tile_kinds, 32)

        tree_image_path = "../Images/tree.png"
        num_trees = 15
        tile_size = self.game_map.tile_size

        for _ in range(num_trees):
            while True:
                x = random.randint(0, len(self.game_map.tiles[0]) - 1)
                y = random.randint(0, len(self.game_map.tiles) - 1)
                tile = self.game_map.tiles[y][x]

                if tile.name == "grass":
                    Sprite(tree_image_path, x * tile_size, y * tile_size)
                    break

        self.player = Player("../Images/player.png", 100, 100, a=0.5)

        self.Reset_Game()

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

            self.player.Update()
            self.screen.fill(self.clear_color)


            for y, row in enumerate(self.game_map.tiles):
                for x, tile in enumerate(row):
                    self.screen.blit(tile.image, (x * self.game_map.tile_size, y * self.game_map.tile_size))


            for s in sprites:
                s.draw(self.screen)

            pygame.display.flip()

        pygame.quit()


game = Game()
game.Run_Game()
