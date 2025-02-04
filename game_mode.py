from board import Board
from chess_rules import Referee
from chess_AI import ChessAI
from chess_timer import Timer

from abc import ABC, abstractmethod

class GameMode(ABC):
    def __init__(self, presenter):
        self.presenter = presenter
        self.referee = self.presenter.referee

    @abstractmethod
    def play_turn(self):
        """Define how each turn should be played in the specific game mode."""
        pass


class PlayerVsPlayerWTimer(GameMode):
    def __init__(self, presenter, white_timer:Timer, black_timer:Timer):
        super().__init__(presenter)
        self.presenter.referee.white_timer = white_timer
        self.presenter.referee.black_timer = black_timer

    def play_turn(self):

        # Process player move
        self.presenter.view.handle_events()

    def _manage_timer(self, current_player):
        if current_player=='white':
            if self.turn_count < 3:
                self.black_timer.start()
            else:
                self.white_timer.pause()
                self.black_timer.resume()

        else:
            self.black_timer.pause()
            if self.turn_count < 3:
                self.white_timer.start()
            else:
                self.white_timer.resume()


class PlayerVsComputer(GameMode):
    def __init__(self, presenter, ai:ChessAI):
        super().__init__(presenter)
        self.ai = ai

    def play_turn(self):
        current_player = self.board.get_current_player()

        if current_player != self.ai.color:
            self.presenter.view.handle_events()
        else:
            # AI move for computer player
            ai_move = self.ai.find_best_move(depth=3)
            self.referee.make_move(ai_move[0], ai_move[1])


class ComputerVsComputer(GameMode):
    def __init__(self, presenter, ai_white, ai_black):
        super().__init__(presenter)
        self.ai_white = ai_white
        self.ai_black = ai_black

    def play_turn(self):
        current_player = self.board.get_current_player()

        if current_player == 'white':
            ai_move = self.ai_white.find_best_move(depth=3)
        else:
            ai_move = self.ai_black.find_best_move(depth=3)

        self.referee.make_move(ai_move[0], ai_move[1])
