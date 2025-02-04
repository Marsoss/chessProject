from abc import ABC, abstractmethod
from typing import List, Tuple

class ChessPiece(ABC):
    def __init__(self, color: str, position: Tuple[int, int]):
        self.color = color
        self.position = position
        self.row, self.col = position

    def _is_valid_move(self, new_row: int, new_col: int, board) -> bool:
        """Check if a move is valid (empty square)."""
        return board.is_available(new_row, new_col)

    def _is_valid_capture(self, new_row: int, new_col: int, board) -> bool:
        """Check if the capture is valid (opponent piece)."""
        return board.is_valid_position(new_row, new_col) and board.is_opponent_piece(new_row, new_col, self.color)

    def _add_moves_in_direction(self, dr: int, dc: int, board, possible_moves: List[Tuple[int, int]]) -> None:
        """Add moves in a specific direction (used for sliding pieces like Rook, Bishop, Queen)."""
        new_row = self.row + dr
        new_col = self.col + dc

        while board.is_valid_position(new_row, new_col):
            if not board.is_available(new_row, new_col):
                possible_moves.append((new_row, new_col))
                break

            possible_moves.append((new_row, new_col))
            new_row += dr
            new_col += dc

    def _add_diagonal_moves(self, board, possible_moves: List[Tuple[int, int]]) -> None:
        """Add diagonal moves (used for Bishop and Queen)."""
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        for dr, dc in directions:
            self._add_moves_in_direction(dr, dc, board, possible_moves)

    def _add_line_moves(self, board, possible_moves: List[Tuple[int, int]]) -> None:
        """Add straight line moves (used for Rook and Queen)."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            self._add_moves_in_direction(dr, dc, board, possible_moves)

    def filter_forbidden_moves(self, board, moves: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        allowed_moves = []
        king_row, king_col = board.get_king_position(self.color)
        for row, col in moves:
            board_cp = board.copy()
            if (row, col) != (king_row, king_col):
                board_cp._execute_move(self.copy(), (row, col))
                if (not board_cp.is_in_check(self.color) and 
                    (board.is_available(row, col) or board.is_opponent_piece(row, col, self.color))):
                        allowed_moves.append((row, col))

        return allowed_moves

    @abstractmethod
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Subclasses must implement this method to return possible moves."""
        pass

    @abstractmethod
    def get_defended_squares(self, board) -> List[Tuple[int, int]]:
        """Subclasses must implement this method to return possible moves."""
        pass

    @abstractmethod
    def copy(self):
        """Subclasses must implement this method to return a copy of the piece."""
        pass

    @abstractmethod
    def __str__(self):
        """Subclasses must implement this method to return the SYMBOLIC string value of the piece"""
        pass

    @abstractmethod
    def classic_notation(self):
        """Subclasses must implement this method to return the CLASSICAL string value of the piece"""
        pass
    
    @abstractmethod
    def evaluate(self, board):
        """Subclasses must implement this method to return its position evaluation"""
        pass

    def __eq__(self, value):
        if value is None:
            return False
        if self.color!=value.color:
            return False
        if self.position!=value.position:
            return False
        return type(self)==type(value)


class Pawn(ChessPiece):
    def __init__(self, color: str, position: Tuple[int, int]):
        super().__init__(color, position)
        self.direction = -1 if color == 'white' else 1  # White pawns move up, black pawns move down
    
    def __str__(self):
        return "♙"
    
    def classic_notation(self):
        return "P"

    def evaluate(self, board):
        evaluation = 1
        diff = 8 if self.color == "white" else 0
        coeff = {"row":0.02, "col":0.01}
        center_weight = (3.5-abs(self.col-3.5))
        evaluation+= coeff["row"]*abs(diff-self.row)
        evaluation+= coeff["col"]*center_weight*abs(diff-self.row)
        
        return evaluation

    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible moves for the Pawn."""
        possible_moves = []
        # Normal one-square move
        new_row = self.row + self.direction
        if board.is_available(new_row, self.col):
            possible_moves.append((new_row, self.col))

        # Two-square move on first move
        if (self.row == 6 and self.color == 'white') or (self.row == 1 and self.color == 'black'):
            two_square_row = self.row + 2 * self.direction
            if board.is_available(two_square_row, self.col) and board.is_available(new_row, self.col):
                possible_moves.append((two_square_row, self.col))

        self.__add_capture_moves(board, possible_moves)
        # Add en passant and promotion logic if applicable
        return self.filter_forbidden_moves(board, possible_moves)
    
    def __add_capture_moves(self,board, possible_moves):
    # Capture diagonally
        for row, col in self.get_defended_squares(board):
            if self._is_valid_capture(row, col, board):
                possible_moves.append((row, col))

            if (isinstance(board.last_moved_piece, Pawn)
            and ((board.last_move_from[0] == 6 and board.last_move_to[0] == 4 and self.row == 4) 
            or (board.last_move_from[0] == 1 and board.last_move_to[0] == 3 and self.row == 3))):
                possible_moves.append((row, board.last_moved_piece.col))
    
    def get_defended_squares(self, board) -> List[Tuple[int, int]]:
        attacked_squares = []
        for dc in [-1, 1]:
            new_col = self.col + dc
            new_row = self.row + self.direction
            if board.is_valid_position(new_row, new_col):
                attacked_squares.append((new_row, new_col))
        return attacked_squares

    def copy(self):
        return Pawn(self.color, self.position)


class Knight(ChessPiece):
    def __str__(self):
        return "♘"
    
    def classic_notation(self):
        return "N"
    
    def evaluate(self, board):
        evaluation = 3
        coeff = {"moves":0.03}
        evaluation += coeff["moves"] * len(self.get_possible_moves(board))
        return evaluation
    
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible moves for the Knight (L-shape move)."""
        possible_moves = self.get_defended_squares(board)
        return self.filter_forbidden_moves(board, possible_moves)
    
    def get_defended_squares(self, board) -> List[Tuple[int, int]]:
        defended_squares = []
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for dr, dc in knight_moves:
            new_row = self.row + dr
            new_col = self.col + dc
            if board.is_valid_position(new_row, new_col):
                defended_squares.append((new_row, new_col))
        return defended_squares

    def copy(self):
        return Knight(self.color, self.position)


