import tdl
from tshrd.state_handling import GameData, GameState
from tshrd.inventory import generate_random_loot, Item


def state(game: GameData, root_console: tdl.Console) -> GameState:

    if game.current_room.encountered:
        return GameState.ROOM

    game.log('You find treasure!', (255, 255, 0))
    loot_list = generate_random_loot(game.current_level)
    for loot in loot_list:
        if type(loot) is str:
            game.log(f'+1 Food', (255, 255, 0))
            game.the_player.food += 1
        elif loot.name == 'Gold':
            game.log(f'+{loot}', (255, 255, 0))
        else:
            game.log(f'+1 {loot}', (255, 255, 0))
    game.current_room.encountered = True

    return GameState.ROOM
