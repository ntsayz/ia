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
        #print(f"{player_number} trying moving stack from {src} to {dest}.")
        src_row, src_col = src
        dest_row, dest_col = dest
        # check if the move is valid - top piece needs to belong to the player making the move
        if self.board[src_row][src_col] and self.board[src_row][src_col][-1] == player_number:
            # moving stack TODO change
            self.board[dest_row][dest_col].extend(self.board[src_row][src_col])
            self.board[src_row][src_col] = []

        self.redistribute_excess_pieces()
        return self

    def is_game_over(self):
        return not (self.has_valid_moves(1) or self.has_valid_moves(2))

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

    def redistribute_excess_pieces(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                stack = self.board[row][col]
                if len(stack) > 5:
                    # Calculate how many pieces need to be removed (and therefore, redistributed)
                    excess_count = len(stack) - 5

                    # Separate the excess pieces from the bottom of the stack
                    excess_pieces = stack[:excess_count]

                    # Trim the original stack to a max size of 5
                    self.board[row][col] = stack[excess_count:]

                    # Determine the top piece AFTER trimming for correct redirection
                    top_piece = self.board[row][col][-1]

                    # Redistribute the excess pieces based on their type relative to the top piece
                    for piece in excess_pieces:
                        if piece == top_piece:
                            # Sidelined destination based on top piece
                            sidelined_dest = (7, 7) if top_piece == 1 else (7, 0)
                            self.board[sidelined_dest[0]][sidelined_dest[1]].append(piece)
                        else:
                            # Captured destination based on top piece
                            captured_dest = (6, 7) if top_piece == 1 else (6, 0)
                            self.board[captured_dest[0]][captured_dest[1]].append(piece)

                    # Ensure the sidelined and captured destinations do not exceed max stack size
                    # This part is optional since capturing/sidelining should not create stacks > 5 normally
                    for dest in [(7, 7), (7, 0), (6, 7), (6, 0)]:
                        if len(self.board[dest[0]][dest[1]]) > 5:
                            self.board[dest[0]][dest[1]] = self.board[dest[0]][dest[1]][-5:]

    def get_result(self, player_number):
        print("GETTING RESULT FOR " + str(player_number) + "")
        """
        Evaluates the game result from the perspective of the given player number.
        Returns 1 for a win, -1 for a loss, and 0 for a draw or if the game is still ongoing.
        """
        # If the current player has no valid moves, they lose
        if not self.has_valid_moves(player_number):
            return -1

        # Check if the opponent has no valid moves
        opponent = 2 if player_number == 1 else 1
        if not self.has_valid_moves(opponent):
            return 1

        # If the game is over (maybe there's a method or logic to determine this),
        # and neither player is in a win/loss condition, it's a draw
        if self.is_game_over():
            return 0  # Assuming a draw or game still in progress

        # If game is not over, return 0 to indicate the game is still ongoing
        return 0



    def has_valid_moves(self, player_number):
        valid_moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.is_playable(row, col) and not (row, col) in [(6, 0), (6, 7)]:
                    cell = self.board[row][col]
                    if cell and cell[-1] == player_number:
                        if self.can_make_a_move_from(row, col):
                            return True  # Found at least one valid move
        return False

    def can_make_a_move_from(self, row, col):
        stack = self.board[row][col]
        stack_size = len(stack)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dx, dy in directions:
            new_row, new_col = row + dx * stack_size, col + dy * stack_size
            if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]):
                if self.is_playable(new_row, new_col):
                    return True  # Found a valid direction to move
        return False
