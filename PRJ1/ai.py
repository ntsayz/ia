import random
import math

from mcts import MCTSNode


class AI:
    def __init__(self, strategy='MiniMax', difficulty='Medium'):
        self.strategy = strategy
        self.difficulty = difficulty
        self.max_depth = 2
        self.max_depth = 2 if difficulty == 'Medium' else (1 if difficulty == 'Easy' else 3)

    def choose_move(self, game_state, player_number):
        if self.strategy == 'MiniMax':
            print("Minimax strategy ", player_number)
            return self.choose_minimax_move(game_state, player_number)
        elif self.strategy == 'AlphaBeta':
            print("AlphaBeta strategy ", player_number)
            return self.choose_minimax_move(game_state, player_number, use_alpha_beta=True)
        elif self.strategy == 'MCTS':
            return self.mcts(game_state, player_number)
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
            if use_alpha_beta:
                eval = self.minimax_alpha_beta(game_state_copy, self.max_depth, player_number, -math.inf, math.inf,
                                               True)
            else:
                eval = self.minimax(game_state_copy, self.max_depth, player_number, True)
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move

    def mcts(self, game_state, player_number):
        root_node = MCTSNode(game_state=game_state, player_number=player_number)
        for iteration in range(100):
            print(f"Iteration: {iteration + 1}")
            node = root_node
            state = game_state.copy()

            # Selection
            steps = 0
            while not node.is_terminal_node() and node.untried_moves == []:
                node = node.select_child()
                state = state.make_move(node.move, player_number)
                steps += 1
            print(f"  Selection ended after {steps} steps.")

            # Expansion
            if node.untried_moves:
                print("  Expansion step.")
                node = node.expand()

            # Simulation
            simulation_steps = 0
            while  simulation_steps < 600:
                possible_moves = self.get_valid_moves(state, player_number)
                if not possible_moves:
                    break  # Exit the simulation loop, as no further moves can be made
                move = random.choice(possible_moves)
                state = state.make_move(move, player_number)
                simulation_steps += 1
            print(f"  Simulation ended after {simulation_steps} steps.")

            # Backpropagation
            backprop_steps = 0
            result = state.get_result(player_number)
            while node is not None:
                effective_result = result if node.player_number == player_number else -result
                node.update(effective_result)
                node = node.parent
                backprop_steps += 1
            print(f"  Backpropagation updated {backprop_steps} nodes.")

        if root_node.children:
            best_move = max(root_node.children, key=lambda c: c.wins / c.visits).move  # Updated to also consider visits
            print(f"Best move chosen from root: {best_move}")
            return best_move
        else:
            print("No children nodes were expanded, choosing a random or default move.")
            possible_moves = self.get_valid_moves(game_state, player_number)
            if possible_moves:
                return random.choice(possible_moves)  # Choose a random move if possible
            else:
                return None



    def choose_mcts_variant_move(self, game_state, player_number):

        return random.choice(self.get_valid_moves(game_state, player_number))[0]

    def minimax(self, game_state, depth, player_number, maximizing_player):
        if depth == 0 or game_state.is_game_over():
            return self.evaluate_state_simpler(game_state, player_number)

        if maximizing_player:
            max_eval = -float('inf')
            for move in self.get_valid_moves(game_state, player_number):
                game_state_copy = game_state.copy()
                game_state_copy.make_move(move, player_number)
                eval = self.minimax(game_state_copy, depth - 1, player_number, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            opponent_number = 2 if player_number == 1 else 1
            for move in self.get_valid_moves(game_state, opponent_number):
                game_state_copy = game_state.copy()
                game_state_copy.make_move(move, opponent_number)
                eval = self.minimax(game_state_copy, depth - 1, player_number, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def minimax_alpha_beta(self, game_state, depth, player_number, alpha=-math.inf, beta=math.inf,
                           maximizing_player=True):
        if depth == 0 or game_state.is_game_over():
            return self.evaluate_state(game_state, player_number)

        if maximizing_player:
            max_eval = -math.inf
            for move in self.get_valid_moves(game_state, player_number):
                game_state_copy = game_state.make_move(move, player_number)
                eval = self.minimax_alpha_beta(game_state_copy, depth - 1, player_number, alpha, beta, False)
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
                eval = self.minimax_alpha_beta(game_state_copy, depth - 1, player_number, alpha, beta, True)
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

    def evaluate_state_simpler(self, game_state, player_number):
        score = 0

        for row in range(game_state.board_size):
            for col in range(game_state.board_size):
                stack = game_state.board[row][col]
                if stack:
                    if stack[-1] == player_number:
                        score += 1 + 0.1 * len(stack)

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

    def simulate_with_heuristic(self, state, player_number):
        simulation_steps = 0
        while not state.is_game_over() and simulation_steps < 200:  # Limiting steps for safety
            possible_moves = self.get_valid_moves(state, player_number)
            if not possible_moves:
                break  # No more moves available

            # Evaluate each move with the heuristic
            move_scores = []
            for move in possible_moves:
                simulated_state = state.copy().make_move(move, player_number)
                score = self.evaluate_state(simulated_state, player_number)
                move_scores.append((score, move))

            # Normalize scores to probabilities
            max_score = max(move_scores, key=lambda x: x[0])[0]
            probabilities = [math.exp(score - max_score) for score, _ in move_scores]
            total = sum(probabilities)
            probabilities = [p / total for p in probabilities]

            # Select move based on biased probability
            move = random.choices([move for _, move in move_scores], weights=probabilities, k=1)[0]
            state = state.make_move(move, player_number)

            simulation_steps += 1
            player_number = 3 - player_number  # Switch player



"""
    def mcts(self, game_state, player_number):
        root_node = MCTSNode(game_state=game_state, player_number=player_number)
        for iteration in range(10):
            print(f"Iteration: {iteration + 1}")
            node = root_node
            state = game_state.copy()

            # Selection
            steps = 0
            while not node.is_terminal_node() and node.untried_moves == []:
                node = node.select_child()
                state = state.make_move(node.move, player_number)
                steps += 1
            print(f"  Selection ended after {steps} steps.")

            # Expansion
            if node.untried_moves:
                print("  Expansion step.")
                node = node.expand()

            # Simulation
            self.simulate_with_heuristic(state, player_number)

            # Backpropagation
            backprop_steps = 0
            result = state.get_result(player_number)
            while node is not None:
                effective_result = result if node.player_number == player_number else -result
                node.update(effective_result)
                node = node.parent
                backprop_steps += 1
            print(f"  Backpropagation updated {backprop_steps} nodes.")

        if root_node.children:
            best_move = max(root_node.children, key=lambda c: c.wins / c.visits).move  # Updated to also consider visits
            print(f"Best move chosen from root: {best_move}")
            return best_move
        else:
            print("No children nodes were expanded, choosing a random or default move.")
            possible_moves = self.get_valid_moves(game_state, player_number)
            if possible_moves:
                return random.choice(possible_moves)  # Choose a random move if possible
            else:
                return None

"""