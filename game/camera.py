import pygame
from config import CAMERA_ZOOM

class Camera:

    def __init__(self):
        self.camera = pygame.Rect(0, 0, 0, 0)
        self.zoom = CAMERA_ZOOM
        self.width = 0
        self.height = 0

    def create_screen(self, width, height, title, mode):
        pygame.display.set_caption(title)
        screen = pygame.display.set_mode((width, height), mode)
        self.width = width
        self.height = height
        self.camera.width = width
        self.camera.height = height
        return screen

    def apply(self, pos):
        x, y = pos
        return (int((x - self.camera.x) * self.zoom), int((y - self.camera.y) * self.zoom))

    def apply_surface(self, surface):
        w = int(surface.get_width() * self.zoom)
        h = int(surface.get_height() * self.zoom)
        return pygame.transform.scale(surface, (w, h))

    def follow(self, target):
        self.target = target

    def update(self):
        if self.target:
            # Przesuwanie kamery wzgledem target
            self.camera.x = int(self.target.x - (self.camera.width / self.zoom) / 2)
            self.camera.y = int(self.target.y - (self.camera.height / self.zoom) / 2)


    def get_visible_tile_range(self, tile_size, map_width_tiles, map_height_tiles):
        # oblicz granice widocznego prostokąta w koordynatach pikselowych mapy
        visible_left = self.camera.x
        visible_top = self.camera.y
        visible_right = self.camera.x + self.camera.width / self.zoom
        visible_bottom = self.camera.y + self.camera.height / self.zoom

        # zmiana na indeksy kafelków
        start_x = max(0, int(visible_left // tile_size))
        end_x = min(map_width_tiles, int(visible_right // tile_size) + 1)
        start_y = max(0, int(visible_top // tile_size))
        end_y = min(map_height_tiles, int(visible_bottom // tile_size) + 1)

        return start_x, end_x, start_y, end_y

