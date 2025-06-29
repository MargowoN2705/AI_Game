import pygame
from game_map import Map,Tile
from game.camera import Camera

class MapEditor:
    def __init__(self, map_path, tile_image_data, tile_size, screen_width, screen_height):


        self.map_path = map_path
        self.tile_size = tile_size

        self.camera = Camera()
        self.camera.create_screen(screen_width, screen_height, "game_map Editor", 0)

        self.clock = pygame.time.Clock()


        self.tile_kinds = [Tile(name, path, solid) for name, path, solid in tile_image_data]

        self.selected_tile_index = 1
        self.game_map = Map(self.map_path, self.tile_kinds)
        self.center_camera_on_map()
        self.running = True

        self.brush_size = 3

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
        tilebar_y = self.camera.screen.get_height() - self.tile_size - 10

        if my >= tilebar_y:
            for i in range(len(self.tile_kinds)):
                x = i * (self.tile_size + 4) + 10
                if x <= mx <= x + self.tile_size:
                    self.selected_tile_index = i
                    print(f"[MapEditor] Wybrano kafelek: {self.tile_kinds[i].name}")
                    return True
        return False


    def handle_events(self):
        mouse_buttons = pygame.mouse.get_pressed()

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
                    width = 32
                    height = 32
                    self.create_empty_map(width, height)
                    print(f"[MapEditor] Stworzono nową mapę {width}x{height}")
                elif event.key == pygame.K_LEFTBRACKET:
                    self.brush_size = max(1, self.brush_size - 2)
                elif event.key == pygame.K_RIGHTBRACKET:
                    self.brush_size = min(15, self.brush_size + 2)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.check_tilebar_click():
                        return
                    self.place_tile()

            elif event.type == pygame.MOUSEWHEEL:
                self.camera.zoom += event.y * 0.1
                self.camera.zoom = max(0.5, min(self.camera.zoom, 3))  # ogranicz zoom od 0.5 do 3
                print(f"Zoom: {self.camera.zoom:.2f}")


        if mouse_buttons[0]:
            if not self.check_tilebar_click():
                self.place_tile()

        # Ruch kamery (strzałki lub WASD)
        keys = pygame.key.get_pressed()
        speed = 10 / self.camera.zoom  # żeby przesuwanie było bardziej naturalne przy zoomie


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

        # Skoryguj pozycję myszy o zoom i przesunięcie kamery
        tx = int((mx / self.camera.zoom + self.camera.camera.x) // self.tile_size)
        ty = int((my / self.camera.zoom + self.camera.camera.y) // self.tile_size)

        radius = self.brush_size // 2

        if 0 <= ty < len(self.game_map.raw_map_data) and 0 <= tx < len(self.game_map.raw_map_data[ty]):
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    xt = tx + dx
                    yt = ty + dy

                    if 0 <= yt < len(self.game_map.raw_map_data) and 0 <= xt < len(self.game_map.raw_map_data[yt]):
                        self.game_map.raw_map_data[yt][xt] = self.selected_tile_index
                        self.game_map.tiles[yt][xt] = self.tile_kinds[self.selected_tile_index]
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
        self.camera.screen.fill((0, 0, 0))
        self.game_map.draw(self.camera.screen, self.camera)


        self.camera.screen.blit(self.tile_kinds[self.selected_tile_index].image, (10, 10))


        for i, tile in enumerate(self.tile_kinds):
            x = i * (self.tile_size + 4) + 10
            y = self.camera.screen.get_height() - self.tile_size - 10
            self.camera.screen.blit(tile.image, (x, y))


            if i == self.selected_tile_index:
                pygame.draw.rect(self.camera.screen, (255, 255, 0), (x, y, self.tile_size, self.tile_size), 2)

        mx, my = pygame.mouse.get_pos()
        tx = int((mx / self.camera.zoom + self.camera.camera.x) // self.tile_size)
        ty = int((my / self.camera.zoom + self.camera.camera.y) // self.tile_size)

        half_brush = self.brush_size // 2

        for dy in range(-half_brush, half_brush + 1):
            for dx in range(-half_brush, half_brush + 1):
                bx = tx + dx
                by = ty + dy

                if 0 <= by < len(self.game_map.raw_map_data) and 0 <= bx < len(self.game_map.raw_map_data[0]):
                    screen_x = (bx * self.tile_size - self.camera.camera.x) * self.camera.zoom
                    screen_y = (by * self.tile_size - self.camera.camera.y) * self.camera.zoom
                    rect = pygame.Rect(screen_x, screen_y, self.tile_size * self.camera.zoom,
                                       self.tile_size * self.camera.zoom)
                    pygame.draw.rect(self.camera.screen, (255, 255, 0), rect, 1)  # żółty kontur



