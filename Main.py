from Game.Game import Game
from Map.Map_Editor import MapEditor
import pygame


#TODO Naprwic Maina


if __name__ == "__main__":
    print ("Gra: 1.")
    print ('Edytor: 2')
    if input() == 1 :
        game = Game()
        game.Run_Game()
    else:
        tile_image_data = [
            ("grass", "../Images/grass.png", False),  # 0
            ("rock_tile", "../Images/rock_tile.png", True),  # 1
            ("water", "../Images/water.png", True),  # 2
            ("wood", "../Images/wood.png", False),  # 3
            ("tree", "../Images/tree.png", True),  # 4
            ("rock", "../Images/rock.png", True),  # 5
            ("sand", "../Images/sand.png", False),  # 6
            ("dirt", "../Images/dirt.png", False),  # 7
            ("ice", "../Images/ice.png", False),  # 8
            ("lava", "../Images/lava.png", False),  # 9

            ("bow", "../Images/bow.png", True),  # 10
            ("sword", "../Images/sword.png", True),  # 11
            ("axe", "../Images/axe.png", True),  # 12
            ("pickaxe", "../Images/pickaxe.png", True),  # 13

            # Warianty / efekty
            ("grass_dark", "../Images/grass_dark.png", False),  # 14
            ("water_bright", "../Images/water_bright.png", True),  # 15
            ("wood_red", "../Images/wood_red.png", False),  # 16
            ("dirt_dark", "../Images/dirt_dark.png", False),  # 17
            ("grass_bright", "../Images/grass_bright.png", False),  # 18
            ("water_dark", "../Images/water_dark.png", True),  # 19
            ("inny_wood", "../Images/inny_wood.png", False),  # 20
            ("rock_tile_dark", "../Images/rock_tile_dark.png", True),  # 21

            # Twoje nowe warianty z efektami
            ("grass_inverted", "../Images/grass_inverted.png", False),  # 22
            ("water_high_contrast", "../Images/water_high_contrast.png", True),  # 23
            ("wood_vibrant", "../Images/wood_vibrant.png", False),  # 24
            ("dirt_desaturated", "../Images/dirt_desaturated.png", False),  # 25
            ("rock_tile_glow", "../Images/rock_tile_glow.png", True),  # 26
            ("chest", "../Images/chest2.png", True),

        ]

        pygame.init()
        screen_info = pygame.display.Info()

        editor = MapEditor(
            map_path="../Map/Maps_Storage/map_1.map",
            tile_image_data=tile_image_data,
            tile_size=32,
            screen_width=screen_info.current_w,
            screen_height=screen_info.current_h
        )

        editor.run()