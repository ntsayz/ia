import random



class AI:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty

    def choose_move(self, game_state):
        empty_cells = [(r, c) for r in range(game_state.board_size) for c in range(game_state.board_size) if game_state.board[r][c] is None]
        if empty_cells:
            return random.choice(empty_cells)  # Return a random empty cell
        return None
