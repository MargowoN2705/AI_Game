import pygame

sprites = []
loaded = {}

class Sprite:
    def __init__(self, image, x, y, offset_y=0):
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image).convert_alpha()
            loaded[image] = self.image

        self.x = x
        self.y = y
        self.offset_y = offset_y

        sprites.append(self)


    def destroy(self):
        if self in sprites:
            sprites.remove(self)

    def draw(self, screen, camera):
        pos = (self.x, self.y - self.offset_y)
        pos = camera.apply(pos)  # przesuwamy i skalujemy pozycję

        scaled_image = camera.apply_surface(self.image)  # skalujemy obrazek

        screen.blit(scaled_image, pos)

    def change_image(self, new_image_path):
        self.image = pygame.image.load(new_image_path).convert_alpha()



