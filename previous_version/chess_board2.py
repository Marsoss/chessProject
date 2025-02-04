# Refactor of Board class to include special moves (pawn promotion, castling, etc.)
from chess_pieces import ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King

WHITE = 'white'
BLACK = 'black'

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()
        self.last_moved_piece = None

    def setup_pieces(self):
        """Initialize the board with the pieces in their starting positions."""
        # Black pieces
        self.board[0][0] = Rook(BLACK, (0, 0))
        self.board[7][0] = Rook(BLACK, (7, 0))
        self.board[1][0] = Knight(BLACK, (1, 0))
        self.board[6][0] = Knight(BLACK, (6, 0))
        self.board[2][0] = Bishop(BLACK, (2, 0))
        self.board[5][0] = Bishop(BLACK, (5, 0))
        self.board[3][0] = Queen(BLACK, (3, 0))
        self.board[4][0] = King(BLACK, (4, 0))
        for i in range(8):
            self.board[i][1] = Pawn(BLACK, (i, 1))

        # White pieces
        self.board[0][7] = Rook(WHITE, (0, 7))
        self.board[7][7] = Rook(WHITE, (7, 7))
        self.board[1][7] = Knight(WHITE, (1, 7))
        self.board[6][7] = Knight(WHITE, (6, 7))
        self.board[2][7] = Bishop(WHITE, (2, 7))
        self.board[5][7] = Bishop(WHITE, (5, 7))
        self.board[3][7] = Queen(WHITE, (3, 7))
        self.board[4][7] = King(WHITE, (4, 7))
        for i in range(8):
            self.board[i][6] = Pawn(WHITE, (i, 6))

    def is_valid_position(self, row, col) -> bool:
        return 0 <= row < 8 and 0 <= col < 8

    def is_available(self, row, col) -> bool:
        return self.is_valid_position(row, col) and self.board[row][col] is None

    def is_opponent_piece(self, row, col, color) -> bool:
        if self.is_valid_position(row, col):
            piece = self.board[row][col]
            return piece is not None and piece.color != color
        return False

    def get_piece(self, row: int, col: int):
        """Retrieve the piece at a specific position."""
        if self.is_valid_position(row, col):
            return self.board[row][col]
        return None

    def move_piece(self, former_position: Tuple[int, int], new_position: Tuple[int, int]) -> bool:
        """Move a piece to a new position, handling special moves like promotion and castling."""
        piece = self.get_piece(former_position[0], former_position[1])
        if not piece:
            return False

        row, col = piece.position
        new_row, new_col = new_position

        if new_position not in piece.get_possible_moves(self):
            return False

        # Handle special cases for pawn promotion and castling
        if isinstance(piece, Pawn):
            # Promotion: if a pawn reaches the final row
            if (new_row == 0 and piece.color == WHITE) or (new_row == 7 and piece.color == BLACK):
                # Promote the pawn to a queen (can be modified for other promotions)
                self.board[new_row][new_col] = Queen(piece.color, (new_row, new_col))
            else:
                self._execute_move(piece, new_position)

        elif isinstance(piece, King):
            # Handle castling
            if abs(col - new_col) == 2:
                self._handle_castling(piece, former_position, new_position)
            else:
                self._execute_move(piece, new_position)
        else:
            self._execute_move(piece, new_position)

        self.last_moved_piece = piece
        return True

    def _execute_move(self, piece: ChessPiece, new_position: Tuple[int, int]) -> None:
        """Perform a basic move."""
        old_row, old_col = piece.position
        new_row, new_col = new_position
        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.position = new_position

    def _handle_castling(self, king: King, former_position: Tuple[int, int], new_position: Tuple[int, int]) -> None:
        """Handle castling by moving both the king and the appropriate rook."""
        new_row, new_col = new_position
        # King-side castling
        if new_col == 6:
            rook = self.get_piece(new_row, 7)
            self._execute_move(rook, (new_row, 5))
        # Queen-side castling
        elif new_col == 2:
            rook = self.get_piece(new_row, 0)
            self._execute_move(rook, (new_row, 3))

        self._execute_move(king, new_position)

    def is_in_check(self, color: str) -> bool:
        """Determine if the current player's king is in check."""
        king_position = self.get_king_position(color)
        opponent_color = self.get_opponent_color(color)

        # Check if any opponent's piece can attack the king
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if (
                    piece is not None
                    and piece.color == opponent_color
                    and king_position in piece.get_possible_moves(self)
                ):
                    return True

        return False

    def get_king_position(self, color: str) -> Tuple[int, int]:
        """Find and return the position of the king of the specified color."""
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None

    def get_opponent_color(self, color: str) -> str:
        """Return the opponent's color."""
        return WHITE if color == BLACK else BLACK

    def is_attacked(self, row: int, col: int, attacker_color: str) -> bool:
        """Check if a square is attacked by any of the opponent's pieces."""
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if (
                    piece is not None
                    and piece.color == attacker_color
                    and (row, col) in piece.get_possible_moves(self)
                ):
                    return True

        return False

    def copy(self):
        """Return a deep copy of the current board."""
        new_board = Board()
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece:
                    new_board.set_piece(row, col, piece.copy())
        if self.last_moved_piece:
            new_board.last_moved_piece = self.last_moved_piece.copy()
        return new_board

