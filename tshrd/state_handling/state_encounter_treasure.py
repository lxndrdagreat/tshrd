import tdl
from tshrd.state_handling import GameData, GameState


def state(game: GameData, root_console: tdl.Console) -> GameState:
    print('You find treasure!')
    game.current_room.encountered = True
    return GameState.ROOM
