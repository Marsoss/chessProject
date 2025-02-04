from chess_pieces import King, Pawn

class ChessNotationTranslator:
    def __init__(self, board):
        """
        Initialise l'objet avec le plateau d'échecs.
        :param board: Une matrice 8x8 représentant les pièces sur le plateau.
                      Les cases vides contiennent None ou ''.
        """
        self.board = board
        self.turn_count = 0
        self.game_notation = ""
        self.files = "abcdefgh"  # Colonnes en notation échiquéenne

    def get_piece(self, position):
        """
        Retourne la pièce sur une position donnée.
        :param position: Tuple (ligne, colonne) représentant la position.
        :return: Chaîne représentant la pièce ou None si vide.
        """
        row, col = position
        return self.board.get_piece(row, col)

    def find_similar_pieces(self, start, end):
        """
        Trouve les pièces similaires qui peuvent se rendre à la position d'arrivée.
        :param start: Position d'origine.
        :param end: Position d'arrivée.
        :param piece_symbol: Symbole de la pièce qui se déplace.
        :return: Liste des positions des pièces similaires.
        """
        candidates = []
        current_piece = self.get_piece(start)
        for row in range(8):
            for col in range(8):
                if (row, col) == start:
                    continue
                other_piece = self.get_piece((row, col))
                if isinstance(other_piece, type(current_piece)):
                    # Ajoutez ici une vérification pour valider si ce candidat peut se déplacer vers `end`
                    if other_piece.color == current_piece.color:
                        if end in other_piece.get_possible_moves(self.board):
                            candidates.append((row, col))
        return candidates

    def handle_king_move(self, start, end):
        if abs(start[1]-end[1])>1:
            if end[1]==6:
                return 'O-O'
            elif end[1]==2:
                return 'O-O-O'
        else:
            return self.translate_move(start, end)
        
    def piece_symbol(self, piece):
        symbol = piece.classic_notation()
        return  symbol if symbol != 'P' else '' 
    
    def transcribe_square(self, square): 
        return f'{self.files[square[1]]}{7-square[0]+1}'
    
    def is_capture(self, start, end):
        piece = self.get_piece(start)
        if isinstance(piece, Pawn) and end[1]!=piece.col:
            return f'{self.transcribe_square(end)[0]}x'
        elif self.get_piece(end) != None:
            print(f'get_piece(end)={self.get_piece(end)}')
            return 'x'
        else: 
            return ''
    
    def promotion(self, start, end):
        piece = self.get_piece(start)
        if not isinstance(piece, Pawn):
            return ''
        if end[1] not in [0,7]:
            return ''
        return 'Q'

    def is_check(self, start, end):
        color = self.get_piece(start).color
        board_cp = self.board.copy()
        board_cp.move_piece(start, end)
        if board_cp.is_in_check(board_cp.get_opponent_color(color)):
            return '+'
        else:
            return ''

    def translate_move(self, start, end):
        """
        Traduit un mouvement en notation algébrique, y compris désambiguïsation.
        :param start: Tuple (ligne, colonne) pour la position de départ.
        :param end: Tuple (ligne, colonne) pour la position d'arrivée.
        :return: Notation algébrique du mouvement.
        """
        start_piece = self.get_piece(start)

        piece_symbol = self.piece_symbol(start_piece)
        
        # Conversion des indices en notation échiquéenne
        end_square = self.transcribe_square(end)

        # Vérifie s'il s'agit d'une capture
        capture_symbol = self.is_capture(start, end)
        
        # Vérifie s'il s'agit d'une promotion
        promote_symbol = self.promotion(start, end)

        # Vérifie di l'adversaire est en échec
        check_symbol = self.is_check(start, end)

        # Désambiguïsation si nécessaire
        similar_pieces = self.find_similar_pieces(start, end)
        disambiguation = ''
        if similar_pieces:
            # Vérifiez si la colonne ou la ligne suffit pour désambiguïser
            same_file = any(pos[1] == start[1] for pos in similar_pieces)
            same_rank = any(pos[0] == start[0] for pos in similar_pieces)
            if same_file:
                disambiguation += self.transcribe_square(start)[1]
            if same_rank or not same_file:
                disambiguation += self.transcribe_square(start)[0]

        # Construction du mouvement
        move = f"{piece_symbol}{disambiguation}{capture_symbol}{end_square}{promote_symbol}{check_symbol}"
        return move

    def write_move(self, start, end):
        moved_piece = self.get_piece(start)
        if not moved_piece:
            raise ValueError(f"Aucune pièce à la position {start}.")    
        if isinstance(moved_piece, King):
            return self.handle_king_move(start, end)
        else:
            return self.translate_move(start, end)
    
    def add_move(self, start, end):
        if self.turn_count % 2 == 0:
            self.game_notation+=f'{self.turn_count//2 + 1}. '
        self.turn_count +=1

        self.game_notation+=self.write_move(start, end)+" "

    def __str__(self):
        return self.game_notation
    
    def save(self):
        file_name = input("Entrer le nom de la partie à enregistrer")
        f = open(file_name+".pgn", "w")
        f.write(self.game_notation)
        f.close()

    def reset(self):
        self.game_notation = ""


if __name__=="__main__":
    # Exemple d'utilisation :
    board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, 'N', None, None, None, None, None],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]

    translator = ChessNotationTranslator(board)

    # Exemple : Deux cavaliers peuvent aller en c4, désambiguïsation nécessaire
    start_position1 = (7, 1)  # Cavalier en b1
    start_position2 = (5, 2)  # Cavalier en c3
    end_position = (4, 2)     # c4

    # Pour chaque mouvement possible :
    move1 = translator.write_move(start_position1, end_position)
    move2 = translator.write_move(start_position2, end_position)
    print(move1)  # Sortie attendue : Nbc4
    print(move2)  # Sortie attendue : N3c4
