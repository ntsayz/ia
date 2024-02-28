import pygame

class GameController:
    def __init__(self, game_state, gui):
        self.game_state = game_state
        self.gui = gui
        self.current_player = 1
        self.score = 100 

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        # Determine if click is in control or info panel
        if pos[0] > self.gui.window_size[0] - self.gui.info_panel_width:
            print("Clicked in info panel")
            # Info panel click
        elif pos[1] > self.gui.grid_size * self.gui.cell_size:
            print("Clicked in control panel")
            # Control panel click
        else:
            # Game board click
            x, y = pos
            row = y // self.gui.cell_size
            col = x // self.gui.cell_size
            if 0 <= row < self.gui.grid_size and 0 <= col < self.gui.grid_size:
                self.current_player = 1 if self.current_player == 2 else 2
                self.gui.update_game_state(row, col, self.current_player)

    def update_gui(self):
        # Update GUI with current game state information
        self.gui.draw_control_panel(self.current_player, self.score)
        self.gui.draw_info_panel(self.current_player, self.score)
