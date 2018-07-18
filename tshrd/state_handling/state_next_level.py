import tdl
from tshrd.utils import wait_for_keys, draw_player_status_bar
from tshrd.state_handling import GameData, GameState


def state(game: GameData, root_console: tdl.Console) -> GameState:

    root_console.clear()
    game.build_map()
    text = f'Dungeon Level {game.current_level}'
    root_console.draw_str(int(root_console.width / 2) - int(len(text) / 2), 15, text, fg=(255, 255, 0), bg=None)

    tdl.flush()

    user_input = wait_for_keys([
        'ESCAPE',
        'ENTER',
        'SPACE'
    ])

    if user_input == 'ESCAPE':
        return GameState.CLOSE

    return GameState.ROOM
