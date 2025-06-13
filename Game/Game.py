import pygame
from pygame import FULLSCREEN


class Game():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("GameAI")

        screen_info = pygame.display.Info()
        width, height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((width, height), FULLSCREEN)

        self.clear_color = (30, 150, 50)
        self.screen = screen
        self.Reset_Game()
        self.keys_down = set()

    def Reset_Game(self):
        pass

    def is_key_pressed(self,key):
        return key in self.keys_down

    def Run_Game(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                      self.keys_down.add(event.key)

                elif event.type == pygame.KEYUP:
                      self.keys_down.remove(event.key)

            self.screen.fill(self.clear_color)
            pygame.display.flip()

        pygame.quit()


game = Game()
game.Run_Game()