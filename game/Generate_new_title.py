import pygame
import os

class ImageProcessor:
    def __init__(self, grass_img, darkgrass_img, water_img, wood_img, dirt_img, rock_tile_img):
        self.grass_img = grass_img
        self.darkgrass_img = darkgrass_img
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

    def blend_surfaces(self, surface1, surface2, alpha):
        blended = surface1.copy()
        overlay = surface2.copy()
        overlay.set_alpha(int(alpha * 255))
        blended.blit(overlay, (0, 0))
        return blended

    def generate_grass_transition(self, images_folder="../images/", steps=5):
        for i in range(1, steps + 1):
            alpha = i / steps  # 0.2, 0.4, ..., 1.0
            blended = self.blend_surfaces(self.grass_img, self.darkgrass_img, alpha)
            filename = f"grass_dark_{i}.png"
            self.save_surface(blended, os.path.join(images_folder, filename))

        mid_blend = self.blend_surfaces(self.grass_img, self.darkgrass_img, 0.5)
        self.save_surface(mid_blend, os.path.join(images_folder, "grass_dark.png"))

    def proces_New_Image(self, images_folder="../images/"):
        grass_inverted = self.invert_colors(self.grass_img)
        water_high_contrast = self.change_contrast(self.water_img, 1.5)
        wood_vibrant = self.tint_image(self.wood_img, (220, 150, 100))
        dirt_desaturated = self.desaturate(self.dirt_img)
        rock_tile_glow = self.add_glow_effect(self.rock_tile_img, intensity=0.8)

        self.save_surface(grass_inverted, os.path.join(images_folder, "grass_inverted.png"))
        self.save_surface(water_high_contrast, os.path.join(images_folder, "water_high_contrast.png"))
        self.save_surface(wood_vibrant, os.path.join(images_folder, "wood_vibrant.png"))
        self.save_surface(dirt_desaturated, os.path.join(images_folder, "dirt_desaturated.png"))
        self.save_surface(rock_tile_glow, os.path.join(images_folder, "rock_tile_glow.png"))

        # NOWOŚĆ: generujemy przejścia trawy
        self.generate_grass_transition(images_folder)

    def invert_colors(self, image):
        inverted = image.copy()
        arr = pygame.surfarray.pixels3d(inverted)
        arr[:] = 255 - arr
        del arr
        return inverted

    def change_contrast(self, image, factor):
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
        glow = image.copy()
        glow = pygame.transform.smoothscale(glow, (glow.get_width() // 2, glow.get_height() // 2))
        glow = pygame.transform.smoothscale(glow, (image.get_width(), image.get_height()))
        glow.fill((int(255 * intensity), int(255 * intensity), int(255 * intensity), 128),
                  special_flags=pygame.BLEND_RGBA_ADD)
        result = image.copy()
        result.blit(glow, (0, 0))
        return result

    def darken_image(self, image, factor=0.5):
        dark_img = image.copy()
        dark_img.fill((int(255 * factor), int(255 * factor), int(255 * factor), 255), special_flags=pygame.BLEND_RGBA_MULT)
        return dark_img


pygame.init()
pygame.display.set_mode((1, 1))

grass_img = pygame.image.load("../images/grass.png").convert_alpha()

# Tworzymy ciemniejszą wersję trawy
procesor_temp = ImageProcessor(None, None, None, None, None, None)
darkgrass_img = procesor_temp.darken_image(grass_img, factor=0.5)

water_img = pygame.image.load("../images/water.png").convert_alpha()
wood_img = pygame.image.load("../images/wood.png").convert_alpha()
dirt_img = pygame.image.load("../images/dirt.png").convert_alpha()
rock_tile_img = pygame.image.load("../images/rock_tile.png").convert_alpha()

procesor = ImageProcessor(grass_img, darkgrass_img, water_img, wood_img, dirt_img, rock_tile_img)
procesor.proces_New_Image()
