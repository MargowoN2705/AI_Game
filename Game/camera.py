import pygame

class Camera:

    def __init__(self):
        self.camera = pygame.Rect(0, 0, 0, 0)

    def create_screen(self, width, height, title,mode):
        pygame.display.set_caption(title)
        screen = pygame.display.set_mode((width, height),mode)
        self.camera.width = width
        self.camera.height = height
        return screen
