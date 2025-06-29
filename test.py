import pygame
from game.game import Game
import sys
from ui.main_menu import main_menu
from game.camera import Camera


# wszystko polaczone do jednego ui - kreator map, gra, ustawienia itp itd

def main():
    pygame.init()
    camera = Camera()
    camera.create_screen(500, 600, "xd", pygame.RESIZABLE)

    state = "menu"  # <- TU ustalasz początkowy stan gry



    while True:
        if state == "menu":
            result = main_menu(camera.screen)
            if result == "play":
                state = "game"
            elif result == "settings":
                state = "settings"
            elif result == "exit":
                pygame.quit()
                sys.exit()

        elif state == "game":
            game = Game()
            game.run_game()
            state = "menu"


if __name__ == "__main__":
    main()