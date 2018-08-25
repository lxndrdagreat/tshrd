import tdl
from tshrd.utils import wait_for_keys
from tshrd.state_handling import GameData, GameState
from tshrd.inventory import Inventory, Item, HealthPotion, Potion, Weapon, Armor
from tshrd.characters import Character


def state(game: GameData, root_console: tdl.Console) -> GameState:

    # TODO: actions for selected item
    # TODO: tooltip for selected item (on key press?)

    player: Character = game.the_player

    # create panels
    inventory_panel = tdl.Console(int((root_console.width - 2) * .7), root_console.height - 2)
    inventory_panel.set_colors(fg=(220, 220, 220), bg=(0, 0, 50))
    equipped_panel = tdl.Console(int((root_console.width - 2) * .3), root_console.height - 2)
    equipped_panel.set_colors(fg=(220, 220, 220), bg=(0, 50, 0))

    selected_index = 0
    current_top = 0

    while True:
        # clear console
        root_console.clear()

        # titles
        root_console.draw_str(1, 0, 'INVENTORY', fg=(255, 255, 0), bg=None)
        root_console.draw_str(int((root_console.width - 2) * .7 + 2), 0, 'EQUIPPED', fg=(255, 255, 0), bg=None)

        # inventory list panel
        inventory_panel.clear()

        text_y = 0
        text_x = 0
        max_lines = root_console.height - 2
        for index, item in enumerate(player.inventory.items[current_top:current_top+max_lines]):
            text_color = (200, 200, 200)
            if index + current_top == selected_index:
                text_color = (255, 255, 0)
            inventory_panel.draw_str(text_x, text_y, f'{str(item)}', fg=text_color)
            text_y += 1

        # draw panel
        root_console.blit(inventory_panel, 1, 1)

        # equipped panel
        # equipped_panel.clear()
        # equipped_panel.print_str(f'WEAPON: {player.weapon.name if player.weapon else "EMPTY"}\n')
        # equipped_panel.print_str(f'ARMOR: {player.armor.name if player.armor else "EMPTY"}\n')
        #
        # root_console.blit(equipped_panel, 2 + inventory_panel.width, 1)

        tdl.flush()

        user_input = wait_for_keys([
            'ESCAPE',
            'UP',
            'DOWN',
            'ENTER',
            'i'
        ])

        if user_input == 'UP':
            # scroll selection up and scroll list up if needed
            if current_top <= 0 and selected_index <= 0:
                # TODO: maybe loop around to bottom of list?
                continue
            selected_index -= 1
            if selected_index < current_top:
                current_top = selected_index

        elif user_input == 'DOWN':
            # scroll selection down and scroll list down if needed
            if selected_index >= len(player.inventory.items) - 1:
                # TODO: maybe loop around to top of list?
                continue

            selected_index += 1
            if selected_index >= current_top + max_lines:
                current_top = selected_index

        if user_input == 'ESCAPE' or user_input == 'i':
            return GameState.ROOM

    return GameState.ROOM
