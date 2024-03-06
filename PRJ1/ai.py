import random



class AI:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty

    def choose_move(self, game_state):
        # All cells are valid choices now, as we can stack moves
        all_cells = [(r, c) for r in range(game_state.board_size) for c in range(game_state.board_size)]
        # Choose a random cell from all available cells
        return random.choice(all_cells)
