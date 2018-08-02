import tdl
from tshrd.utils import wait_for_keys
from tshrd.state_handling import GameData, GameState


def state(game: GameData, root_console: tdl.Console) -> GameState:

    root_console.clear()

    # titles
    root_console.draw_str(1, 0, 'INVENTORY', fg=(255, 255, 0), bg=None)
    root_console.draw_str(int((root_console.width - 2) * .7 + 2), 0, 'EQUIPPED', fg=(255, 255, 0), bg=None)

    # inventory list panel
    inventory_panel = tdl.Console(int((root_console.width - 2) * .7), root_console.height - 2)
    inventory_panel.set_colors(fg=(220, 220, 220), bg=(0, 0, 50))
    inventory_panel.clear()

    # draw panel
    root_console.blit(inventory_panel, 1, 1)

    # equipped panel
    equipped_panel = tdl.Console(int((root_console.width - 2) * .3), root_console.height - 2)
    equipped_panel.set_colors(fg=(220, 220, 220), bg=(0, 50, 0))
    equipped_panel.clear()
    root_console.blit(equipped_panel, 2 + inventory_panel.width, 1)

    tdl.flush()

    user_input = wait_for_keys([
        'ESCAPE',
        'UP',
        'DOWN',
        'LEFT',
        'RIGHT',
        'ENTER',
        'i'
    ])

    # if user_input == 'UP':
    #     return GameState.MOVE_NORTH
    #
    # elif user_input == 'DOWN':
    #     return GameState.MOVE_SOUTH
    #
    # elif user_input == 'LEFT':
    #     return GameState.MOVE_WEST
    #
    # elif user_input == 'RIGHT':
    #     return GameState.MOVE_EAST

    if user_input == 'ESCAPE' or user_input == 'i':
        return GameState.ROOM

    return GameState.ROOM
