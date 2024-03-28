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
        # Handling moves for normal gameplay
        for row in range(game_state.board_size):
            for col in range(game_state.board_size):
                if self.is_playable(row, col):
                    stack = game_state.board[row][col]
                    if stack and stack[-1] == player_number:
                        stack_size = len(stack)
                        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        for dx, dy in directions:
                            # Check positions based on stack size, but don't include current position in distance
                            target_row = row + dx * stack_size
                            target_col = col + dy * stack_size
                            if 0 <= target_row < game_state.board_size and 0 <= target_col < game_state.board_size:
                                if self.is_playable(target_row, target_col):
                                    valid_moves.append(((row, col), (target_row, target_col)))

        # Handling reserved pieces
        sideline_src = (7, 7) if player_number == 1 else (7, 0)
        if game_state.board[sideline_src[0]][sideline_src[1]]:
            for row in range(game_state.board_size):
                for col in range(game_state.board_size):
                    if self.is_playable(row, col) and not (
                            (row, col) in [(7, 7), (7, 0), (6, 7), (6, 0)]):  # Avoid placing in special cells
                        valid_moves.append((sideline_src, (row, col)))

        return valid_moves

    # TODO way too simplistic, change!
    def evaluate_state(self, game_state, player_number):
        score = 0
        opponent_number = 2 if player_number == 1 else 1

        # Scoring for pieces on the board
        for row in range(game_state.board_size):
            for col in range(game_state.board_size):
                stack = game_state.board[row][col]
                if stack:
                    if stack[-1] == player_number:
                        score += 10 + 5 * len(stack)
                    else:
                        score -= 5 * len(stack)

        # Scoring for reserved and captured pieces
        reserved_location = (7, 7) if player_number == 1 else (7, 0)
        captured_location = (6, 7) if player_number == 1 else (6, 0)
        score += 20 * len(game_state.board[reserved_location[0]][reserved_location[1]])  # Value for each reserved piece
        score += 15 * len(
            game_state.board[captured_location[0]][captured_location[1]])  # Value for each captured opponent piece
        score += random.uniform(-0.1, 0.1)
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
