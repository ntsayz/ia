import copy


class GameState:
    def __init__(self, board_size=8):
        self.board_size = board_size
        self.board = self.initialize_board()

    def initialize_board(self):
        board = [[[] for _ in range(self.board_size)] for _ in range(self.board_size)]

        for row in range(1, 7):
            for col in range(1, 7):
                if row % 2 == 1:  # rows: 1, 3, 5
                    if col % 2 == 1:  # columns: 1, 3, 5
                        board[row][col] = [1] if (col == 1 or col == 5) else [2]
                    else:  # even columns: 2, 4, 6
                        board[row][col] = [2] if (col == 2 or col == 6) else [1]
                else:  # even rows: 2, 4, 6
                    if col % 2 == 1:  # odd columns 1, 3, 5
                        board[row][col] = [2] if (col == 1 or col == 5) else [1]
                    else:  # even columns: 2, 4, 6
                        board[row][col] = [1] if (col == 2 or col == 6) else [2]

        return board

    def make_move(self, move, player_number):
        src, dest = move
        # print(f"{player_number} trying moving stack from {src} to {dest}.")
        src_row, src_col = src
        dest_row, dest_col = dest
        # check if the move is valid - top piece needs to belong to the player making the move
        if self.board[src_row][src_col] and self.board[src_row][src_col][-1] == player_number:
            # moving stack TODO change
            self.board[dest_row][dest_col].extend(self.board[src_row][src_col])
            self.board[src_row][src_col] = []

            # check for and handle stacks larger than 5 pieces, if necessary TODO
            if len(self.board[dest_row][dest_col]) > 5:
                self.board[dest_row][dest_col] = self.board[dest_row][dest_col][-5:]

        return self

    def is_game_over(self):
        # TODO finish this
        for player_number in [1, 2]:
            if not self.get_legal_moves(player_number):
                return True
        return False  # If both players can still move, the game is not over.

    def get_legal_moves(self, player_number):
        valid_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                stack = self.board[row][col]
                if stack and stack[-1] == player_number:  # If the top piece belongs to the player
                    stack_size = len(stack)
                    # Determine valid move directions and distances based on stack size
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    for d in directions:
                        for distance in range(1, stack_size + 1):
                            new_row, new_col = row + d[0] * distance, col + d[1] * distance
                            if 0 <= new_row < self.board_size and 0 <= new_col < self.board_size:
                                if self.is_playable(new_row, new_col):  # Ensure move is to a playable cell
                                    # Check if the move does not result in a stack over 5 pieces
                                    destination_stack_size = len(self.board[new_row][new_col])
                                    if destination_stack_size + stack_size <= 5:
                                        valid_moves.append(((row, col), (new_row, new_col)))
        return valid_moves

    def update_cell(self, row, col, value):
        self.board[row][col].append(value)

    def print_board(self):
        for row in self.board:
            print('|' + '|'.join([str(cell) if cell is not None else ' ' for cell in row]) + '|')
        print()

    def copy(self):
        return copy.deepcopy(self)

    def is_playable(self, row, col):
        non_playable_cells = [
            (0, 0), (0, 1), (0, 6), (0, 7),
            (1, 0), (1, 7),
            (6, 0), (6, 7),
            (7, 0), (7, 1), (7, 6), (7, 7)
        ]
        return (row, col) not in non_playable_cells

