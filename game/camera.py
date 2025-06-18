import pygame
from config import CAMERA_ZOOM

class Camera:

    def __init__(self):
        self.camera = pygame.Rect(0, 0, 0, 0)
        self.zoom = CAMERA_ZOOM

    def create_screen(self, width, height, title, mode):
        pygame.display.set_caption(title)
        screen = pygame.display.set_mode((width, height), mode)
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