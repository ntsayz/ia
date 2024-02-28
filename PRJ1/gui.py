import pygame
from game_state import GameState
from game_controller import GameController

class GUI:
    def __init__(self, game_state):
        self.game_state = game_state
        pygame.init()
        self.window_size = (1000, 900)
        self.screen = pygame.display.set_mode(self.window_size)
        self.cell_size = 100
        self.grid_size = self.game_state.board_size  
        self.control_panel_height = 100
        self.info_panel_width = 200 
        self.font = pygame.font.Font(None, 36)
        self.draw_board()  

    def draw_board(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                cell_color = (255, 255, 255) if self.game_state.board[i][j] is None else self.game_state.board[i][j]
                pygame.draw.rect(self.screen, cell_color, rect)

     
        self.draw_control_panel(0, 0)  

        self.draw_info_panel(0, 0)

    def draw_control_panel(self, current_player, score):
        control_panel_rect = pygame.Rect(0, self.grid_size * self.cell_size, self.window_size[0] - self.info_panel_width, self.control_panel_height)
        pygame.draw.rect(self.screen, (180, 180, 180), control_panel_rect)
        control_text_surface = self.font.render(f'Player Turn: {current_player}', True, (0, 0, 0))
        self.screen.blit(control_text_surface, (10, self.grid_size * self.cell_size + 10))

    def draw_info_panel(self, current_player, score):
        info_panel_rect = pygame.Rect(self.window_size[0] - self.info_panel_width, 0, self.info_panel_width, self.window_size[1])
        pygame.draw.rect(self.screen, (200, 200, 200), info_panel_rect)
        info_text_surface = self.font.render(f'Score: {score}', True, (0, 0, 0))
        self.screen.blit(info_text_surface, (self.window_size[0] - self.info_panel_width + 10, 10))

    def update_game_state(self, row, col, player):
        self.game_state.board[row][col] = player  
        self.draw_board()  # Redraw board to reflect the updated state

    def main_loop(self):
        running = True
        game_controller = GameController(self.game_state, self)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    game_controller.handle_event(event)

            pygame.display.flip()
        pygame.quit()

