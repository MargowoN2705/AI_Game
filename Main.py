import pygame

from game.game import Game
from game_map.map_editor import MapEditor


#TODO Naprwic Maina

def main():
    print ("Gra: 1.")
    print ('Edytor: 2')
    if input() == 1 :
        game = Game()
        game.run_game()
    else:
        tile_image_data = [
            ("grass", "../images/grass.png", False),  # 0
            ("rock_tile", "../images/rock_tile.png", True),  # 1
            ("water", "../images/water.png", True),  # 2
            ("wood", "../images/wood.png", False),  # 3
            ("tree", "../images/tree.png", True),  # 4
            ("rock", "../images/rock.png", True),  # 5
            ("sand", "../images/sand.png", False),  # 6
            ("dirt", "../images/dirt.png", False),  # 7
            ("ice", "../images/ice.png", False),  # 8
            ("lava", "../images/lava.png", False),  # 9

            ("bow", "../images/bow.png", True),  # 10
            ("sword", "../images/sword.png", True),  # 11
            ("axe", "../images/axe.png", True),  # 12
            ("pickaxe", "../images/pickaxe.png", True),  # 13

            # Warianty / efekty
            ("grass_dark", "../images/grass_dark.png", False),  # 14
            ("water_bright", "../images/water_bright.png", True),  # 15
            ("wood_red", "../images/wood_red.png", False),  # 16
            ("dirt_dark", "../images/dirt_dark.png", False),  # 17
            ("grass_bright", "../images/grass_bright.png", False),  # 18
            ("water_dark", "../images/water_dark.png", True),  # 19
            ("inny_wood", "../images/inny_wood.png", False),  # 20
            ("rock_tile_dark", "../images/rock_tile_dark.png", True),  # 21

            # Twoje nowe warianty z efektami
            ("grass_inverted", "../images/grass_inverted.png", False),  # 22
            ("water_high_contrast", "../images/water_high_contrast.png", True),  # 23
            ("wood_vibrant", "../images/wood_vibrant.png", False),  # 24
            ("dirt_desaturated", "../images/dirt_desaturated.png", False),  # 25
            ("rock_tile_glow", "../images/rock_tile_glow.png", True),  # 26
            ("chest", "../images/chest2.png", True),

        ]

        pygame.init()
        screen_info = pygame.display.Info()

        editor = MapEditor(
            map_path="../game_map/maps_storage/map_1.map",
            tile_image_data=tile_image_data,
            tile_size=32,
            screen_width=screen_info.current_w,
            screen_height=screen_info.current_h
        )

        editor.run()

if __name__ == "__main__":
    main()