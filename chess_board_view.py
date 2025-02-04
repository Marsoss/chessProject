import pygame
from chess_pieces import Pawn, Rook, King, Queen, Bishop, Knight
from pygame_extension.arrow import draw_arrow

class ChessBoardView:
    def __init__(self):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT = (255, 255, 0)
        self.GREY = (128, 128, 128)

        self.nb_square = 8
        self.square_pixel_length = 80

        self.screen_width = self.nb_square * self.square_pixel_length + 400
        self.screen_height = self.nb_square * self.square_pixel_length

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.chess_font = pygame.font.SysFont("chessmagnetic", 48)

        pygame.display.set_caption("Chess")

    def draw_board(self, presenter):
        """Draw the chess board and highlight selected squares and possible moves."""
        for row in range(self.nb_square):
            for col in range(self.nb_square):
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                self.color_square(row, col, color)

        # Highlight selected square
        if presenter.clicked_square:
            self.color_square(presenter.clicked_square[0], presenter.clicked_square[1], self.LIGHT)

        # Highlight possible moves
        for move in presenter.possible_moves:
            self.small_square(move[0], move[1], self.GREY)

    def update_view(self, presenter):
        """Update the view of all pieces on the board."""
        self.screen.fill((0,0,0))
        self.draw_board(presenter)
        for row in range(8):
            for col in range(8):
                piece = presenter.referee.board.get_piece(row, col)
                self.put_text(piece, row, col)
        self.draw_timers(presenter.referee)
        self.draw_turn_count(presenter.referee)
        self.draw_arrow_last_move(presenter.referee.board)

    def put_text(self, piece, row, col):
        """Render the piece's character at the specified board position."""
        if piece is not None:
            char = self.piece_to_char(piece)
            color = (255, 0, 0) if piece.color == "white" else (0, 0, 255)
            text = self.chess_font.render(char, True, color)
            text_rect = text.get_rect(center=(col * self.square_pixel_length + self.square_pixel_length // 2,
                                              row * self.square_pixel_length + self.square_pixel_length // 2))
            self.screen.blit(text, text_rect)

    def piece_to_char(self, piece):
        """Convert a chess piece to a character for display."""
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

    def handle_events(self, presenter):
        """Handle Pygame events, including mouse clicks."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                presenter.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                presenter.handle_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                presenter.handle_keyboard(event.key)

    def color_square(self, row, col, color):
        """Color a specific square on the board."""
        square_rect = pygame.Rect(col * self.square_pixel_length, row * self.square_pixel_length,
                                  self.square_pixel_length, self.square_pixel_length)
        pygame.draw.rect(self.screen, color, square_rect)

    def small_square(self, row, col, color):
        """Draw a small square to indicate a possible move."""
        square_rect = pygame.Rect(col * self.square_pixel_length + self.square_pixel_length // 4,
                                  row * self.square_pixel_length + self.square_pixel_length // 4,
                                  self.square_pixel_length // 2, self.square_pixel_length // 2)
        pygame.draw.rect(self.screen, color, square_rect)

    def draw_end_screen(self, result, color:str):
        self.screen.fill((0, 0, 0))  # Fill the screen with a color, e.g., black
        font = pygame.font.SysFont(None, 74)
        
        if result == "checkmate":
            text = font.render(f'{color.upper()} is Checkmate !', True, (255, 255, 255))
            self.screen.blit(text, (self.screen_width//2 - 270, self.screen_height//3 - 50))  # Position the text
        elif result == "stalemate":
            text = font.render('Stalemate !', True, (255, 255, 255))
            self.screen.blit(text, (self.screen_width//2 - 140, self.screen_height//3 - 50))  # Position the text
        elif result == "timesup":    
            text = font.render(f'{color.upper()} had no time left !', True, (255, 255, 255))
            self.screen.blit(text, (self.screen_width//2 - 300, self.screen_height//3 - 50))  # Position the text
        elif result == "repetition":    
            text = font.render('Draw by repetition', True, (255, 255, 255))
            self.screen.blit(text, (self.screen_width//2 - 230, self.screen_height//3 - 50))  # Position the text
        text = font.render('Press R to resart', True, (255, 255, 255))
        self.screen.blit(text, (self.screen_width//2 - 205, (2*self.screen_height)//3 - 50))  # Position the text
        
        pygame.display.flip()  # Update the display

    def draw_timer_rect(self, left, top, width, height, timer):
    
        pixel_width = 5
        timer_rect1 = pygame.Rect(left, top,
                                  height, width)
        timer_rect2 = pygame.Rect(left + pixel_width, top + pixel_width,
                                  height - 2*pixel_width, width - 2*pixel_width)
        
        pygame.draw.rect(self.screen, self.WHITE, timer_rect1)
        pygame.draw.rect(self.screen, self.BLACK, timer_rect2)

        font = pygame.font.SysFont(None, 74)
        text = font.render(timer.__str__(), True, (255, 255, 255))
        self.screen.blit(text, (left + 2*pixel_width, top+2*pixel_width))  # Position the text
    
    def draw_timers(self, referee):
        if referee.white_timer is not None:
            top_black = self.screen_height//3 
            top_white = 2*self.screen_height//3
            width = 200
            height = 70
            
            left = self.nb_square * self.square_pixel_length + 50
            self.draw_timer_rect(left, top_black, height, width, referee.black_timer)
            self.draw_timer_rect(left, top_white, height, width, referee.white_timer)

    def draw_turn_count(self, referee):
        shift = 30
        radius = 13
        height = self.screen_height - 30 if referee.current_player() == 'white' else 30

        center = self.nb_square * self.square_pixel_length + shift, height
        pygame.draw.circle(self.screen, (self.GREY), center, radius)

        shifth = 9
        shiftw = 6 if len(str(referee.turn_count))<2 else 11
        
        font = pygame.font.SysFont(None, 30)
        text = font.render(str(referee.turn_count), True, (20, 20, 20))
        self.screen.blit(text, (center[0] - shiftw, height - shifth))  # Position the text

    def draw_arrow_last_move(self, board):
        if board.last_move_from is None:
            return
        row_start, col_start = board.last_move_from
        row_end, col_end = board.last_move_to
        v_start = pygame.Vector2((col_start+0.5) * self.square_pixel_length, (row_start+0.5) * self.square_pixel_length)
        v_end = pygame.Vector2((col_end+0.5) * self.square_pixel_length, (row_end+0.5) * self.square_pixel_length)

        draw_arrow(self.screen, v_start, v_end, self.GREY, 8, 16, 16)

        

