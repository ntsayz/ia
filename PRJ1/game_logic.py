class GameLogic:
    def __init__(self, state):
        self.state = state

    def validate_move(self, move):
        return True  

    def update_state(self, move):
        self.state.make_move(move)

    def check_win_condition(self):
        return False  

    def get_winner(self):
        return None
