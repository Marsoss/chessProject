
class BoardTracker():
    def __init__(self, referee):
        self.referee = referee
        self.reset()

    def __str__(self):
        return f"index: {str(self.index)}, turn_count: {str(self.referee.turn_count)}, board_list_size: {len(self.board_list)}"

    def reset(self):
        self.board_list = [self.referee.board.copy()]
        self.index = 0
        self.max_index = 0

    def get_current_board(self):
        return self.board_list[self.index].copy()

    def undo(self):
        if self.index > 0:
            self.index -= 1
            self.referee.turn_count -= 1
        self.referee.board = self.get_current_board()
    
    def redo(self):
        if self.index + 1 < len(self.board_list):
            self.index += 1
            self.referee.turn_count += 1
        self.referee.board = self.get_current_board()
    
    def update(self):
        # Tronquer les futurs états si on revient en arrière
        if self.index < len(self.board_list) - 1:
            self.board_list = self.board_list[:self.index+1]
            self.referee.freeze_timers()
        
        # Ajouter une copie de l'état actuel
        self.board_list.append(self.referee.board.copy())
        self.index += 1
        self.check_repetition()

    def check_repetition(self):
        current_board = self.board_list[-1]
        c = 0
        for i in range(len(self.board_list)-1):
            if current_board == self.board_list[i]:
                c+=1
            if c == 2:
                self.referee.state = "repetition"
                break