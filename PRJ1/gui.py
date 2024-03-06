import pygame
from game_state import GameState
from game_controller import GameController

class GUI:
    def __init__(self, game_state : GameState):
        self.game_state = game_state
        pygame.init()
        self.window_size = (1000, 900)
        self.screen = pygame.display.set_mode(self.window_size)
        self.game_controller = GameController(self.game_state, self)
        self.cell_size = 100
        self.grid_size = self.game_state.board_size  
        self.control_panel_height = 100
        self.info_panel_width = 200 
        self.font = pygame.font.Font(None, 36)
        self.draw_board()

    def draw_board(self):
        bottom_left = (self.grid_size - 1, 0)
        bottom_right = (self.grid_size - 1, self.grid_size - 1)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # Define the rectangle for each cell
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)

                # Set the background color for the cell
                if not self.is_playable(i, j):
                    cell_color = (200, 200, 200)  # Non-playable cells colored gray
                else:
                    cell_color = (255, 255, 255)  # Default white color for playable cells

                # Special coloring for the bottom-left and bottom-right cells
                if (i, j) == bottom_left:
                    cell_color = (255, 0, 0)  # Red color for the bottom-left special cell
                elif (i, j) == bottom_right:
                    cell_color = (0, 0, 255)  # Blue color for the bottom-right special cell

                pygame.draw.rect(self.screen, cell_color, rect)

                # Draw the visual representation of the stack in each cell
                cell_stack = self.game_state.board[i][j]
                stack_height = self.cell_size // 6
                for k in range(len(cell_stack)):
                    # Determine the color for each piece
                    piece_color = (0, 0, 255) if cell_stack[k] == 1 else (255, 255, 0)  # Blue for 1, yellow for 2
                    # Calculate the position for each piece in the stack
                    piece_x = j * self.cell_size + self.cell_size // 2
                    piece_y = (i + 1) * self.cell_size - (k + 1) * stack_height + (stack_height // 2)
                    # Draw the piece as a small circle
                    pygame.draw.circle(self.screen, piece_color, (piece_x, piece_y), self.cell_size // 12)

                # Highlight the borders of playable cells
                if self.is_playable(i, j):
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Black border for playable cells

        # Draw control and info panels
        self.draw_control_panel(self.game_controller.current_player, self.game_controller.score)
        self.draw_info_panel(self.game_controller.current_player, self.game_controller.score)

    def is_playable(self, row, col):
        # Non-playable cells are explicitly defined
        non_playable_cells = [
            (0, 0), (0, 1), (0, 6), (0, 7),
            (1, 0), (1, 7),
            (6, 0), (6, 7),
            (7, 0), (7, 1), (7, 6), (7, 7)
        ]

        # The cell is playable if it's not in the list of non-playable cells
        return (row, col) not in non_playable_cells

    def draw_control_panel(self, current_player, score):
        control_panel_rect = pygame.Rect(0, self.grid_size * self.cell_size, self.window_size[0] - self.info_panel_width, self.control_panel_height)
        pygame.draw.rect(self.screen, (200, 200, 200), control_panel_rect)
        control_text_surface = self.font.render(f'Player Turn: {current_player}', True, (0, 0, 0))
        self.screen.blit(control_text_surface, (10, self.grid_size * self.cell_size + 10))

    def draw_info_panel(self, current_player, score):
        info_panel_rect = pygame.Rect(self.window_size[0] - self.info_panel_width, 0, self.info_panel_width, self.window_size[1])
        pygame.draw.rect(self.screen, (200, 200, 200), info_panel_rect)
        info_text_surface = self.font.render(f'Score: {score}', True, (0, 0, 0))
        self.screen.blit(info_text_surface, (self.window_size[0] - self.info_panel_width + 10, 10))

    def highlight_cell(self, row, col, highlight_color=(255, 255, 0), duration=100):
        """Highlight the specified cell for a brief moment."""
        rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, highlight_color, rect, 5)  # Draw a thick border for highlight
        pygame.display.flip()  # Update the display to show the highlight
        pygame.time.wait(duration)

    def update_game_state(self, row, col, player):
        if len(self.game_state.board[row][col]) >= 5:
            # Redistribute pieces
            self.redistribute_pieces(row, col)
        self.game_state.board[row][col].append(player)
        self.draw_board()
        pygame.display.flip()

    def redistribute_pieces(self, row, col):
        # Initialize bottom corners
        bottom_left = (self.game_state.board_size - 1, 0)  # Bottom-left corner
        bottom_right = (self.game_state.board_size - 1, self.game_state.board_size - 1)  # Bottom-right corner

        for piece in self.game_state.board[row][col]:
            if piece == 1:
                # Add to bottom-left if not exceeding the stack limit, otherwise ignore or handle differently
                if len(self.game_state.board[bottom_left[0]][bottom_left[1]]) < 5:
                    self.game_state.board[bottom_left[0]][bottom_left[1]].append(1)
            elif piece == 2:
                # Add to bottom-right if not exceeding the stack limit, otherwise ignore or handle differently
                if len(self.game_state.board[bottom_right[0]][bottom_right[1]]) < 5:
                    self.game_state.board[bottom_right[0]][bottom_right[1]].append(2)

        # Clear the original cell after redistribution
        self.game_state.board[row][col] = []

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.game_controller.handle_event(event)

            pygame.display.flip()
        pygame.quit()


