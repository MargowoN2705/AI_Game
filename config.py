import os

# 'Elastyczna' sciezka do pliku

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_asset_path(*parts, own_path=False):
    if own_path: return os.path.join(BASE_DIR, *parts)
    return os.path.join(BASE_DIR, "images", *parts)


# Gracz/bot

PLAYER_CONFIG = {
    "ACC": 3,
    "FRICTION": 1,
    "MAX_VEL": 5,
    "MAX_HP": 100,
    "MAX_MP": 100,
}

INVENTORY_SIZE = 5
DEFAULT_SELECTED_SLOT = 1


# Widok

CAMERA_ZOOM = 1.5 # stały zoom, 1.5 = 150% powiększenia
TILE_SIZE = 32


# Gra

GAME_CONFIG = {
    "clear_color": (0, 0, 0),
    "game_speed": 60,
    #"fullscreen": True,
    "game_map": get_asset_path("game_map", "maps_storage", "map_1.map", own_path=True),
    #"game_map": get_asset_path("game_map", "maps_storage", "simple_map.map", own_path=True),
    "title": "GameAI",
    #"bush_spawn_chance": 0.15,
    #"zoom_step": 0.25,
    #"zoom_max": 4.0,
    #"zoom_min": 0.25,
}

TILE_KINDS = [
    # 0–9: podstawowe podłoża i warianty
    {"name": "grass", "solid": False},          # 0
    {"name": "grass_dark", "solid": False},     # 1
    {"name": "grass_bright", "solid": False},   # 2
    {"name": "grass_dark_1", "solid": False},   # 3
    {"name": "grass_dark_2", "solid": False},   # 4
    {"name": "grass_dark_3", "solid": False},   # 5
    {"name": "grass_dark_4", "solid": False},   # 6
    {"name": "grass_dark_5", "solid": False},   # 7
    {"name": "rock_tile", "solid": True},       # 8
    {"name": "rock_tile_dark", "solid": True},  # 9

    # 10–13: woda i warianty
    {"name": "water", "solid": True},           # 10
    {"name": "water_bright", "solid": True},    # 11
    {"name": "water_dark", "solid": True},      # 12
    {"name": "water_high_contrast", "solid": True},     # 13

    # 15–17: drewno i warianty
    {"name": "wood", "solid": False},           # 14
    {"name": "wood_red", "solid": False},       # 15
    {"name": "wood_vibrant", "solid": False},   # 16
    {"name": "inny_wood", "solid": False},      # 17

    # 18–19: ziemia i warianty
    {"name": "dirt", "solid": False},           # 18
    {"name": "dirt_dark", "solid": False},      # 19
    {"name": "dirt_desaturated", "solid": False},       # 20

    # 21–24: inne naturalne elementy
    {"name": "sand", "solid": False},           # 21
    {"name": "ice", "solid": False},            # 22
    {"name": "lava", "solid": False},           # 23
    {"name": "rock", "solid": False},           # 24

    # 25–28: efekty specjalne
    {"name": "grass_inverted", "solid": False}, # 25
    {"name": "rock_tile_glow", "solid": True},  # 26
    {"name": "grass", "solid": False},          # 27
    {"name": "grass", "solid": False},           # 28

    # tymczasowe
    {"name": "grass", "solid": False},  # 28
    {"name": "grass", "solid": False},  # 28
    {"name": "grass", "solid": False},  # 28
    {"name": "grass", "solid": False},  # 28
    {"name": "grass", "solid": False},  # 28
    {"name": "grass", "solid": False}  # 28
]
'''??????????????????????????????????????????????????????????????????????????????????????
            # 29–33: obiekty interaktywne
            Tile("tree<-----------------------", get_asset_path("grass_dark.png"<-----------?????????), True),  # 27
            Tile("bow", get_asset_path("grass.png"), True),  # 28
            Tile("sword", get_asset_path("grass.png"), True),  # 29
            Tile("axe", get_asset_path("grass_dark.png"), True),  # 30
            Tile("pickaxe", get_asset_path("grass_dark.png"), True),  # 31
            Tile("chest", get_asset_path("chest2.png"), True),  # 32
        '''