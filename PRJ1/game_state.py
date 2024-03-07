import copy


class GameState:
    def __init__(self, board_size=8):
        self.board_size = board_size
        self.board = self.initialize_board()

    def initialize_board(self):
        # Start with an empty board of the correct size
        board = [[[] for _ in range(self.board_size)] for _ in range(self.board_size)]

        for row in range(1, 7):
            for col in range(1, 7):
                if row % 2 == 1:  # Odd rows: 1, 3, 5
                    if col % 2 == 1:  # Odd columns: 1, 3, 5
                        board[row][col] = [1] if (col == 1 or col == 5) else [2]
                    else:  # Even columns: 2, 4, 6
                        board[row][col] = [2] if (col == 2 or col == 6) else [1]
                else:  # Even rows: 2, 4, 6
                    if col % 2 == 1:  # Odd columns: 1, 3, 5
                        board[row][col] = [2] if (col == 1 or col == 5) else [1]
                    else:  # Even columns: 2, 4, 6
                        board[row][col] = [1] if (col == 2 or col == 6) else [2]

        return board

    def make_move(self, move, player_number):
        src, dest = move
        print(f"Moving stack from {src} to {dest}.")
        src_row, src_col = src
        dest_row, dest_col = dest

        # Check if the move is valid (the top piece belongs to the player making the move)
        if self.board[src_row][src_col] and self.board[src_row][src_col][-1] == player_number:
            # Move the stack from source to destination
            self.board[dest_row][dest_col].extend(self.board[src_row][src_col])
            self.board[src_row][src_col] = []

            # Check for and handle stacks larger than 5 pieces, if necessary
            # This is just an example and might need adjusting based on your game's rules
            if len(self.board[dest_row][dest_col]) > 5:
                self.board[dest_row][dest_col] = self.board[dest_row][dest_col][-5:]

        # Return 'self' to indicate the state has been updated
        # Note: Depending on your design, you might want to return a new GameState instance instead
        return self

    def get_legal_moves(self):
        return []

    def is_game_over(self):
        return False

    def update_cell(self, row, col, value):
        self.board[row][col].append(value)

    def print_board(self):
        for row in self.board:
            print('|' + '|'.join([str(cell) if cell is not None else ' ' for cell in row]) + '|')
        print()

    def copy(self):
        return copy.deepcopy(self)

