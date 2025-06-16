import pygame
from .sprite import Sprite
from enum import Enum
from .item import Inventory


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Player(Sprite):
    def __init__(self, image, x, y, a, game_map):
        super().__init__(image, x, y,offset_y=32)

        self.VEL_X = 0
        self.VEL_Y = 0
        self.ACC = 5
        self.FRICTION = 1
        self.MAX_VEL = 5
        self.game_map = game_map
        self.keys_down = set()
        self.DIR = Direction.RIGHT
        self.rect = pygame.Rect(int(self.x), int(self.y), 25, 25)
        self.inventory = Inventory()

        #for Animation
        self.sprite_sheet = pygame.image.load(image).convert_alpha()
        self.frame_width = 32
        self.frame_height = 32
        self.animation_row = 2
        self.frame_count = 10
        self.current_frame = 0
        self.animation_speed = 0.15
        self.frame_timer = 0
        self.moving = False

    def is_key_pressed(self, key):
        return key in self.keys_down

    def handle_key_down(self, key):
        self.keys_down.add(key)

    def handle_key_up(self, key):
        self.keys_down.discard(key)

    def apply_friction(self):

        if not (self.is_key_pressed(pygame.K_a) or self.is_key_pressed(pygame.K_d)):
            if abs(self.VEL_X) < self.FRICTION:
                self.VEL_X = 0
            else:
                self.VEL_X -= self.FRICTION * (1 if self.VEL_X > 0 else -1)


        if not (self.is_key_pressed(pygame.K_w) or self.is_key_pressed(pygame.K_s)):
            if abs(self.VEL_Y) < self.FRICTION:
                self.VEL_Y = 0
            else:
                self.VEL_Y -= self.FRICTION * (1 if self.VEL_Y > 0 else -1)

    def clamp_velocity(self):
        self.VEL_X = max(-self.MAX_VEL, min(self.VEL_X, self.MAX_VEL))
        self.VEL_Y = max(-self.MAX_VEL, min(self.VEL_Y, self.MAX_VEL))

    def get_movement(self):
        acc = self.ACC

        if self.is_key_pressed(pygame.K_w):
            self.VEL_Y -= acc
            self.DIR = Direction.UP
        if self.is_key_pressed(pygame.K_s):
            self.VEL_Y += acc
            self.DIR = Direction.DOWN
        if self.is_key_pressed(pygame.K_a):
            self.VEL_X -= acc
            self.DIR = Direction.LEFT
        if self.is_key_pressed(pygame.K_d):
            self.VEL_X += acc
            self.DIR = Direction.RIGHT

        self.apply_friction()
        self.clamp_velocity()

        # Ustawiamy flagę czy się ruszamy (potrzebne do animacji)
        self.moving = (self.VEL_X != 0 or self.VEL_Y != 0)

        return self.VEL_X, self.VEL_Y

    def get_position(self):
        dx, dy = self.get_movement()

        # --- KOLIZJA OSOBNO DLA X ---
        new_x = self.x + dx
        new_rect_x = self.rect.copy()
        new_rect_x.x = int(new_x)

        collision_x = False
        for y, row in enumerate(self.game_map.tiles):
            for x_, tile in enumerate(row):
                if tile.is_solid:
                    tile_rect = pygame.Rect(x_ * self.game_map.tile_size, y * self.game_map.tile_size,
                                            self.game_map.tile_size, self.game_map.tile_size)
                    if new_rect_x.colliderect(tile_rect):
                        collision_x = True
                        break
            if collision_x:
                break

        if not collision_x:
            self.x = new_x

        # --- KOLIZJA OSOBNO DLA Y ---
        new_y = self.y + dy
        new_rect_y = self.rect.copy()
        new_rect_y.y = int(new_y)

        collision_y = False
        for y, row in enumerate(self.game_map.tiles):
            for x_, tile in enumerate(row):
                if tile.is_solid:
                    tile_rect = pygame.Rect(x_ * self.game_map.tile_size, y * self.game_map.tile_size,
                                            self.game_map.tile_size, self.game_map.tile_size)
                    if new_rect_y.colliderect(tile_rect):
                        collision_y = True
                        break
            if collision_y:
                break

        if not collision_y:
            self.y = new_y

        # Zaktualizuj rect
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        return self.x, self.y

    def update_animation(self, dt):
        if self.moving:
            self.frame_timer += dt
            if self.frame_timer >= self.animation_speed:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % self.frame_count
        else:
            self.current_frame = 0

    def draw(self, surface, camera):
        frame_rect = pygame.Rect(
            self.current_frame * self.frame_width,
            self.animation_row * self.frame_height,
            self.frame_width,
            self.frame_height
        )
        frame_image = self.sprite_sheet.subsurface(frame_rect)

        if self.DIR == Direction.LEFT:
            frame_image = pygame.transform.flip(frame_image, True, False)

        # Skalowanie obrazka
        frame_image = camera.apply_surface(frame_image)

        # Pozycja na ekranie z uwzględnieniem kamery i zoomu
        screen_pos = camera.apply((self.x, self.y))

        surface.blit(frame_image, screen_pos)

    def update(self, camera, dt):
        self.x, self.y = self.get_position()
        self.rect.topleft = (int(self.x), int(self.y))
        camera.camera.x = self.x - (camera.camera.width / camera.zoom) / 2
        camera.camera.y = self.y - (camera.camera.height / camera.zoom) / 2

        self.update_animation(dt)





