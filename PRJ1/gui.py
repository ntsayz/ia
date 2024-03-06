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
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # Define the rectangle for each cell
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                # Set a default cell color, e.g., white
                cell_color = (255, 255, 255)  # White color for cell background
                pygame.draw.rect(self.screen, cell_color, rect)

                # Count 1s and 2s in the stack for the current cell
                ones = self.game_state.board[i][j].count(1)
                twos = self.game_state.board[i][j].count(2)

                # Create the text to display in each cell
                cell_text = f"{ones}/{twos}"
                text_surface = self.font.render(cell_text, True, (0, 0, 0))  # Black color for text
                # Adjust text position to be more centered in the cell if needed
                text_x = j * self.cell_size + (self.cell_size - text_surface.get_width()) / 2
                text_y = i * self.cell_size + (self.cell_size - text_surface.get_height()) / 2
                self.screen.blit(text_surface, (text_x, text_y))

        # Draw control and info panels
        self.draw_control_panel(self.game_controller.current_player, self.game_controller.score)
        self.draw_info_panel(self.game_controller.current_player, self.game_controller.score)

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
        self.game_state.board[row][col].append(player)
        self.draw_board()
        pygame.display.flip()

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


