import pygame
from chess_rules import Referee
from chess_AI import ChessAI
from chess_scriber import ChessNotationTranslator

class ChessBoardPresenter:
    def __init__(self, view, referee : Referee):
        self.view = view
        self.referee = referee
        self.clicked_square = None
        self.selected_piece = None
        self.possible_moves = []
        self.running = True
        self.chess_notation = ChessNotationTranslator(referee.board)

    def start_game(self):
        """Start the main game loop."""
        while self.running:
            self.referee.check_timers()
            if self.referee.state == "ongoing":
                self.view.update_view(self)
                pygame.display.flip()
            else:
                self.view.draw_end_screen(self.referee.state, self.referee.current_player())
            self.view.handle_events(self)
        
        if self.referee.white_timer is not None:
            self.referee.white_timer.stop()
            self.referee.black_timer.stop()
        pygame.quit()

    def handle_mouse_click(self, mouse_pos):
        """Handle logic when a square is clicked."""
        col, row = mouse_pos[0] // self.view.square_pixel_length, mouse_pos[1] // self.view.square_pixel_length
        if 0<=col<8 and 0<=row<8:
            self.clicked_square = (row, col)
        else:
            return
        
        piece = self.referee.board.get_piece(self.clicked_square[0], self.clicked_square[1])
        
        if self.selected_piece and self.clicked_square in self.possible_moves:
            self.chess_notation.add_move(self.selected_piece.position, self.clicked_square)
            self.referee.make_move(self.selected_piece.position, self.clicked_square)
            print(self.chess_notation)
            self.selected_piece = None
            self.possible_moves = []
        elif piece and piece.color == self.referee.current_player():
            self.selected_piece = piece
            self.possible_moves = piece.get_possible_moves(self.referee.board)

    def handle_keyboard(self, key):
        """Handle logic when pressing R key"""
        if key == pygame.K_r:
            self.referee.reset()
            self.chess_notation.reset()
            self.possible_moves = []
        if key == pygame.K_b:
            self.referee.board_tracker.undo()
            self.referee.state = "ongoing"
        if key == pygame.K_n:
            self.referee.board_tracker.redo()
        if key == pygame.K_a:
            ai = ChessAI(self.referee, depth=2, color=self.referee.current_player())
            from_pos, to_pos = ai.best_move()
            self.referee.make_move(from_pos, to_pos)
        if key == pygame.K_q:
            self.running = False
