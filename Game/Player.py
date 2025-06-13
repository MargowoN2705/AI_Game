import pygame
from Sprite import Sprite
from enum import Enum


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Player(Sprite):
    def __init__(self, image, x, y, a, game_map):
        super().__init__(image, x, y)

        self.VEL_X = 0
        self.VEL_Y = 0
        self.ACC = a
        self.FRICTION = 0.2
        self.MAX_VEL = 4
        self.game_map = game_map
        self.keys_down = set()
        self.DIR = Direction.RIGHT
        self.player_rect = pygame.Rect(int(self.x), int(self.y), 16, 32)
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

    def get_Movement(self):
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

        return self.VEL_X, self.VEL_Y

    def get_Position(self):
        dx, dy = self.get_Movement()


        new_rect = self.player_rect.move(dx, dy)

        collision = False
        for y, row in enumerate(self.game_map.tiles):
            for x, tile in enumerate(row):
                if tile.is_solid:
                    tile_rect = pygame.Rect(x * self.game_map.tile_size, y * self.game_map.tile_size,
                                            self.game_map.tile_size, self.game_map.tile_size)
                    if new_rect.colliderect(tile_rect):
                        collision = True
                        break
            if collision:
                break

        if not collision:
            return self.x + dx, self.y + dy
        else:
            return self.x, self.y

    def Update(self, camera):
        self.x, self.y = self.get_Position()
        self.player_rect.topleft = (int(self.x), int(self.y))
        camera.camera.x = self.x - camera.camera.width / 2
        camera.camera.y = self.y - camera.camera.height / 2




