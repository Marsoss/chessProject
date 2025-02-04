from chess_pieces import ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King
from copy import deepcopy
from typing import Tuple, List

BLACK = 'black'
WHITE = 'white'

class Board:
    def __init__(self, board):
        self.board = board
        self.start_board = deepcopy(board)
        

    def __str__(self):
        """Visual representation of the board."""
        str_board = ""
        for row in self.board:
            for p in row:
                str_board += f"{p.__str__()}" if p else ' '
            str_board += "\n"
        return str_board
    
    def reset(self):
        """Reset the board positions to the first move"""
        self.board = deepcopy(self.start_board)
        self.last_move_to = self.last_move_to_init
        self.last_move_from = self.last_move_from_init
        self.last_moved_piece = self.last_moved_piece_init

    
    def start_classic_setup(self):
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

        self.last_moved_piece = None
        self.last_move_from, self.last_move_to = None, None
        self.last_moved_piece_init = None
        self.last_move_from_init, self.last_move_to_init = None, None
        self.start_board = deepcopy(self.board)

    def change_board(self, board, last_moved_piece, move_from, move_to):
        self.board = board
        self.last_moved_piece = last_moved_piece
        self.last_moved_piece_init = last_moved_piece.copy()
        self.last_move_from_init, self.last_move_to_init = move_from, move_to
        self.start_board = deepcopy(board)

    def get_piece(self, row, col) -> ChessPiece|None:
        """Retrieve a piece from the board."""
        return self.board[row][col] if 0 <= row < 8 and 0 <= col < 8 else None

    def set_piece(self, piece, row, col):
        """Place a piece on the board."""
        self.board[row][col] = piece
    
    def is_valid_position(self, row, col) -> bool:
        return 0 <= row < 8 and 0 <= col < 8
    
    def is_available(self, row, col) -> bool:
        return self.is_valid_position(row, col) and self.board[row][col] is None

    def move_piece(self, former_position: Tuple[int, int], new_position: Tuple[int, int]) -> bool:
        """Move a piece to a new position, handling special moves like promotion and castling."""
        piece = self.get_piece(former_position[0], former_position[1])
        self.last_moved_piece = piece
        self.last_move_from = former_position
        self.last_move_to = new_position
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

        return True

    def _execute_move(self, piece:ChessPiece, new_position: Tuple[int, int]) -> None:
        """Perform a basic move."""
        old_row, old_col = piece.position

        new_row, new_col = new_position

        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.position = new_position
        piece.row, piece.col = new_row, new_col


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

    def is_opponent_piece(self, row, col, color) -> bool:
        if self.is_valid_position(row, col):
            piece = self.board[row][col]
            return piece is not None and piece.color != color
        return False

    def erase(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def get_king_position(self, color: str) -> Tuple[int, int]:
        """Find and return the position of the king of the specified color."""
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if isinstance(piece, King) and piece.color == color:
                    return row, col
        print(f"Did not find king {color}")
        return -1, -1
    
    def get_attack_map(self, attacker_color: str) -> List[List[int]]:
        map_attack = [[0 for _ in range(8)] for _ in range(8)]
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r,c)
                if piece is None:
                    continue
                if piece.color != attacker_color:
                    continue
                for rd, cd in piece.get_defended_squares(self):
                    map_attack[rd][cd] += 1
        return map_attack
    
    def get_opponent_color(self, color) -> str:
        """Return the opponent's color."""
        return 'white' if color == 'black' else 'black'
    
    def is_in_check(self, color) -> bool:
        """Check if the king of the given color is in check."""
        king_position = self.get_king_position(color)
        return self.is_attacked(king_position, self.get_opponent_color(color))

    def is_attacked(self, position, attacker_color) -> bool:
        """Check if the given position is attacked by any of the opponent's pieces."""
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == attacker_color:
                    if position in piece.get_defended_squares(self):
                        return True
        return False
    
    def get_all_moves(self, color: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Generate all possible moves for the specified color."""
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    for move in piece.get_possible_moves(self):
                        moves.append(((row, col), move))
        return moves
    
    def copy(self):
        boardcp = Board(deepcopy(self.board)) 
        boardcp.last_moved_piece = self.last_moved_piece 
        boardcp.last_move_from = self.last_move_from
        boardcp.last_move_to = self.last_move_to
        boardcp.last_moved_piece_init = self.last_moved_piece_init 
        boardcp.last_move_from_init = self.last_move_from_init
        boardcp.last_move_to_init = self.last_move_to_init
        boardcp.start_board = deepcopy(self.start_board)
        return boardcp
    
    def __eq__(self, board) -> bool:
        for i in range(8):
            for j in range(8):
                current_piece = self.get_piece(i,j)
                other_piece = board.get_piece(i,j)
                if current_piece!=other_piece:
                    return False
        return True                    
