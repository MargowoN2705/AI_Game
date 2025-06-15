class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def draw_item_entity(self, item_entity, tile_size):
        screen_x = item_entity.x * tile_size
        screen_y = item_entity.y * tile_size
        self.screen.blit(item_entity.image, (screen_x, screen_y))
