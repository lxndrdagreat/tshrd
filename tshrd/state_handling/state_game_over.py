import tdl
from tshrd.state_handling import GameData, GameState
from tshrd.utils import wait_for_keys


def state(game: GameData, root_console: tdl.Console) -> GameState:
    root_console.clear()
    text = f'You have died. Would you like to play again?'
    root_console.draw_str(root_console.width / 2 - len(text) / 2, 10, text)
    text = 'Y/N'
    root_console.draw_str(root_console.width / 2 - len(text) / 2, 12, text)
    tdl.flush()
    choice = wait_for_keys(['ESCAPE', 'y', 'n'])
    if choice == 'ESCAPE' or choice == 'n':
        # quit game
        return GameState.CLOSE
    root_console.clear()
    tdl.flush()
    return GameState.GAME_RESTART
