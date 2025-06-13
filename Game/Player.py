import pygame
from Sprite import Sprite
from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Player(Sprite):
    def __init__(self, image, x, y, a):
        super().__init__(image, x, y)

        self.VEL_X = 0
        self.VEL_Y = 0
        self.ACC = a
        self.FRICTION = 0.45
        self.MAX_VEL = 7.5

        self.keys_down = set()
        self.DIR = Direction.RIGHT

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
        new_x = self.x + dx
        new_y = self.y + dy
        return new_x, new_y

    def Update(self):
        self.x, self.y = self.get_Position()
