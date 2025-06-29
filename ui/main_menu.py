import pygame
import sys
from config import get_asset_path

def main_menu(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 48)
    small_font = pygame.font.SysFont("Arial", 32)

    # Kolory
    BG_COLOR = (30, 30, 30)
    TEXT_COLOR = (255, 255, 255)
    BUTTON_COLOR = (70, 70, 70)
    BUTTON_HOVER = (100, 100, 100)

    # Przyciski
    play_rect = pygame.Rect(300, 200, 200, 60)
    exit_rect = pygame.Rect(300, 300, 200, 60)

    while True:
        screen.fill(BG_COLOR)

        mx, my = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        # Play button
        if play_rect.collidepoint((mx, my)):
            pygame.draw.rect(screen, BUTTON_HOVER, play_rect)
            if click:
                return 'play'
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, play_rect)

        # Exit button
        if exit_rect.collidepoint((mx, my)):
            pygame.draw.rect(screen, BUTTON_HOVER, exit_rect)
            if click:
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, exit_rect)

        # Teksty
        play_text = small_font.render("Play", True, TEXT_COLOR)
        exit_text = small_font.render("Exit", True, TEXT_COLOR)
        title_text = font.render("My Game Title", True, TEXT_COLOR)

        screen.blit(title_text, (250, 100))
        screen.blit(play_text, (play_rect.x + 70, play_rect.y + 15))
        screen.blit(exit_text, (exit_rect.x + 70, exit_rect.y + 15))

        pygame.display.flip()
        clock.tick(60)
