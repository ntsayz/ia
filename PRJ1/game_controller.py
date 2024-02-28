import pygame
from ai import AI

class GameController:
    def __init__(self, game_state, gui, player1_type='Human', player2_type='AI'):
        self.game_state = game_state
        self.gui = gui
        self.current_player = 1  # Start with player 1
        self.score = 100  # Example score, adjust as needed
        self.players = {1: player1_type, 2: player2_type}
        self.ai = AI()  # AI object for making AI moves

    def handle_event(self, event):
        # Only handle mouse clicks for human players
        if event.type == pygame.MOUSEBUTTONDOWN and self.players[self.current_player] == 'Human':
            self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        # Process click only if it's within the game board
        x, y = pos
        row = y // self.gui.cell_size
        col = x // self.gui.cell_size
        if 0 <= row < self.gui.grid_size and 0 <= col < self.gui.grid_size:
            # Update the game state with the new move
            self.gui.update_game_state(row, col, self.current_player)
            # After a move, switch to the next player
            self.switch_player()

    def handle_ai_turn(self):
        ai_move = self.ai.choose_move(self.game_state)
        if ai_move:
            row, col = ai_move
            # Update the game state with the AI's move
            self.gui.update_game_state(row, col, self.current_player)
            # Switch to the next player after the AI move
            #pygame.time.wait(400)
            self.switch_player()

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
