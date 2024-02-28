from game_state import GameState
from game_logic import GameLogic
from ai import AI
from gui import GUI

def main():
    game_state = GameState(board_size=8)
    game_logic = GameLogic(game_state)
    ai_player = AI(difficulty='medium')
    gui = GUI(game_state)
    gui.main_loop()  

if __name__ == "__main__":
    main()
