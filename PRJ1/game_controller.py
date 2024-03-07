import pygame
from ai import AI

class GameController:
    def __init__(self, game_state, gui, player1_type='Human', player2_type='AI'):
        self.game_state = game_state
        self.gui = gui
        self.current_player = 1
        self.score = 100
        self.players = {1: player1_type, 2: player2_type}
        self.ai = AI()
        self.selected_source = None
        self.selected_destination = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        x, y = pos
        row = y // self.gui.cell_size
        col = x // self.gui.cell_size

        if 0 <= row < self.gui.grid_size and 0 <= col < self.gui.grid_size:
            if self.selected_source is None:  # first click selects the source
                self.selected_source = (row, col)
                self.gui.highlight_cell(row, col)
            else:  # second click selects the destination
                self.selected_destination = (row, col)
                self.gui.highlight_cell(row, col)

                # make the move if it's valid
                if self.validate_move(self.selected_source, self.selected_destination):
                    self.perform_move(self.selected_source, self.selected_destination)

                # reset the selections after the move (this was cluttering the screen)
                self.selected_source = None
                self.selected_destination = None
        self.game_state.print_board()

    def validate_move(self, source, destination):
        # For now
        return True

    def perform_move(self, source, destination):
        # move the stack from source to destination
        self.game_state.board[destination[0]][destination[1]].extend(self.game_state.board[source[0]][source[1]])
        self.game_state.board[source[0]][source[1]] = [] # TODO THIS NEEDS TO GO
        self.gui.draw_board()
        pygame.display.flip()

        # switch players after a successful move
        self.switch_player()



    def handle_ai_turn(self):
        pygame.time.wait(200)

        ai_move = self.ai.choose_move(self.game_state, self.current_player)
        if ai_move:
            src, dest = ai_move
            src_row, src_col = src
            dest_row, dest_col = dest

            print(f"{self.current_player} moved from {src} to {dest}.")

            # highlight source and dest
            self.gui.highlight_cell(src_row, src_col, highlight_color=(255, 0, 0))
            pygame.time.wait(200)
            self.gui.highlight_cell(dest_row, dest_col, highlight_color=(255, 255, 0))

            # make the  move
            self.move_pieces(src_row, src_col, dest_row, dest_col)

            self.gui.redraw_board()

            self.switch_player()

        self.game_state.print_board()

    def move_pieces(self, src_row, src_col, dest_row, dest_col):
        # move stack from src to dest
        stack_to_move = self.game_state.board[src_row][src_col]
        self.game_state.board[dest_row][dest_col].extend(stack_to_move)
        self.game_state.board[src_row][src_col] = []

        self.gui.redraw_board()

    def switch_player(self):

        self.current_player = 1 if self.current_player == 2 else 2

        self.check_and_handle_ai_turn()

    def check_and_handle_ai_turn(self):
        if self.players[self.current_player] == 'AI':
            self.handle_ai_turn()

    def update_gui(self):
        self.gui.draw_control_panel(self.current_player, self.score)
        self.gui.draw_info_panel(self.current_player, self.score)
