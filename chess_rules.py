from board import Board
from chess_timer import Timer
from board_tracker import BoardTracker
from chess_AI import ChessAI
from chess_typing import Color, Square, Move

white_timer = Timer(3*60,2)
black_timer = Timer(3*60,2)

class Referee:
    def __init__(self, board: Board, start_player="white", white_timer:Timer=None, black_timer:Timer=None):
        self.board = board.copy()
        self.start_player = start_player
        self.turn_count = 1
        self.state = "ongoing"
        # Initialize timers for both players (in seconds, e.g., 3 minutes and 2s increment)
        self.white_timer = white_timer
        self.black_timer = black_timer
        # Initialize the board tracker
        self.board_tracker = BoardTracker(self)

    def reset(self):
        """Reset the board positions to the first move"""
        self.board.reset()
        self.state = "ongoing"
        self.turn_count = 1
        if self.white_timer is not None:
            self.black_timer.reset()
            self.white_timer.reset()
        self.board_tracker.reset()

    def current_player(self):
        return self.start_player if self.turn_count % 2 == 1 else self.board.get_opponent_color(self.start_player)

    def is_checkmate(self, color) -> bool:
        """Check if the current player is in checkmate."""
        if not self.board.is_in_check(color):
            return False
        return not self.can_legal_move_be_made(color)

    def can_legal_move_be_made(self, color) -> bool:
        """Check if any legal moves can be made by the current player."""
        return len(self.board.get_all_moves(color))>0

    def switch_player(self):
        """Switch to the next player and manage the timers."""
        
        self.manage_timers()
        # Switch player and increment the turn count
        self.turn_count += 1

    def manage_timers(self):
        if self.white_timer is not None:
            if self.current_player()=='white':
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

    def check_timers(self):
        """Check if any player's time has run out."""
        if self.white_timer is not None and self.state == "ongoing":
            if self.white_timer.times_up:
                self.state = "timesup"
                print("White ran out of time. Black wins!")
            elif self.black_timer.times_up:
                self.state = "timesup"
                print("Black ran out of time. White wins!")

    def update_game_state(self):
        """Update the game state after each move."""
        if self.state == "ongoing" and not self.can_legal_move_be_made(self.current_player()):
            print(f"Legal Move for {self.current_player()}? {self.can_legal_move_be_made(self.current_player())}")
            self.state = "stalemate"
            print("It's a stalemate!")
        elif self.state == "ongoing" and self.is_checkmate(self.current_player()):
            self.state = "checkmate"
            print(f"{self.board.get_opponent_color(self.current_player())} wins by checkmate!")
    

    def make_move(self, from_pos, to_pos):
        """Make a move, check for legalities, and update the game state."""
        if self.board.move_piece(from_pos, to_pos):
            if self.state == "ongoing":
                self.switch_player()
                self.board_tracker.update()
            self.update_game_state()

    
    def freeze_timers(self):
        if self.white_timer is not None:
            self.white_timer.stop()
            self.black_timer.stop()
