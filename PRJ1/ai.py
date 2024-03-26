import random
import math


class AI:
    def __init__(self, strategy='MiniMax', difficulty='Medium'):
        self.strategy = strategy
        self.difficulty = difficulty
        self.max_depth = 2
        self.max_depth = 2 if difficulty == 'Medium' else (1 if difficulty == 'Easy' else 3)

    def choose_move(self, game_state, player_number):
        if self.strategy == 'MiniMax':
            return self.choose_minimax_move(game_state, player_number)
        elif self.strategy == 'AlphaBeta':
            return self.choose_minimax_move(game_state, player_number, use_alpha_beta=True)
        elif self.strategy == 'MCTS':
            return self.choose_mcts_move(game_state, player_number)
        elif self.strategy == 'Variation of MCTS':
            return self.choose_mcts_variant_move(game_state, player_number)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

    def choose_minimax_move(self, game_state, player_number, use_alpha_beta=False):
        best_eval = -math.inf
        best_move = None
        for move in self.get_valid_moves(game_state, player_number):
            game_state_copy = game_state.copy()
            game_state_copy.make_move(move,
                                      player_number)
            eval = self.minimax(game_state_copy, self.max_depth, player_number, -math.inf, math.inf, False)
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move

    def choose_mcts_move(self, game_state, player_number):
        # Placeholder for Monte Carlo Tree Search algorithm
        # You will replace this with the actual MCTS implementation
        return random.choice(self.get_valid_moves(game_state, player_number))[0]

    def choose_mcts_variant_move(self, game_state, player_number):
        # Placeholder for a variant of the MCTS algorithm
        # This could be an implementation with different exploration/exploitation balance, etc.
        return random.choice(self.get_valid_moves(game_state, player_number))[0]

    def minimax(self, game_state, depth, player_number, alpha=-math.inf, beta=math.inf, maximizing_player=True):
        if depth == 0 or game_state.is_game_over():
            return self.evaluate_state(game_state, player_number)

        if maximizing_player:
            max_eval = -math.inf
            for move in self.get_valid_moves(game_state, player_number):
                game_state_copy = game_state.make_move(move, player_number)
                eval = self.minimax(game_state_copy, depth - 1, player_number, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            opponent_number = 2 if player_number == 1 else 1
            for move in self.get_valid_moves(game_state, opponent_number):
                game_state_copy = game_state.make_move(move, opponent_number)
                eval = self.minimax(game_state_copy, depth - 1, player_number, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_valid_moves(self, game_state, player_number):
        valid_moves = []
        for row in range(game_state.board_size):
            for col in range(game_state.board_size):
                stack = game_state.board[row][col]
                if stack and stack[-1] == player_number:  # if the top piece belongs to the player
                    stack_size = len(stack)
                    # determina valid move dirs and distances based on stack size
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
                    for d in directions:
                        for distance in range(1, stack_size + 1):
                            new_row, new_col = row + d[0] * distance, col + d[1] * distance
                            if 0 <= new_row < game_state.board_size and 0 <= new_col < game_state.board_size:
                                if self.is_playable(new_row, new_col):
                                    # move cannot result in stack with over 5 pieces
                                    destination_stack_size = len(game_state.board[new_row][new_col])
                                    if destination_stack_size + stack_size <= 5:
                                        valid_moves.append(((row, col), (new_row, new_col)))
        return valid_moves

    # TODO way too simplistic, change!
    def evaluate_state(self, game_state, player_number):
        score = 0
        for row in range(game_state.board_size):
            for col in range(game_state.board_size):
                stack = game_state.board[row][col]
                if stack:
                    if stack[-1] == player_number:  # control of the stack
                        score += 5 * len(stack)  # weight by stack size
                    else:
                        score -= 3 * len(stack)  # opponent's stack diminishes score
        return score
    # todo this has to be dynamic to support multiple board sizes
    def is_playable(self, row, col):
        non_playable_cells = [
            (0, 0), (0, 1), (0, 6), (0, 7),
            (1, 0), (1, 7),
            (6, 0), (6, 7),
            (7, 0), (7, 1), (7, 6), (7, 7)
        ]
        return (row, col) not in non_playable_cells
