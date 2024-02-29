class GameState:
    def __init__(self, board_size=8):
        self.board_size = board_size
        self.board = self.initialize_board()

    def initialize_board(self):
        return [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

    def make_move(self, move):
        pass

    def get_legal_moves(self):
        return []

    def is_game_over(self):
        return False
    
    # In GameState class
    def update_cell(self, row, col, value):
        self.board[row][col] = value

