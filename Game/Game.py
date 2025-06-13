import pygame
from pygame import FULLSCREEN

from Player import Player
from Sprite import sprites


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("GameAI")

        screen_info = pygame.display.Info()
        width, height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((width, height), FULLSCREEN)

        self.clear_color = (30, 150, 50)
        self.screen = screen
        self.keys_down = set()
        self.GAME_SPEED = 60

        self.player = Player("../Images/player.png", 100, 100, a=0.3)

        self.Reset_Game()

    def Reset_Game(self):
        pass



    def is_key_pressed(self, key):
        return key in self.keys_down

    def Run_Game(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(self.GAME_SPEED)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    self.keys_down.add(event.key)
                    self.player.handle_key_down(event.key)

                elif event.type == pygame.KEYUP:
                    self.keys_down.discard(event.key)
                    self.player.handle_key_up(event.key)

            self.player.Update()
            self.screen.fill(self.clear_color)


            for s in sprites:
                s.draw(self.screen)

            pygame.display.flip()

        pygame.quit()


game = Game()
game.Run_Game()
