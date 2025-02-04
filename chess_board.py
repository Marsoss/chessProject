from typing import Tuple, List
from copy import deepcopy

from chess_timer import Timer
from board_tracker import BoardTracker

from chess_pieces import ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King

from chess_typing import Color, Square, Move, WHITE, BLACK

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.start_player = WHITE
        self.start_setup()
        self.start_board = deepcopy(self.board)
        self.last_moved_piece = None
        self.last_move_from, self.last_move_to = None, None
        self.turn_count = 1
        self.state = "ongoing"
        self.white_timer = Timer(3*60, 2) # 3 minutes
        self.black_timer = Timer(3*60, 2)
        self.board_tracker = BoardTracker(self)

    def __str__(self) -> str:
        str_board = ""
        for row in self.board:
            for p in row:
                if p is not None:
                    str_board+=f"{p.__str__()}"
                else:
                    str_board+=' '#·'
            str_board+="\n"
        return  str_board
    
    def change_board(self, board, last_moved_piece):
        self.board = board
        self.last_moved_piece = last_moved_piece
        self.start_player = self.get_opponent_color(last_moved_piece.color)
        self.start_board = deepcopy(board)

    def reset(self):
        """Reset the board positions to the first move"""
        self.board = deepcopy(self.start_board)
        self.state = "ongoing"
        self.current_player = self.start_player
        self.turn_count = 1
        self.black_timer.reset()
        self.white_timer.reset()
        self.board_tracker.reset()
    
    def erase(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def get_current_player(self):
            return self.get_opponent_color(self.start_player) if self.turn_count%2 == 0 else self.start_player

    def next_player(self):
        """Switch to the next player."""
        current_player = self.get_current_player()
        if current_player==WHITE:
            if self.turn_count < 3:
                self.black_timer.start()
            else:
                self.white_timer.pause()
                self.black_timer.resume()

        else:
            if self.turn_count < 3:
                self.white_timer.start()
            else:
                self.white_timer.resume()
            self.black_timer.pause()

        if self.is_check_mate(current_player):
            self.state = "checkmate"
        elif not self.is_legal_move_possible(current_player):
            self.state = "stalemate"
        self.turn_count +=1


    def start_setup(self):
        """Initialize the board with the pieces in their starting positions."""
        # Black pieces
        for i in range(8):
            for j in range(8):
                self.board[i][j] = None

        self.board[0][0] = Rook(BLACK, (0, 0))
        self.board[0][7] = Rook(BLACK, (0, 7))
        self.board[0][1] = Knight(BLACK, (0, 1))
        self.board[0][6] = Knight(BLACK, (0, 6))
        self.board[0][2] = Bishop(BLACK, (0, 2))
        self.board[0][5] = Bishop(BLACK, (0, 5))
        self.board[0][3] = Queen(BLACK, (0, 3))
        self.board[0][4] = King(BLACK, (0, 4))
        for i in range(8):
            self.board[1][i] = Pawn(BLACK, (1, i))

        # White pieces
        self.board[7][0] = Rook(WHITE, (7, 0))
        self.board[7][7] = Rook(WHITE, (7, 7))
        self.board[7][1] = Knight(WHITE, (7, 1))
        self.board[7][6] = Knight(WHITE, (7, 6))
        self.board[7][2] = Bishop(WHITE, (7, 2))
        self.board[7][5] = Bishop(WHITE, (7, 5))
        self.board[7][3] = Queen(WHITE, (7, 3))
        self.board[7][4] = King(WHITE, (7, 4))
        for i in range(8):
            self.board[6][i] = Pawn(WHITE, (6, i))

    def is_valid_position(self, row, col) -> bool:
        return 0 <= row < 8 and 0 <= col < 8

    def is_available(self, row, col) -> bool:
        return self.is_valid_position(row, col) and self.board[row][col] is None

    def is_opponent_piece(self, row, col, color) -> bool:
        if self.is_valid_position(row, col):
            piece = self.board[row][col]
            return piece is not None and piece.color != color
        return False

    def get_piece(self, row: int, col: int) -> ChessPiece|None:
        """Retrieve the piece at a specific position."""
        if self.is_valid_position(row, col):
            return self.board[row][col]
        return None
    
    def set_piece(self, piece: ChessPiece, row: int, col: int):
        self.board[row][col] = piece

    def move_piece(self, former_position: Tuple[int, int], new_position: Tuple[int, int]) -> bool:
        """Move a piece to a new position, handling special moves like promotion and castling."""
        piece = self.get_piece(former_position[0], former_position[1])
        if not piece:
            return False
        row, col = piece.position
        new_row, new_col = new_position
        
        
        if (new_row, new_col) not in piece.get_possible_moves(self):
            print("Wrong move !")
            return False

        # Handle special cases for pawn promotion and castling
        if isinstance(piece, Pawn):
            self._handle_pawn_moves(piece, new_position)
        elif isinstance(piece, King):
            self._handle_king_moves(piece, new_position)
        else:
            self._execute_move(piece, new_position)
        
        self.last_move_from = row, col
        self.last_move_to = new_row, new_col
        self.last_moved_piece = self.get_piece(new_row, new_col)
        self.next_player()
        self.board_tracker.update()

        return True

    def _execute_move(self, piece: ChessPiece, new_position: Tuple[int, int]) -> None:
        """Perform a basic move."""
        old_row, old_col = piece.position

        new_row, new_col = new_position

        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.position = new_position
        piece.row, piece.col = new_position
        

    def _handle_castling(self, king: King, new_position: Tuple[int, int]) -> None:
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
    
    def _handle_en_passant(self, pawn: Pawn, new_position: Tuple[int, int]) -> None:
        _, new_col = new_position
        old_row = pawn.row
        self._execute_move(pawn, new_position)
        self.board[old_row][new_col] = None

    def _handle_pawn_moves(self, piece:Pawn, new_position: Tuple[int, int]) -> None:
            new_row, new_col = new_position
            row, col = piece.row, piece.col
        # Promotion: if a pawn reaches the final row
            if (new_row == 0 and piece.color == WHITE) or (new_row == 7 and piece.color == BLACK):
                # Promote the pawn to a queen (can be modified for other promotions)
                self.board[new_row][new_col] = Queen(piece.color, (new_row, new_col))
                self.board[row][col] = None
            
            elif (new_col!=col) and self.is_available(new_row, new_col):
                    self._handle_en_passant(piece, (new_row, new_col))
            else:
                self._execute_move(piece, new_position)
    
    def _handle_king_moves(self, piece: King, new_position) -> None:
        # Handle castling
        _, new_col = new_position
        col = piece.col
        if abs(col - new_col) == 2:
            self._handle_castling(piece, new_position)
        else:
            self._execute_move(piece, new_position)

    def is_in_check(self, color: str) -> bool:
        """Determine if the current player's king is in check."""
        row, col = self.get_king_position(color)
        if row == -1:
            return True
        opponent_color = self.get_opponent_color(color)
        return self.is_attacked(row, col, opponent_color)

    def get_king_position(self, color: str) -> Tuple[int, int]:
        """Find and return the position of the king of the specified color."""
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if isinstance(piece, King) and piece.color == color:
                    return row, col
        print(f"Did not find king {color}")
        return -1, -1

    def get_opponent_color(self, color: str) -> str:
        """Return the opponent's color."""
        return WHITE if color == BLACK else BLACK
    
    def get_attack_map(self, attacker_color: str) -> List[List[int]]:
        map_attack = [[0 for _ in range(8)] for _ in range(8)]
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece is None:
                    continue
                if piece.color != attacker_color:
                    continue
                for rd, cd in piece.get_defended_squares(self):
                    map_attack[rd][cd] += 1
        return map_attack

    def is_attacked(self, row: int, col: int, attacker_color: str) -> bool:
        """Check if a square is attacked by any of the opponent's pieces."""
        return self.get_attack_map(attacker_color)[row][col] > 0
    
    def is_legal_move_possible(self, color: str) -> bool:
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece is None:
                    continue
                if piece.color != color:
                    continue
                board_cp = self.copy()
                for rd, cd in piece.get_possible_moves(self):
                    board_cp._execute_move(piece.copy(), (rd, cd))
                    if not board_cp.is_in_check(color):
                        return True
        return False

    def is_check_mate(self, color: str) -> bool:
        return self.is_in_check(color) and not self.is_legal_move_possible(color)
    
    def time_is_up(self) -> bool:
        current_player = self.get_current_player()
        if current_player == BLACK:
            return self.black_timer.timesup
        else: 
            return self.white_timer.timesup
        
    def get_board_copy(self):
        new_board = [[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece is not None:
                    new_board[row][col] = piece.copy()
        return new_board

    def copy(self):
        """Return a deep copy of the current board."""
        new_board = Board()
        new_board.board = self.get_board_copy()

        if self.last_moved_piece is not None:
            new_board.last_moved_piece = self.last_moved_piece.copy()
        new_board.last_move_from = self.last_move_from
        new_board.last_move_to = self.last_move_to
        new_board.last_moved_piece = None if self.last_moved_piece is None else self.last_moved_piece.copy()
        new_board.start_board = self.start_board
        new_board.turn_count = self.turn_count
        return new_board
