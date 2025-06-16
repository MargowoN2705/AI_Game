import pygame
from .sprite import Sprite


class Item:
    def __init__(self, name, image_path, is_solid=False):
        self.name = name
        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert_alpha()
        #self.is_solid = is_solid
        # można dodać więcej atrybutów: damage, durability, rarity



class ItemEntity(Sprite):
    # klasa do wyswietlania itemow
    def __init__(self, item: Item, x, y, picked_up=False):
        super().__init__(item.image_path, x, y)
        self.item = item
        self.picked_up = picked_up
        self.rect = self.image.get_rect(topleft=(x, y))


class Inventory:
    def __init__(self, size=5):
        self.slots = [None] * size
        self.selected_index = 3 # aktualnie wybrany slot


    def add_item(self, item):

        # dodawanie do aktualnego slota
        if self.slots[self.selected_index] is None:
            self.slots[self.selected_index] = item
            return True

        # dodawanie do wolnego slota
        for i in range(len(self.slots)):
            if self.slots[i] is None:
                self.slots[i] = item
                return True

        return False  # brak miejsca


    def drop_item(self):
        dropped_item = self.slots[self.selected_index]
        self.slots[self.selected_index] = None
        return dropped_item