class Bishop(ChessPiece):
    def __str__(self):
        return "♗"
    
    def classic_notation(self):
        return "B"
    
    def evaluate(self, board):
        evaluation = 3
        coeff = {"moves":0.03}
        evaluation += coeff["moves"] * len(self.get_possible_moves(board))
        return evaluation
    
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible moves for the Bishop (diagonal)."""
        possible_moves = self.get_defended_squares(board)
        return self.filter_forbidden_moves(board, possible_moves)

    def get_defended_squares(self, board) -> List[Tuple[int, int]]:
        possible_moves = []
        self._add_diagonal_moves(board, possible_moves)
        return possible_moves
    
    def copy(self):
        return Bishop(self.color, self.position)


class Rook(ChessPiece):
    def __init__(self, color: str, position: Tuple[int, int]):
        super().__init__(color, position)
        self.has_moved = False
    
    def __str__(self):
        return "♖"
    
    def classic_notation(self):
        return "R"
    
    def __eq__(self, value):
        if type(value) == type(self):
            return super().__eq__(value) and self.has_moved == value.has_moved
        return False
    
    def evaluate(self, board):
        evaluation = 5
        return evaluation
    
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible moves for the Rook (horizontal and vertical)."""
        possible_moves = self.get_defended_squares(board)
        return self.filter_forbidden_moves(board, possible_moves)
    
    def get_defended_squares(self, board) -> List[Tuple[int, int]]:
        possible_moves = []
        self._add_line_moves(board, possible_moves)
        return possible_moves

    def copy(self):
        rook_copy = Rook(self.color, self.position)
        rook_copy.has_moved = self.has_moved
        return rook_copy
    

class Queen(ChessPiece):
    def __str__(self):
        return "♕"
    
    def classic_notation(self):
        return "Q"
    
    def evaluate(self, board):
        evaluation = 9
        return evaluation
    
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible moves for the Queen (both diagonal and straight line)."""
        possible_moves = self.get_defended_squares(board)
        return self.filter_forbidden_moves(board, possible_moves)
    
    def get_defended_squares(self, board) -> List[Tuple[int, int]]:
        defended_squares = []
        self._add_diagonal_moves(board, defended_squares)
        self._add_line_moves(board, defended_squares)
        return defended_squares

    def copy(self):
        return Queen(self.color, self.position)


class King(ChessPiece):
    def __init__(self, color: str, position: Tuple[int, int]):
        super().__init__(color, position)
        self.has_moved = False

    def __str__(self):
        return "♔"
    
    def classic_notation(self):
        return "K"
    
    def __eq__(self, value):
        if type(value) == type(self):
            return super().__eq__(value) and self.has_moved == value.has_moved
        return False
    
    def evaluate(self, board):
        evaluation = 100
        return evaluation
    
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible moves for the King."""
        possible_moves = self.get_defended_squares(board)
        # Add castling moves
        possible_moves += self._get_castling_moves(board)
        return self.filter_forbidden_moves(board, possible_moves)

    
    def get_defended_squares(self, board) -> List[Tuple[int, int]]:
        possible_moves = []
        # Check all adjacent squares
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row = self.row + dr
                new_col = self.col + dc
                if board.is_valid_position(new_row, new_col):
                    possible_moves.append((new_row, new_col))
        return possible_moves
    
    def __check_queenside_castle(self, board) -> Tuple[int, int]|None:
        rook = board.get_piece(self.row, 0)
        if not isinstance(rook, Rook):
            return
        if rook.has_moved:
            return 
        for i in range(1,4):
            if board.is_attacked((self.row, i), board.get_opponent_color(self.color)) or not board.is_available(self.row,i): 
                return
        return (self.row, self.col-2)
    
    def __check_kingside_castle(self, board) -> Tuple[int, int]|None:
        rook = board.get_piece(self.row, 7)
        if not isinstance(rook, Rook):
            return 
        if rook.has_moved:
            return 
        for i in range(5,7):
            if board.is_attacked((self.row, i), board.get_opponent_color(self.color)) or not board.is_available(self.row,i): 
                return
        return (self.row, self.col+2)

    def _get_castling_moves(self, board) -> List[Tuple[int, int]]:
        """Add castling moves for the King."""
        castling_moves = []
        if self.has_moved or board.is_in_check(self.color):
            return []
        kingside_castle = self.__check_kingside_castle(board)
        if kingside_castle is not None:
            castling_moves.append(kingside_castle)

        queenside_castle = self.__check_queenside_castle(board)
        if queenside_castle is not None:
            castling_moves.append(queenside_castle)
        
        return castling_moves

    def copy(self):
        king_copy = King(self.color, self.position)
        king_copy.has_moved = self.has_moved
        return king_copy
    

if __name__ == "__main__":
    color = "white"
    row = 0
    col = 0
    
    p1 = Rook(color, (row, col))
    p2 = Rook(color, (row, col))

    print(p1!=p2)