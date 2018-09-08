import tdl
from tshrd.state_handling import GameData, GameState


def state(game: GameData, root_console: tdl.Console) -> GameState:
    if game.current_room.encountered:
        return GameState.ROOM
    game.advance_turn()
    log_text = f'You encounter a trap. You lose 1 turn and consume food.'
    game.log(log_text, (149, 108, 53))
    game.current_room.encountered = True
    return GameState.ROOM
