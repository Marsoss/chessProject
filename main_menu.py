from chess_board_view import ChessBoardView
from board import Board
from chess_rules import Referee
from chess_board_presenter import ChessBoardPresenter
from chess_timer import Timer
from game_mode import GameMode, PlayerVsComputer, PlayerVsPlayerWTimer, ComputerVsComputer
from chess_AI import ChessAI
import pygame

# TODO: add remove last move from game notation
# TODO: add game reader
# TODO: add menu screen
# TODO: add reader/writer fen format

from pygame_extension.menu import Menu
from pygame_extension.button import Button

def main_menu(screen):
    options = [
        "Joueur contre Joueur",
        "Joueur contre Ordinateur",
        "Ordinateur contre Ordinateur"
    ]

    functions = [
        cadence_menu,
        pve_game,
        ai_game
    ]
    menu = Menu(screen, options, functions, back_function=None, title="Menu Principal", button_size=(420,60))
    return menu.run()

def pve_game(*args):
    print("PVE!")

def ai_game(*args):
    print("AI game!")

def cadence_menu(screen):
    options = [
        "Bullet",
        "Blitz",
        "Rapide",
        "Longue",
        "Illimité",
        "Personnaliser"
    ]
    functions = [
        bullet_game,
        blitz3_game,
        rapid_game,
        long_game,
        unlimited_game,
        custom_game
    ]
    menu = Menu(screen, options, functions, back_function=main_menu, title="Choix de la Cadence")
    return menu.run()

def unlimited_game(*args):
    board = Board([[None for _ in range(8)] for _ in range(8)])
    board.start_classic_setup()
    referee = Referee(board)
    view = ChessBoardView()
    presenter = ChessBoardPresenter(view, referee)
    presenter.start_game()

def custom_game(start_time, increment):
    board = Board([[None for _ in range(8)] for _ in range(8)])
    board.start_classic_setup()
    white_timer = Timer(start_time, increment)
    black_timer = Timer(start_time, increment)
    referee = Referee(board, white_timer=white_timer, black_timer=black_timer)
    view = ChessBoardView()
    presenter = ChessBoardPresenter(view, referee)
    presenter.start_game()

def long_game(*args):
    custom_game(90*60, 30)

def rapid_game(*args):
    custom_game(30*60, 10)

def blitz10_game(*args):
    custom_game(10*60, 10)

def blitz3_game(*args):
    custom_game(3*60, 3)

def bullet_game(*args):
    custom_game(60, 1)

if __name__ == '__main__':
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menu du Jeu d'échecs")
    main_menu(screen)
