import time

import pygame
from game_state import GameState
from game_controller import GameController


class GUI:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        pygame.init()
        self.window_size = (1000, 900)
        self.ai_types = ['MiniMax', 'AlphaBeta', 'MCTS', 'Variation of MCTS']
        self.game_modes = ['Human vs Human', 'Human vs AI', 'AI vs AI']
        self.current_game_mode = 'AI vs AI'
        self.difficulties = ['Easy', 'Medium', 'Hard']
        self.current_ai_type = 'MiniMax'  # Default AI type for player 1
        self.current_ai_type_2 = 'MiniMax'  # Default AI type for player 2, used in AI vs AI
        self.current_difficulty = 'Hard'
        self.screen = pygame.display.set_mode(self.window_size)
        self.game_controller = GameController(self.game_state, self)
        self.cell_size = 100
        self.game_ended = False
        self.game_started = False
        self.start_time = time.time()
        self.tip_algorithms = ['MiniMax', 'AlphaBeta', 'MCTS', 'Variation of MCTS']
        self.current_tip_algorithm_index = 0
        self.grid_size = self.game_state.board_size
        self.control_panel_height = 100
        self.info_panel_width = 200
        self.font = pygame.font.Font(None, 36)
        self.draw_board()

    def reset_game(self):
        # Reinitialize game state
        self.game_state = GameState(board_size=8)  # Assuming board size is constant, adjust if necessary
        self.game_controller = GameController(self.game_state, self)

        # Reset other relevant variables
        self.game_ended = False
        self.game_started = False
        self.start_time = time.time()

        # Optionally, reset any other variables or states here

        # Redraw the board to reflect the reset state
        self.draw_board()

        # Restart the game loop
        self.main_loop()

    def draw_board(self):
        bottom_left = (self.grid_size - 1, 0)
        bottom_right = (self.grid_size - 1, self.grid_size - 1)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # rectangle for each cell
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)

                # background color for each cell
                if not self.is_playable(i, j):
                    cell_color = (100, 100, 100)  # gray
                else:
                    cell_color = (255, 255, 255)  # white for playable cells

                # colors for the store and out of the game cells
                if (i, j) == bottom_left:
                    cell_color = (100, 120, 120)  # g
                elif (i, j) == bottom_right:
                    cell_color = (100, 120, 120)  # g

                pygame.draw.rect(self.screen, cell_color, rect)

                # visual rep of the stack in each cell
                cell_stack = self.game_state.board[i][j]
                stack_height = self.cell_size // 6
                for k in range(len(cell_stack)):
                    piece_color = (0, 0, 255) if cell_stack[k] == 1 else (255, 255, 0)  # Blue for 1, yellow for 2
                    piece_x = j * self.cell_size + self.cell_size // 2
                    piece_y = (i + 1) * self.cell_size - (k + 1) * stack_height + (stack_height // 2)
                    pygame.draw.circle(self.screen, piece_color, (piece_x, piece_y), self.cell_size // 12)

                # Highlight the borders of playable cells
                if self.is_playable(i, j):
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # black border for playable cells

        self.draw_control_panel(self.game_controller.current_player, self.game_controller.score)
        self.draw_info_panel(self.game_controller.current_player, self.game_controller.score)
        self.draw_timer()

    def draw_timer(self):
        if not self.game_ended:  # Only update the timer if the game hasn't ended
            elapsed_time = int(time.time() - self.start_time)
            timer_text_surface = self.font.render(f'Time: {elapsed_time}s', True, (0, 255, 0))
            self.screen.blit(timer_text_surface, (self.window_size[0] - self.info_panel_width + 10, 130))

    def is_playable(self, row, col):
        non_playable_cells = [
            (0, 0), (0, 1), (0, 6), (0, 7),
            (1, 0), (1, 7),
            (6, 0), (6, 7),
            (7, 0), (7, 1), (7, 6), (7, 7)
        ]

        return (row, col) not in non_playable_cells

    def draw_ai_selection_menu(self):
        self.screen.fill((0, 0, 0))  # Clear screen or use a background color

        y_start = 100
        for game_mode in self.game_modes:
            color = (255, 255, 0) if game_mode == self.current_game_mode else (255, 255, 255)
            text_surface = self.font.render(game_mode, True, color)
            rect = text_surface.get_rect(center=(self.window_size[0] // 2, y_start))
            self.screen.blit(text_surface, rect)
            y_start += 50

        self.draw_start_button()

        if self.current_game_mode != 'Human vs Human':
            self.draw_ai_options(y_start, self.window_size[0] // 4, is_second_ai=False)  # Draw options for the first AI

        if self.current_game_mode == 'AI vs AI':
            # Adjust y_start based on how many options were displayed above
            #y_start += (len(self.ai_types) + len(self.difficulties)) * 50
            self.draw_ai_options(y_start,  self.window_size[0] - self.window_size[0] // 4, is_second_ai=True)

        pygame.display.flip()  # Update the display to show the menu

    def draw_game_end_block(self, winner):
        end_game_rect = pygame.Rect(100, 100, 800, 700)
        pygame.draw.rect(self.screen, (0, 0, 0), end_game_rect)
        font = pygame.font.Font(None, 74)
        text_surface = font.render(f'GAME ENDED - Winner: Player {winner}', True, (255, 0, 0))
        self.screen.blit(text_surface, (110, 110))
        elapsed_time = int(time.time() - self.start_time)
        elapsed_time_surface = font.render(f'Time: {elapsed_time} seconds', True, (255, 255, 255))
        self.screen.blit(elapsed_time_surface, (110, 160))

        # Player stats including moves and captures
        font_stats = pygame.font.Font(None, 54)  # Smaller font for stats

        # Using the stack sizes at (6,7) and (6,0) for captures
        player1_captures = len(self.game_state.board[6][7])
        player2_captures = len(self.game_state.board[6][0])

        player1_stats_surface = font_stats.render(
            f'Player 1 - Moves: {self.game_controller.moves_made[1]}, Captures: {player1_captures}', True,
            (255, 255, 255))
        self.screen.blit(player1_stats_surface, (110, 210))

        player2_stats_surface = font_stats.render(
            f'Player 2 - Moves: {self.game_controller.moves_made[2]}, Captures: {player2_captures}', True,
            (255, 255, 255))
        self.screen.blit(player2_stats_surface, (110, 260))

        avg_move_time_p1 = self.game_controller.calculate_average_move_time(1)
        avg_move_time_p2 = self.game_controller.calculate_average_move_time(2)

        # Draw the text for average move time for each player
        font_stats = pygame.font.Font(None, 54)  # Adjust size as needed
        avg_move_time_surface_p1 = font_stats.render(f'Player 1 Avg Move Time: {avg_move_time_p1:.2f}s', True,
                                                     (255, 255, 255))
        avg_move_time_surface_p2 = font_stats.render(f'Player 2 Avg Move Time: {avg_move_time_p2:.2f}s', True,
                                                     (255, 255, 255))

        # Adjust positioning as necessary
        self.screen.blit(avg_move_time_surface_p1, (110, 310))
        self.screen.blit(avg_move_time_surface_p2, (110, 360))

        pygame.display.flip()

    def draw_ai_options(self, y_start, x_start, is_second_ai):
        # Function to draw AI type and difficulty options
        label = 'AI 2 Type:' if is_second_ai else 'AI Type:'
        ai_label_surface = self.font.render(label, True, (255, 255, 255))
        self.screen.blit(ai_label_surface, (x_start - 100, y_start))
        y_start += 50

        for ai_type in self.ai_types:
            current_ai_type = self.current_ai_type_2 if is_second_ai else self.current_ai_type
            color = (255, 255, 0) if ai_type == current_ai_type else (255, 255, 255)
            text_surface = self.font.render(ai_type, True, color)
            rect = text_surface.get_rect(center=(x_start, y_start))
            self.screen.blit(text_surface, rect)
            y_start += 50

        if not is_second_ai:
            label = 'Difficulty:'
            difficulty_label_surface = self.font.render(label, True, (255, 255, 255))
            self.screen.blit(difficulty_label_surface, (2 * x_start - 100, y_start))
            y_start += 50

            for difficulty in self.difficulties:
                color = (255, 255, 0) if difficulty == self.current_difficulty else (255, 255, 255)
                text_surface = self.font.render(difficulty, True, color)
                rect = text_surface.get_rect(center=(2 * x_start, y_start))
                self.screen.blit(text_surface, rect)
                y_start += 50

    def handle_ai_menu_selection(self, pos):
        # Game Mode selection
        game_mode_index = (pos[1] - 100) // 50
        if 0 <= game_mode_index < len(self.game_modes):
            self.current_game_mode = self.game_modes[game_mode_index]

        # Adjust y_start based on game modes displayed
        y_start = 100 + len(self.game_modes) * 50

        # AI Type selection for first AI or only AI
        ai_type_index = (pos[1] - y_start) // 48  - 1
        if 0 <= ai_type_index < len(self.ai_types):
            if self.current_game_mode != 'AI vs AI':
                self.current_ai_type = self.ai_types[ai_type_index]
            else:
                # Distinguish between first and second AI based on screen position
                if pos[0] < self.window_size[0] // 2:
                    self.current_ai_type = self.ai_types[ai_type_index]
                else:
                    self.current_ai_type_2 = self.ai_types[ai_type_index]

        # Difficulty selection
        difficulty_index = (pos[1] - (y_start + len(self.ai_types) * 50)) // 50 - 1
        if 0 <= difficulty_index < len(self.difficulties):
            self.current_difficulty = self.difficulties[difficulty_index]

        self.draw_ai_selection_menu()  # Redraw menu with updated selection

    def draw_control_panel(self, current_player, score):
        control_panel_rect = pygame.Rect(0, self.grid_size * self.cell_size,
                                         self.window_size[0] - self.info_panel_width, self.control_panel_height)
        pygame.draw.rect(self.screen, (200, 200, 200), control_panel_rect)

        # Mode and current player info
        mode_text_surface = self.font.render(f'Mode: {self.current_game_mode}', True, (0, 0, 0))
        self.screen.blit(mode_text_surface, (10, self.grid_size * self.cell_size + 10))

        # Represent current player with a piece color
        player_piece_color = (0, 0, 255) if self.game_controller.current_player == 1 else (
            255, 255, 0)  # Blue for Player 1, Yellow for Player 2
        pygame.draw.circle(self.screen, player_piece_color, (450, self.grid_size * self.cell_size + 30), 15)
        player_text_surface = self.font.render("Player's Turn", True, (0, 0, 0))
        self.screen.blit(player_text_surface, (270, self.grid_size * self.cell_size + 10))

        # AI and difficulty info based on game mode
        if self.current_game_mode == 'Human vs AI':
            ai_text_surface = self.font.render(f'AI (Player 2): {self.current_ai_type}', True, (0, 0, 0))
            self.screen.blit(ai_text_surface, (10, self.grid_size * self.cell_size + 40))

        elif self.current_game_mode == 'AI vs AI':
            ai1_text_surface = self.font.render(f'AI (Player 1): {self.current_ai_type}', True, (0, 0, 0))
            ai2_text_surface = self.font.render(f'AI (Player 2): {self.current_ai_type_2}', True, (0, 0, 0))
            self.screen.blit(ai1_text_surface, (10, self.grid_size * self.cell_size + 40))
            self.screen.blit(ai2_text_surface, (10, self.grid_size * self.cell_size + 70))

        # Show difficulty if AI is involved
        if self.current_game_mode != 'Human vs Human':
            difficulty_text_surface = self.font.render(f'Difficulty: {self.current_difficulty}', True, (0, 0, 0))
            self.screen.blit(difficulty_text_surface, (10, self.grid_size * self.cell_size + 100))

    def draw_info_panel(self, current_player, score):
        info_panel_rect = pygame.Rect(self.window_size[0] - self.info_panel_width, 0, self.info_panel_width,
                                      self.window_size[1])
        pygame.draw.rect(self.screen, (200, 200, 200), info_panel_rect)
        info_text_surface = self.font.render(f'FOCUS', True, (0, 0, 0))
        self.screen.blit(info_text_surface, (self.window_size[0] - self.info_panel_width + 10, 10))
        tips_text_surface = self.font.render('TIPS', True, (0, 0, 0))
        self.screen.blit(tips_text_surface, (self.window_size[0] - self.info_panel_width + 10, 50))
        current_algo_surface = self.font.render(self.tip_algorithms[self.current_tip_algorithm_index], True,
                                                (0, 0, 255))
        self.screen.blit(current_algo_surface, (self.window_size[0] - self.info_panel_width + 10, 90))

    def highlight_cell(self, row, col, highlight_color=(255, 255, 0), duration=100):
        rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, highlight_color, rect, 5)  # thick border for highlight
        # if no duration, don't wait and don't flip the display
        if duration > 0:
            pygame.display.flip()  # updating the display to show the highlight move
            # pygame.time.wait(duration)

    def update_game_state(self, row, col, player):
        if len(self.game_state.board[row][col]) >= 5:
            self.redistribute_pieces(row, col)
        self.game_state.board[row][col].append(player)
        self.draw_board()
        pygame.display.flip()

    def redraw_board(self):
        self.draw_board()
        pygame.display.flip()

    def redistribute_pieces(self, row, col):
        # Initialize bottom corners
        bottom_left = (self.game_state.board_size - 1, 0)
        bottom_right = (self.game_state.board_size - 1, self.game_state.board_size - 1)

        for piece in self.game_state.board[row][col]:
            if piece == 1:
                # Add to bottom-left if not exceeding the stack limit, otherwise ignore or handle differently
                if len(self.game_state.board[bottom_left[0]][bottom_left[1]]) < 5:
                    self.game_state.board[bottom_left[0]][bottom_left[1]].append(1)
            elif piece == 2:
                # Add to bottom-right if not exceeding the stack limit, otherwise ignore or handle differently
                if len(self.game_state.board[bottom_right[0]][bottom_right[1]]) < 5:
                    self.game_state.board[bottom_right[0]][bottom_right[1]].append(2)

        # clear the original cell after redistribution TODO THIS IS VERY WRONG , REPLACE POSITIONS BY THE SOURCE STACK
        self.game_state.board[row][col] = []

    def draw_start_button(self):
        start_button_rect = pygame.Rect(self.window_size[0] - 200, self.window_size[1] - 100, 200, 100)
        pygame.draw.rect(self.screen, (0, 255, 0), start_button_rect)  # Green button

        start_text = self.font.render('START GAME', True, (0, 0, 0))
        self.screen.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 35))

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Check for ESC key
                        self.reset_game()  # Reset and restart the game
                        return

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    # Check if the game has not started and handle the AI menu selection
                    if not self.game_started:
                        # Handle clicks on the AI selection menu
                        self.handle_ai_menu_selection(event.pos)

                        # Assuming the start button position and dimensions from `draw_start_button`
                        if self.window_size[0] - 200 <= x <= self.window_size[0] and \
                                self.window_size[1] - 100 <= y <= self.window_size[1]:
                            self.game_started = True
                            self.draw_board()

                    # If the game has already started, handle game-related events
                    elif self.game_started:
                        self.game_controller.set_player_types()
                        if self.game_controller.is_ai_vs_ai_mode:
                            self.game_controller.handle_event(event)
                        else:
                            self.game_controller.handle_event(event)
                elif event.type == pygame.KEYDOWN:
                    # Directly forward keyboard events to the game controller if the game has started
                    if self.game_started:
                        self.game_controller.handle_event(event)

            if not self.game_ended and self.game_started:
                self.game_ended = self.game_controller.check_game_end()

            # Only draw the start button and AI selection menu if the game has not started
            if not self.game_started:
                self.draw_ai_selection_menu()
            elif not self.game_ended:
                self.draw_timer()
            pygame.display.flip()
        pygame.quit()
