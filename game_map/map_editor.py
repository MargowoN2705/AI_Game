import pygame
from game_map import Map,Tile
from game.camera import Camera

class MapEditor:
    def __init__(self, map_path, tile_image_data, tile_size, screen_width, screen_height):


        self.map_path = map_path
        self.tile_size = tile_size

        self.camera = Camera()
        self.screen = self.camera.create_screen(screen_width, screen_height, "game_map Editor", 0)
        self.clock = pygame.time.Clock()


        self.tile_kinds = [Tile(name, path, solid) for name, path, solid in tile_image_data]

        self.selected_tile_index = 1
        self.game_map = Map(self.map_path, self.tile_kinds, self.tile_size)
        self.center_camera_on_map()
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.draw()
            pygame.display.flip()

        pygame.quit()

    def create_empty_map(self, width, height):
        self.game_map.raw_map_data = [[0 for _ in range(width)] for _ in range(height)]
        self.game_map.tiles = [[self.tile_kinds[0] for _ in range(width)] for _ in range(height)]

    def center_camera_on_map(self):
        map_width_px = len(self.game_map.raw_map_data[0]) * self.tile_size
        map_height_px = len(self.game_map.raw_map_data) * self.tile_size

        self.camera.camera.x = max(0, map_width_px // 2 - self.camera.camera.width // 2)
        self.camera.camera.y = max(0, map_height_px // 2 - self.camera.camera.height // 2)

    def check_tilebar_click(self):
        mx, my = pygame.mouse.get_pos()
        tilebar_y = self.screen.get_height() - self.tile_size - 10

        if my >= tilebar_y:
            for i in range(len(self.tile_kinds)):
                x = i * (self.tile_size + 4) + 10
                if x <= mx <= x + self.tile_size:
                    self.selected_tile_index = i
                    print(f"[MapEditor] Wybrano kafelek: {self.tile_kinds[i].name}")
                    return True
        return False


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if pygame.K_0 <= event.key <= pygame.K_9:
                    self.selected_tile_index = min(event.key - pygame.K_0, len(self.tile_kinds) - 1)

                elif event.key == pygame.K_s:
                    self.save_map()
                elif event.key == pygame.K_l:
                    self.load_map_data_from_file(self.map_path)
                elif event.key == pygame.K_n:
                    width = 100
                    height = 80
                    self.create_empty_map(width, height)
                    print(f"[MapEditor] Stworzono nową mapę {width}x{height}")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.check_tilebar_click():
                        return
                    self.place_tile()

        # Ruch kamery (strzałki lub WASD)
        keys = pygame.key.get_pressed()
        speed = 10

        # Obliczamy maksymalne przesunięcie, żeby kamera nie wyszła poza mapę
        map_width_px = len(self.game_map.raw_map_data[0]) * self.tile_size
        map_height_px = len(self.game_map.raw_map_data) * self.tile_size

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.camera.camera.x = max(0, self.camera.camera.x - speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.camera.camera.x = min(map_width_px - self.camera.camera.width, self.camera.camera.x + speed)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.camera.camera.y = max(0, self.camera.camera.y - speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.camera.camera.y = min(map_height_px - self.camera.camera.height, self.camera.camera.y + speed)

    def place_tile(self):
        mx, my = pygame.mouse.get_pos()
        tx = (mx + self.camera.camera.x) // self.tile_size
        ty = (my + self.camera.camera.y) // self.tile_size


        if 0 <= ty < len(self.game_map.raw_map_data) and 0 <= tx < len(self.game_map.raw_map_data[ty]):
            self.game_map.raw_map_data[ty][tx] = self.selected_tile_index
            self.game_map.tiles[ty][tx] = self.tile_kinds[self.selected_tile_index]
        else:
            print(f"[MapEditor] Kliknięto poza mapą: tx={tx}, ty={ty}")

    def save_map(self):
        with open(self.map_path, "w") as f:
            for row in self.game_map.raw_map_data:
                line = " ".join(str(cell) for cell in row)
                f.write(line + "\n")
        print("[MapEditor] Mapa zapisana.")

    def load_map_data_from_file(self, path):
        with open(path, "r") as f:
            raw_map_data = []
            for line in f:
                row = [int(x) for x in line.strip().split()]
                raw_map_data.append(row)
        return raw_map_data

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.game_map.draw(self.screen, self.camera)


        self.screen.blit(self.tile_kinds[self.selected_tile_index].image, (10, 10))


        for i, tile in enumerate(self.tile_kinds):
            x = i * (self.tile_size + 4) + 10
            y = self.screen.get_height() - self.tile_size - 10
            self.screen.blit(tile.image, (x, y))


            if i == self.selected_tile_index:
                pygame.draw.rect(self.screen, (255, 255, 0), (x, y, self.tile_size, self.tile_size), 2)

tile_image_data = [
    # 0–9: podstawowe podłoża i warianty
    ("grass", "../images/grass.png", False),                    # 0
    ("grass_dark", "../images/grass_dark.png", False),          # 1
    ("grass_bright", "../images/grass_bright.png", False),      # 2
    ("grass_dark_1", "../images/grass_dark_1.png", False),      # 3
    ("grass_dark_2", "../images/grass_dark_2.png", False),      # 4
    ("grass_dark_3", "../images/grass_dark_3.png", False),      # 5
    ("grass_dark_4", "../images/grass_dark_4.png", False),      # 6
    ("grass_dark_5", "../images/grass_dark_5.png", False),      # 7
    ("rock_tile", "../images/rock_tile.png", True),             # 8
    ("rock_tile_dark", "../images/rock_tile_dark.png", True),   # 9

    # 10–14: woda i warianty
    ("water", "../images/water.png", True),                     # 10
    ("water_bright", "../images/water_bright.png", True),       # 11
    ("water_dark", "../images/water_dark.png", True),           # 12
    ("water_high_contrast", "../images/water_high_contrast.png", True),  # 13

    # 15–18: drewno i warianty
    ("wood", "../images/wood.png", False),                      # 14
    ("wood_red", "../images/wood_red.png", False),              # 15
    ("wood_vibrant", "../images/wood_vibrant.png", False),      # 16
    ("inny_wood", "../images/inny_wood.png", False),            # 17

    # 19–21: ziemia i warianty
    ("dirt", "../images/dirt.png", False),                      # 18
    ("dirt_dark", "../images/dirt_dark.png", False),            # 19
    ("dirt_desaturated", "../images/dirt_desaturated.png", False),  # 20

    # 22–25: inne naturalne elementy
    ("sand", "../images/sand.png", False),                      # 21
    ("ice", "../images/ice.png", False),                        # 22
    ("lava", "../images/lava.png", False),                      # 23
    ("rock", "../images/rock.png", True),                       # 24

    # 26–27: efekty specjalne
    ("grass_inverted", "../images/grass_inverted.png", False),  # 25
    ("rock_tile_glow", "../images/rock_tile_glow.png", True),   # 26

    # 28–33: obiekty interaktywne
    ("tree", "../images/tree.png", True),                       # 27
    ("bow", "../images/bow.png", True),                         # 28
    ("sword", "../images/sword.png", True),                     # 29
    ("axe", "../images/axe.png", True),                         # 30
    ("pickaxe", "../images/pickaxe.png", True),                 # 31
    ("chest", "../images/chest2.png", True),                    # 32
]


pygame.init()
screen_info = pygame.display.Info()

editor = MapEditor(
    map_path="maps_storage/map_1.map",
    tile_image_data=tile_image_data,
    tile_size=32,
    screen_width=screen_info.current_w,
    screen_height=screen_info.current_h
)

editor.run()



