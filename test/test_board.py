import sys
import os

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add parent directory to sys.path
sys.path.append(parent_dir)

from chess_board_view import ChessBoardView
from chess_board import Board, WHITE, BLACK
from chess_pieces import King, Bishop, Rook, Queen, Knight, Pawn
from chess_board_presenter import ChessBoardPresenter

if __name__ == '__main__':
    board = Board()
    bboard = [[None for _ in range(8)] for _ in range(8)]
    # Black pieces
    for i in range(8):
        for j in range(8):
            bboard[i][j] = None

    bboard[0][4] = King(BLACK, (0, 4))
    for i in range(8):
        bboard[1][i] = Pawn(BLACK, (1,i))

        # White pieces
        bboard[7][0] = Rook(WHITE, (7, 0))
        bboard[7][1] = Knight(WHITE, (7, 1))
        bboard[7][2] = Bishop(WHITE, (7, 2))
        bboard[7][5] = Bishop(WHITE, (7, 5))
        bboard[7][3] = Queen(WHITE, (7, 3))
        bboard[7][4] = King(WHITE, (7, 4))

    board.change_board(bboard, last_moved_piece=King(BLACK, (0, 4)))
    view = ChessBoardView()
    presenter = ChessBoardPresenter(view, board)
    presenter.start_game()
