import pygame
from game_state import GameState
from game_controller import GameController


class GUI:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        pygame.init()
        self.window_size = (1000, 900)
        self.ai_types = ['MiniMax', 'AlphaBeta', 'MCTS', 'Variation of MCTS']
        self.difficulties = ['Easy', 'Medium', 'Hard']
        self.current_ai_type = 'MiniMax'
        self.current_difficulty = 'Medium'
        self.screen = pygame.display.set_mode(self.window_size)
        self.game_controller = GameController(self.game_state, self)
        self.cell_size = 100
        self.grid_size = self.game_state.board_size
        self.control_panel_height = 100
        self.info_panel_width = 200
        self.font = pygame.font.Font(None, 36)
        self.draw_board()
        self.game_started = False

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
                    cell_color = (255, 0, 0)  # Red
                elif (i, j) == bottom_right:
                    cell_color = (0, 0, 255)  # Blue

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
        for ai_type in self.ai_types:
            color = (255, 255, 0) if ai_type == self.current_ai_type else (255, 255, 255)
            text_surface = self.font.render(ai_type, True, color)
            rect = text_surface.get_rect(center=(self.window_size[0] // 3, y_start))
            self.screen.blit(text_surface, rect)
            y_start += 50

        y_start = 100
        for difficulty in self.difficulties:
            color = (255, 255, 0) if difficulty == self.current_difficulty else (255, 255, 255)
            text_surface = self.font.render(difficulty, True, color)
            rect = text_surface.get_rect(center=(2 * self.window_size[0] // 3, y_start))
            self.screen.blit(text_surface, rect)
            y_start += 50

        start_button_rect = pygame.Rect(self.window_size[0] - 200, self.window_size[1] - 100, 200, 100)
        pygame.draw.rect(self.screen, (0, 255, 0), start_button_rect)  # Green button

        start_text = self.font.render('START GAME', True, (0, 0, 0))
        self.screen.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 35))

        pygame.display.flip()  # Update the display to show the menu

    def handle_ai_menu_selection(self, pos):
        # Assuming menu items are spaced 50 pixels apart and start at 100 pixels down
        # Adjust these values based on your actual layout
        ai_type_index = (pos[1] - 100) // 50 if pos[0] < self.window_size[0] // 2 else None
        difficulty_index = (pos[1] - 100) // 50 if pos[0] >= self.window_size[0] // 2 else None

        if ai_type_index is not None and 0 <= ai_type_index < len(self.ai_types):
            self.current_ai_type = self.ai_types[ai_type_index]
        if difficulty_index is not None and 0 <= difficulty_index < len(self.difficulties):
            self.current_difficulty = self.difficulties[difficulty_index]

        self.draw_ai_selection_menu()  # Redraw the menu with the updated selection

    def draw_control_panel(self, current_player, score):
        #
        control_panel_rect = pygame.Rect(0, self.grid_size * self.cell_size,
                                         self.window_size[0] - self.info_panel_width, self.control_panel_height)
        pygame.draw.rect(self.screen, (200, 200, 200), control_panel_rect)
        control_text_surface = self.font.render(f'Player Turn: {current_player}', True, (0, 0, 0))
        self.screen.blit(control_text_surface, (10, self.grid_size * self.cell_size + 10))
        control_text_surface = self.font.render(f'{self.game_controller.players[1]} vs {self.game_controller.players[2]}', True, (0, 0, 0))
        self.screen.blit(control_text_surface, (10, self.grid_size * self.cell_size + 30))
        ai_text = f'AI: {self.current_ai_type}' if self.current_ai_type else 'AI: Not selected'
        difficulty_text = f'Difficulty: {self.current_difficulty}'
        ai_text_surface = self.font.render(ai_text, True, (0, 0, 0))
        difficulty_text_surface = self.font.render(difficulty_text, True, (0, 0, 0))
        self.screen.blit(ai_text_surface, (10, self.grid_size * self.cell_size + 50))
        self.screen.blit(difficulty_text_surface, (10, self.grid_size * self.cell_size + 80))


    def draw_info_panel(self, current_player, score):
        info_panel_rect = pygame.Rect(self.window_size[0] - self.info_panel_width, 0, self.info_panel_width,
                                      self.window_size[1])
        pygame.draw.rect(self.screen, (200, 200, 200), info_panel_rect)
        info_text_surface = self.font.render(f'FOCUS', True, (0, 0, 0))
        self.screen.blit(info_text_surface, (self.window_size[0] - self.info_panel_width + 10, 10))

    def highlight_cell(self, row, col, highlight_color=(255, 255, 0), duration=100):
        rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, highlight_color, rect, 5)  # thick border for highlight
        # if no duration, don't wait and don't flip the display
        if duration > 0:
            pygame.display.flip()  # updating the display to show the highlight move
            pygame.time.wait(duration)

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
                        self.game_controller.handle_event(event)

            # Only draw the start button and AI selection menu if the game has not started
            if not self.game_started:
                self.draw_ai_selection_menu()

            pygame.display.flip()
        pygame.quit()


