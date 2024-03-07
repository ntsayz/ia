import pygame
from ai import AI

class GameController:
    def __init__(self, game_state, gui, player1_type='AI', player2_type='AI'):
        self.game_state = game_state
        self.gui = gui
        self.current_player = 1
        self.score = 100
        self.players = {1: player1_type, 2: player2_type}
        self.ai = AI()
        self.selected_source = None
        self.selected_destination = None

    def handle_event(self, event):
        # Only handle mouse clicks for human players
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        x, y = pos
        row = y // self.gui.cell_size
        col = x // self.gui.cell_size

        if 0 <= row < self.gui.grid_size and 0 <= col < self.gui.grid_size:
            if self.selected_source is None:  # First click selects the source
                self.selected_source = (row, col)
                self.gui.highlight_cell(row, col)
            else:  # Second click selects the destination
                self.selected_destination = (row, col)
                self.gui.highlight_cell(row, col)

                # Perform the move if it's valid
                if self.validate_move(self.selected_source, self.selected_destination):
                    self.perform_move(self.selected_source, self.selected_destination)

                # Reset the selections after the move
                self.selected_source = None
                self.selected_destination = None
        self.game_state.print_board()

    def validate_move(self, source, destination):
        # For now
        return True

    def perform_move(self, source, destination):
        # Move the stack from source to destination
        self.game_state.board[destination[0]][destination[1]].extend(self.game_state.board[source[0]][source[1]])
        self.game_state.board[source[0]][source[1]] = []
        self.gui.draw_board()
        pygame.display.flip()

        # Switch players after a successful move
        self.switch_player()



    def handle_ai_turn(self):
        pygame.time.wait(400)  # Artificial delay for better user experience

        # Ask the AI to choose a move based on the current game state and which player the AI is
        ai_move = self.ai.choose_move(self.game_state, self.current_player)
        if ai_move:
            # Unpack the source and destination from the move chosen by the AI
            src, dest = ai_move
            src_row, src_col = src
            dest_row, dest_col = dest

            # Optionally, highlight the source and destination cells for visual feedback
            self.gui.highlight_cell(src_row, src_col, highlight_color=(255, 0, 0))
            pygame.time.wait(200)  # Small delay to see the highlight
            self.gui.highlight_cell(dest_row, dest_col, highlight_color=(255, 255, 0))

            # Perform the move
            # This assumes that 'move_pieces' method updates the game state correctly according to the rules of your game
            self.move_pieces(src_row, src_col, dest_row, dest_col)

            # Redraw the board to reflect the move
            self.gui.redraw_board()  # Ensure this method updates the GUI based on the current game state

            # Switch to the next player after the AI's turn
            self.switch_player()

        # Optionally, print the board state to the console for debugging
        self.game_state.print_board()

    def move_pieces(self, src_row, src_col, dest_row, dest_col):
        # Move stack from src to dest
        stack_to_move = self.game_state.board[src_row][src_col]
        self.game_state.board[dest_row][dest_col].extend(stack_to_move)
        self.game_state.board[src_row][src_col] = []

        self.gui.redraw_board()

    def switch_player(self):
        # Switch to the next player
        self.current_player = 1 if self.current_player == 2 else 2
        # If the next player is AI, handle the AI turn
        self.check_and_handle_ai_turn()

    def check_and_handle_ai_turn(self):
        if self.players[self.current_player] == 'AI':
            self.handle_ai_turn()

    def update_gui(self):
        self.gui.draw_control_panel(self.current_player, self.score)
        self.gui.draw_info_panel(self.current_player, self.score)
