import pygame
from chess_board import Board
from chess_pieces import Pawn, Knight, Bishop, Rook, Queen, King

class ChessBoardView:
    def __init__(self):
        # Define colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT = (255, 255, 0)
        self.GREY = (128, 128, 128)

        # Define the size of the chessboard and each cell
        self.nb_square = 8
        self.square_pixel_length = 80

        # Calculate the screen size
        self.screen_width = self.nb_square * self.square_pixel_length
        self.screen_height = self.nb_square * self.square_pixel_length

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.chess_font = pygame.font.SysFont("chessmagnetic", 48)

        pygame.display.set_caption("Chess")

        # Initialize the game board
        self.board = Board()
        self.current_player = 'white'

        # Variables for gameplay
        self.running = True
        self.clicked_square = None
        self.selected_piece = None
        self.possible_moves = []
    
    def start_game(self):
        """Start the main game loop."""
        while self.running:
            self.handle_events()
            self.draw_board()
            pygame.display.flip()

        pygame.quit()

    def next_player(self):
        """Switch to the next player."""
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def piece_to_char(self, piece):
        """Convert a chess piece to a character for display."""
        if piece is None:
            return ''
        if isinstance(piece, Pawn):
            char = 'p'
        elif isinstance(piece, Rook):
            char = 'r'
        elif isinstance(piece, Bishop):
            char = 'b'
        elif isinstance(piece, Knight):
            char = 'n'
        elif isinstance(piece, Queen):
            char = 'q'
        elif isinstance(piece, King):
            char = 'k'
        return char if piece.color == 'white' else char.upper()

    def put_text(self, piece, row, col):
        """Render the piece's character at the specified board position."""
        if piece is not None:
            if piece.color == "white":
                text = self.chess_font.render(self.piece_to_char(piece), True, (255, 0, 0))
            else:
                text = self.chess_font.render(self.piece_to_char(piece), True, (0, 0, 255))
            text_rect = text.get_rect(center=(col * self.square_pixel_length + self.square_pixel_length // 2,
                                          row * self.square_pixel_length + self.square_pixel_length // 2
                                          ))
            self.screen.blit(text, text_rect)

    def update_view(self):
        """Update the view of all pieces on the board."""
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)  # No need to reverse row and col
                self.put_text(piece, row, col)

    def handle_events(self):
        """Handle Pygame events, including mouse clicks."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                self.handle_r_key(event.key)
                

    def handle_mouse_click(self, mouse_pos):
        """Handle logic when a square is clicked."""
        print("NEW CLICK!!!")
        col, row = mouse_pos[0] // self.square_pixel_length, mouse_pos[1] // self.square_pixel_length
        # Use row as is for White's perspective (row 0 at the bottom for white)
        self.clicked_square = (row, col)
        
        piece = self.board.get_piece(self.clicked_square[0], self.clicked_square[1])
        
        # If a piece is selected and it is the player's turn
        if self.selected_piece and self.clicked_square in self.possible_moves:
            self.board.move_piece(self.selected_piece.position, self.clicked_square)
            self.next_player()
            self.selected_piece = None
            self.possible_moves = []
        elif piece and piece.color == self.current_player:
            self.selected_piece = piece
            self.possible_moves = piece.get_possible_moves(self.board)
            
    def handle_r_key(self, key):
        """Handle logic when pressing R key"""
        if key == pygame.K_r:  # Detect the "R" key
                    self.board.start_setup()  # Cal
                    self.current_player = "white"
                    self.possible_moves = []

    def color_square(self, row, col, color):
        """Color a specific square on the board."""        
        square_rect = pygame.Rect(col * self.square_pixel_length, row * self.square_pixel_length, 
                                  self.square_pixel_length, self.square_pixel_length)
        pygame.draw.rect(self.screen, color, square_rect)
    
    def small_square(self, row, col, color):
        square_rect = pygame.Rect(col * self.square_pixel_length + self.square_pixel_length//4, 
                                  row * self.square_pixel_length + self.square_pixel_length//4, 
                                  self.square_pixel_length//2, self.square_pixel_length//2)
        pygame.draw.rect(self.screen, color, square_rect)


    def draw_board(self):
        """Draw the chess board and highlight selected squares and possible moves."""        
        for row in range(self.nb_square):
            for col in range(self.nb_square):
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                self.color_square(row, col, color)

        # Highlight selected square
        if self.clicked_square:
            self.color_square(self.clicked_square[0], self.clicked_square[1], self.LIGHT)

        # Highlight possible moves
        for move in self.possible_moves:
            self.small_square(move[0], move[1], self.GREY)

        self.update_view()

if __name__ == '__main__':
    game = ChessBoardView()
    game.start_game()
