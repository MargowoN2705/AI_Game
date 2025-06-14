import pygame

class ImageProcessor:
    def __init__(self, grass_img, water_img, wood_img, dirt_img, rock_tile_img):
        self.grass_img = grass_img
        self.water_img = water_img
        self.wood_img = wood_img
        self.dirt_img = dirt_img
        self.rock_tile_img = rock_tile_img

    def tint_image(self, image, tint_color):
        tinted_image = image.copy()
        tinted_image.fill(tint_color + (255,), special_flags=pygame.BLEND_RGBA_MULT)
        return tinted_image

    def change_brightness(self, image, factor):
        bright_image = image.copy()
        brightness_value = int(factor * 255)
        brightness_value = max(0, min(255, brightness_value))
        bright_image.fill((brightness_value, brightness_value, brightness_value, 255),
                          special_flags=pygame.BLEND_RGBA_MULT)
        return bright_image

    def save_surface(self, surface, filename):
        pygame.image.save(surface, filename)
        print(f"Saved image to {filename}")


    def proces_New_Image(self,images_folder="../images/"):

        grass_inverted = self.invert_colors(self.grass_img)  # odwrócone kolory trawy
        water_high_contrast = self.change_contrast(self.water_img, 1.5)  # wysoki kontrast wody
        wood_vibrant = self.tint_image(self.wood_img, (220, 150, 100))  # bardziej intensywny odcień drewna
        dirt_desaturated = self.desaturate(self.dirt_img)  # odcienie szarości ziemi
        rock_tile_glow = self.add_glow_effect(self.rock_tile_img, intensity=0.8)  # efekt "poświaty" na kamieniu

        self.save_surface(grass_inverted, images_folder + "grass_inverted.png")
        self.save_surface(water_high_contrast, images_folder + "water_high_contrast.png")
        self.save_surface(wood_vibrant, images_folder + "wood_vibrant.png")
        self.save_surface(dirt_desaturated, images_folder + "dirt_desaturated.png")
        self.save_surface(rock_tile_glow, images_folder + "rock_tile_glow.png")

    def invert_colors(self, image):
        inverted = image.copy()
        arr = pygame.surfarray.pixels3d(inverted)
        arr[:] = 255 - arr
        del arr
        return inverted

    def change_contrast(self, image, factor):
        # Prosta zmiana kontrastu
        contrast_img = image.copy()
        arr = pygame.surfarray.pixels3d(contrast_img)
        mean = arr.mean(axis=(0, 1), keepdims=True)
        arr[:] = pygame.surfarray.array3d(image) * factor + mean * (1 - factor)
        arr[:] = arr.clip(0, 255)
        del arr
        return contrast_img

    def desaturate(self, image):
        desat_img = image.copy()
        arr = pygame.surfarray.pixels3d(desat_img)
        gray = arr.mean(axis=2, keepdims=True).astype(arr.dtype)
        arr[:] = gray
        del arr
        return desat_img

    def add_glow_effect(self, image, intensity=0.5):
        # Prosty glow: nakładamy rozmytą kopię na oryginał
        glow = image.copy()
        glow = pygame.transform.smoothscale(glow, (glow.get_width() // 2, glow.get_height() // 2))
        glow = pygame.transform.smoothscale(glow, (image.get_width(), image.get_height()))
        glow.fill((int(255 * intensity), int(255 * intensity), int(255 * intensity), 128),
                  special_flags=pygame.BLEND_RGBA_ADD)
        result = image.copy()
        result.blit(glow, (0, 0))
        return result



pygame.init()
pygame.display.set_mode((1, 1))  # Minimalne okno, potrzebne dla convert_alpha()

grass_img = pygame.image.load("../images/grass.png").convert_alpha()
water_img = pygame.image.load("../images/water.png").convert_alpha()
wood_img = pygame.image.load("../images/wood.png").convert_alpha()
dirt_img = pygame.image.load("../images/dirt.png").convert_alpha()
rock_tile_img = pygame.image.load("../images/rock_tile.png").convert_alpha()

procesor = ImageProcessor(grass_img, water_img, wood_img, dirt_img, rock_tile_img)
procesor.proces_New_Image()