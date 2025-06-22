import pygame
from game_map.map_editor import MapEditor
from pygame.display import Info

tile_image_data = [
    # 0–9: podstawowe podłoża i warianty
    ("grass", "images/grass.png", False),                    # 0
    ("grass_dark", "images/grass_dark.png", False),          # 1
    ("grass_bright", "images/grass_bright.png", False),      # 2
    ("grass_dark_1", "images/grass_dark_1.png", False),      # 3
    ("grass_dark_2", "images/grass_dark_2.png", False),      # 4
    ("grass_dark_3", "images/grass_dark_3.png", False),      # 5
    ("grass_dark_4", "images/grass_dark_4.png", False),      # 6
    ("grass_dark_5", "images/grass_dark_5.png", False),      # 7
    ("rock_tile", "images/rock_tile.png", True),             # 8
    ("rock_tile_dark", "images/rock_tile_dark.png", True),   # 9

    # 10–14: woda i warianty
    ("water", "images/water.png", True),                     # 10
    ("water_bright", "images/water_bright.png", True),       # 11
    ("water_dark", "images/water_dark.png", True),           # 12
    ("water_high_contrast", "images/water_high_contrast.png", True),  # 13

    # 15–18: drewno i warianty
    ("wood", "images/wood.png", False),                      # 14
    ("wood_red", "images/wood_red.png", False),              # 15
    ("wood_vibrant", "images/wood_vibrant.png", False),      # 16
    ("inny_wood", "images/inny_wood.png", False),            # 17

    # 19–21: ziemia i warianty
    ("dirt", "images/dirt.png", False),                      # 18
    ("dirt_dark", "images/dirt_dark.png", False),            # 19
    ("dirt_desaturated", "images/dirt_desaturated.png", False),  # 20

    # 22–25: inne naturalne elementy
    ("sand", "images/sand.png", False),                      # 21
    ("ice", "images/ice.png", False),                        # 22
    ("lava", "images/lava.png", False),                      # 23
    ("rock", "images/rock.png", True),                       # 24

    # 26–27: efekty specjalne
    ("grass_inverted", "images/grass_inverted.png", False),  # 25
    ("rock_tile_glow", "images/rock_tile_glow.png", True),   # 26

    # 28–33: obiekty interaktywne
    ("tree", "images/tree.png", True),                       # 27
    ("bow", "images/bow.png", True),                         # 28
    ("sword", "images/sword.png", True),                     # 29
    ("axe", "images/axe.png", True),                         # 30
    ("pickaxe", "images/pickaxe.png", True),                 # 31
    ("chest", "images/chest2.png", True),                    # 32
]

def main():
    pygame.init()
    screen_info = Info()

    editor = MapEditor(
        map_path = "game_map/maps_storage/map_23.map",

        tile_image_data=tile_image_data,
        tile_size=32,
        screen_width=screen_info.current_w,
        screen_height=screen_info.current_h
    )

    editor.run()

if __name__ == "__main__":
    main()
