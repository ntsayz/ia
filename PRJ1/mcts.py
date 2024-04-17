import math




class MCTSNode:
    def __init__(self, game_state, move=None, parent=None, player_number=None):
        self.game_state = game_state
        self.move = move
        self.parent = parent
        self.player_number = player_number
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = self.get_valid_moves()

    def get_valid_moves(self):
        valid_moves = []
        # Handling moves for normal gameplay
        for row in range(self.game_state.board_size):
            for col in range(self.game_state.board_size):
                if self.is_playable(row, col):
                    stack = self.game_state.board[row][col]
                    if stack and stack[-1] == self.player_number:
                        stack_size = len(stack)
                        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        for dx, dy in directions:
                            # Check positions based on stack size, but don't include current position in distance
                            target_row = row + dx * stack_size
                            target_col = col + dy * stack_size
                            if 0 <= target_row < self.game_state.board_size and 0 <= target_col < self.game_state.board_size:
                                if self.is_playable(target_row, target_col):
                                    valid_moves.append(((row, col), (target_row, target_col)))
        return  valid_moves

    def has_valid_moves(self, player_number):
        valid_moves = []
        for row in range(len(self.game_state.board)):
            for col in range(len(self.game_state.board[row])):
                if self.game_state.is_playable(row, col) and not (row, col) in [(6, 0), (6, 7)]:
                    cell = self.game_state.board[row][col]
                    if cell and cell[-1] == player_number:
                        if self.can_make_a_move_from(row, col):
                            return True  # Found at least one valid move
        return False

    def can_make_a_move_from(self, row, col):
        stack = self.game_state.board[row][col]
        stack_size = len(stack)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dx, dy in directions:
            new_row, new_col = row + dx * stack_size, col + dy * stack_size
            if 0 <= new_row < len(self.game_state.board) and 0 <= new_col < len(self.game_state.board[0]):
                if self.game_state.is_playable(new_row, new_col):
                    return True  # Found a valid direction to move
        return False

    def is_terminal_node(self):
        # Check if the game is over
        return not self.has_valid_moves(self.player_number)

    def update(self, result):
        self.visits += 1
        self.wins += result
        print(f"Update: Node {self.move} - Wins: {self.wins}, Visits: {self.visits}")

    def select_child(self):
        selected_child = sorted(
            self.children,
            key=lambda c: float('inf') if c.visits == 0 else c.wins / c.visits + math.sqrt(
                2 * math.log(self.visits) / c.visits)
        )[-1]
        print(
            f"Select Child: Chose {selected_child.move} with Wins/Visits: {selected_child.wins}/{selected_child.visits}")
        return selected_child

    def expand(self):
        move = self.untried_moves.pop()
        print(f"Expand: Expanding with move {move}")
        next_state = self.game_state.copy().make_move(move, self.player_number)
        child_node = MCTSNode(next_state, move=move, parent=self, player_number=3 - self.player_number)
        self.children.append(child_node)
        print(f"Expand: New child with move {move} added. Total children now: {len(self.children)}")
        return child_node

    def is_playable(self, row, col):
        non_playable_cells = [
            (0, 0), (0, 1), (0, 6), (0, 7),
            (1, 0), (1, 7),
            (6, 0), (6, 7),
            (7, 0), (7, 1), (7, 6), (7, 7)
        ]
        return (row, col) not in non_playable_cells
