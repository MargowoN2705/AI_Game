import pygame

class Item:
    def __init__(self, name, image_path, is_solid=False):
        self.name = name
        self.image = pygame.image.load(image_path).convert_alpha()
        self.is_solid = is_solid
        self.image = pygame.image.load(image_path).convert_alpha()
        # można dodać więcej atrybutów: damage, durability, rarity


class ItemEntity:
    def __init__(self, item, position):
        self.item = item  # referencja do Item
        self.position = position  # np. (x, y)
        self.picked_up = False