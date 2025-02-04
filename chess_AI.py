import math
from typing import Tuple, List

class ChessAI:
    def __init__(self, referee, depth=3, color="black"):
        self.referee = referee
        self.board = referee.board
        self.depth = depth  # Depth of search for the AI
        self.color = color  # AI's color


    def evaluate_board(self) -> int:
        """Simple evaluation function that sums up piece values. Modify to add advanced heuristics."""
        score = 0

        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece is not None:
                    value = piece.evaluate(self.board)
                    score += value if piece.color == self.color else -value
        return score

    def get_all_moves(self, color: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Generate all possible moves for the specified color."""
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    for move in piece.get_possible_moves(self.board):
                        moves.append(((row, col), move))
        return moves

    def minimax(self, depth: int, alpha: int, beta: int, maximizing: bool) -> int:
        """Minimax function with alpha-beta pruning."""
        if depth == 0 :
            return self.evaluate_board()
        
        if maximizing:
            max_eval = -math.inf
            for move in self.get_all_moves(self.color):
                from_pos, to_pos = move
                # Make a move and evaluate
                piece_captured = self.board.get_piece(*to_pos)
                self.board.move_piece(from_pos, to_pos)
                
                eval_score = self.minimax(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                # Undo move
                self.board.move_piece(to_pos, from_pos)
                if piece_captured:
                    self.board.set_piece(piece_captured, *to_pos)
                
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = math.inf
            opponent_color = self.board.get_opponent_color(self.color)
            for move in self.get_all_moves(opponent_color):
                from_pos, to_pos = move
                # Make a move and evaluate
                piece_captured = self.board.get_piece(*to_pos)
                self.board.move_piece(from_pos, to_pos)
                
                eval_score = self.minimax(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                # Undo move
                self.board.move_piece(to_pos, from_pos)
                if piece_captured:
                    self.board.set_piece(piece_captured, *to_pos)

                if beta <= alpha:
                    break
            return min_eval

    def best_move(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Find the best move for the AI using the minimax algorithm with alpha-beta pruning."""
        best_score = -math.inf
        best_move = None
        self.board = self.referee.board.copy()

        for move in self.get_all_moves(self.color):
            from_pos, to_pos = move
            piece_captured = self.board.get_piece(*to_pos)
            self.board.move_piece(from_pos, to_pos)

            move_score = self.minimax(self.depth - 1, -math.inf, math.inf, False)
            
            # Undo move
            self.board.move_piece(to_pos, from_pos)
            if piece_captured:
                self.board.set_piece(piece_captured, *to_pos)
            
            if move_score > best_score:
                best_score = move_score
                best_move = move

        return best_move
