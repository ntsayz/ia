import pygame
from ai import AI
import copy

class GameController:
    def __init__(self, game_state, gui):
        self.game_state = game_state
        self.gui = gui
        self.current_player = 1
        self.score = 100
        self.players = [AI(), AI()]
        self.ai_player_1 = None  # Initialize to None
        self.ai_player_2 = None  # Initialize to None
        self.set_player_types()
        self.selected_source = None
        self.selected_destination = None
        self.is_human = False
        self.tip_algorithms = ['MiniMax', 'AlphaBeta', 'MCTS', 'Variation of MCTS']
        self.suggestion_shown = False
        self.last_suggested_move = None

    def set_player_types(self):
        # Update player types based on GUI selection
        mode = self.gui.current_game_mode
        if mode == 'Human vs Human':
            self.players = {1: 'Human', 2: 'Human'}
            self.is_human = True
        elif mode == 'Human vs AI':
            self.players = {1: 'Human', 2: 'AI'}
            self.ai_player_2 = AI(strategy=self.gui.current_ai_type, difficulty=self.gui.current_difficulty)

        elif mode == 'AI vs AI':
            self.players = {1: 'AI', 2: 'AI'}
            self.ai_player_1 = AI(strategy=self.gui.current_ai_type, difficulty=self.gui.current_difficulty)
            self.ai_player_2 = AI(strategy=self.gui.current_ai_type_2, difficulty=self.gui.current_difficulty)

    def handle_event(self, event):
        if self.gui.game_started:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # Cycle through algorithms upwards
                    self.gui.current_tip_algorithm_index = (self.gui.current_tip_algorithm_index - 1) % len(self.tip_algorithms)
                    self.gui.draw_info_panel(self.current_player, self.score)
                elif event.key == pygame.K_DOWN:
                    # Cycle through algorithms downwards
                    self.gui.current_tip_algorithm_index = (self.gui.current_tip_algorithm_index + 1) % len(self.tip_algorithms)
                    self.gui.draw_info_panel(self.current_player, self.score)
                elif event.key == pygame.K_s:
                    self.show_move_suggestion()

    def handle_mouse_click(self, pos):
        x, y = pos
        row = y // self.gui.cell_size
        col = x // self.gui.cell_size

        if 0 <= row < self.gui.grid_size and 0 <= col < self.gui.grid_size:
            if self.selected_source is None:  # Attempting to select a source
                if self.can_select_source(row, col):
                    self.selected_source = (row, col)
                    self.gui.highlight_cell(row, col)
                    self.highlight_possible_moves(row, col)
            else:  # Source is already selected, attempting to select a destination
                self.selected_destination = (row, col)
                if self.validate_move(self.selected_source, self.selected_destination):
                    self.perform_move(self.selected_source, self.selected_destination)
                    self.selected_source = None
                    self.selected_destination = None
                    self.gui.redraw_board()
                else:
                    # Invalid move, reset selection
                    self.gui.highlight_cell(*self.selected_source,
                                            highlight_color=(255, 0, 0))  # Highlight source as invalid
                    self.selected_source = None
                    self.selected_destination = None

        self.game_state.print_board()

    def validate_move(self, source, destination, preview=False):
        row_s, col_s = source
        row_d, col_d = destination

        if not (0 <= row_s < self.gui.grid_size and 0 <= col_s < self.gui.grid_size and
                0 <= row_d < self.gui.grid_size and 0 <= col_d < self.gui.grid_size):
            return False  # Out of bounds

        if source == destination:
            return False  # No move

        # Check for sideline piece being moved onto the board
        if source in [(7, 7), (7, 0)] and self.game_state.is_playable(row_d, col_d):
            # Allow moving sidelined piece to any playable position
            return self.game_state.board[row_s][col_s][-1] == self.current_player

        stack = self.game_state.board[row_s][col_s]
        if not stack or stack[-1] != self.current_player:
            return False  # Empty stack or not player's piece

        stack_size = len(stack)
        move_distance = abs(row_s - row_d) + abs(col_s - col_d)
        if move_distance != stack_size:
            return False  # Stack size and move distance mismatch

        if not (row_s == row_d or col_s == col_d):
            return False  # Non-orthogonal move

        return True

    def perform_move(self, source, destination):
        if not self.validate_move(source, destination):
            print("Invalid move.")
            return

        row_s, col_s = source
        row_d, col_d = destination
        moving_stack = self.game_state.board[row_s][col_s]

        self.game_state.board[row_d][col_d].extend(moving_stack)
        self.game_state.board[row_s][col_s] = []
        self.game_state.redistribute_excess_pieces()

        self.gui.draw_board()
        pygame.display.flip()

        self.switch_player()


    def handle_ai_turn(self):
        # Determine which AI object to use based on the current player
        ai = self.ai_player_1 if self.current_player == 1 else self.ai_player_2

        if ai:  # If the current player is an AI
            # pygame.time.wait(200)  # Optionally wait a bit to simulate thinking

            ai_move = ai.choose_move(self.game_state, self.current_player)
            if ai_move:
                src, dest = ai_move
                src_row, src_col = src
                dest_row, dest_col = dest

                print(f"AI Player {self.current_player} moved from {src} to {dest}.")

                # Highlight source and destination cells
                self.gui.highlight_cell(src_row, src_col, highlight_color=(255, 0, 0))
                # pygame.time.wait(100)  # Optionally wait a bit to simulate move animation
                self.gui.highlight_cell(dest_row, dest_col, highlight_color=(255, 255, 0))

                # Perform the move
                self.move_pieces(src_row, src_col, dest_row, dest_col)

                self.gui.redraw_board()

                self.switch_player()

            self.game_state.print_board()

    def move_pieces(self, src_row, src_col, dest_row, dest_col):
        # move stack from src to dest
        stack_to_move = self.game_state.board[src_row][src_col]
        self.game_state.board[dest_row][dest_col].extend(stack_to_move)
        self.game_state.board[src_row][src_col] = []
        self.game_state.redistribute_excess_pieces()

        self.gui.redraw_board()

    def switch_player(self):
        self.current_player = 1 if self.current_player == 2 else 2


        # Debug print to trace player switching
        print(f"Player switched to {self.current_player}")

        if not self.is_human:
            # AI turn check and handling
            if (self.current_player == 1 and self.ai_player_1) or (self.current_player == 2 and self.ai_player_2):
                self.check_and_handle_ai_turn()

    def is_ai_vs_ai_mode(self):
        return self.players[1] == 'AI' and self.players[2] == 'AI'

    def check_and_handle_ai_turn(self):
        # Determine which AI is playing based on the current player
        if self.current_player == 1 and self.ai_player_1:
            self.handle_ai_turn()
        elif self.current_player == 2 and self.ai_player_2:
            self.handle_ai_turn()

    def show_move_suggestion(self):
        # Generate move suggestion based on the current algorithm
        algo = self.gui.tip_algorithms[self.gui.current_tip_algorithm_index]
        suggested_move = self.generate_move_suggestion(algo, self.game_state, self.current_player)

        if suggested_move:
            src, dest = suggested_move
            # Highlight source in purple
            self.gui.highlight_cell(src[0], src[1], highlight_color=(128, 0, 128))
            # Highlight destination in purple
            self.gui.highlight_cell(dest[0], dest[1], highlight_color=(102, 0, 102))
            pygame.display.flip()

    def generate_move_suggestion(self, algorithm, game_state, player_number):
        # Placeholder for generating a move based on the selected algorithm
        # This method should invoke the corresponding algorithm from the AI class and return the suggested move
        # Example:
        ai1 = AI()
        return ai1.choose_move(game_state, player_number)

    def update_gui(self):
        self.gui.draw_control_panel(self.current_player, self.score)
        self.gui.draw_info_panel(self.current_player, self.score)

    def highlight_possible_moves(self, row, col):
        if (row, col) in [(7, 7), (7, 0)]:
            # Highlight all playable positions for sidelined pieces
            for r in range(self.gui.grid_size):
                for c in range(self.gui.grid_size):
                    if self.game_state.is_playable(r, c):
                        self.gui.highlight_cell(r, c, highlight_color=(0, 255, 0))
        else:
            stack_size = len(self.game_state.board[row][col])
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                for distance in range(1, stack_size + 1):
                    new_row, new_col = row + dx * distance, col + dy * distance
                    if 0 <= new_row < self.gui.grid_size and 0 <= new_col < self.gui.grid_size and self.validate_move(
                            (row, col), (new_row, new_col), preview=True):
                        self.gui.highlight_cell(new_row, new_col, highlight_color=(0, 255, 0))

    def can_select_source(self, row, col):
        stack = self.game_state.board[row][col]
        # Can select if the stack is not empty and the top piece belongs to the current player
        return bool(stack) and stack[-1] == self.current_player

