import pygame
from ai import AI

class GameController:
    def __init__(self, game_state, gui, player1_type='Human', player2_type='AI'):
        self.game_state = game_state
        self.gui = gui
        self.current_player = 2
        self.score = 100
        self.players = {1: player1_type, 2: player2_type}
        self.ai = AI()

    def handle_event(self, event):
        # Only handle mouse clicks for human players
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        # Process click only if it's within the game board
        x, y = pos
        row = y // self.gui.cell_size
        col = x // self.gui.cell_size
        self.gui.highlight_cell(row, col,highlight_color=(0, 0, 255))
        if 0 <= row < self.gui.grid_size and 0 <= col < self.gui.grid_size:
            # Update the game state with the new move
            self.gui.update_game_state(row, col, self.current_player)
            # After a move, switch to the next player
            self.switch_player()
        self.game_state.print_board()

    def handle_ai_turn(self):
        # delay for UX
        pygame.time.wait(400)

        ai_move = self.ai.choose_move(self.game_state)
        if ai_move:
            row, col = ai_move
            self.gui.highlight_cell(row, col,highlight_color=(255, 0, 0))
            # Update the game state with the AI's move
            self.gui.update_game_state(row, col, self.current_player)
            # Switch to the next player after the AI move
            self.switch_player()
        self.game_state.print_board()

    def switch_player(self):
        # Switch to the next player
        self.current_player = 1 if self.current_player == 2 else 2
        # If the next player is AI, handle the AI turn
        self.check_and_handle_ai_turn()

    def check_and_handle_ai_turn(self):
        if self.players[self.current_player] == 'AI':
            # Small delay for AI turn to simulate thinking delay (optional)
            self.handle_ai_turn()

    def update_gui(self):
        # Redraw the control panel and info panel with updated info
        self.gui.draw_control_panel(self.current_player, self.score)
        self.gui.draw_info_panel(self.current_player, self.score)
