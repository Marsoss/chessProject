from main_menu import main_menu
import pygame

# TODO: add remove last move from game notation
# TODO: add game reader
# TODO: add menu screen
# TODO: add reader/writer fen format

if __name__ == '__main__':
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menu du Jeu d'échecs")
    main_menu(screen)
