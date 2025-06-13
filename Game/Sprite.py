import pygame

sprites = []
loaded = {}

class Sprite:
    def __init__(self, image, x, y):
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image).convert_alpha()
            loaded[image] = self.image

        self.x = x
        self.y = y

        sprites.append(self)

    def destroy(self):
        if self in sprites:
            sprites.remove(self)

    def draw(self, screen,camera):
        screen.blit(self.image, (self.x-camera.camera.x ,self.y-camera.camera.y))

