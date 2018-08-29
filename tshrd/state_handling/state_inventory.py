import tdl
from tshrd.utils import wait_for_keys
from tshrd.state_handling import GameData, GameState
from tshrd.inventory import Inventory, Item, HealthPotion, Potion, Weapon, Armor
from tshrd.characters import Character


def state(game: GameData, root_console: tdl.Console) -> GameState:

    player: Character = game.the_player

    # create panels
    inventory_panel = tdl.Console(int((root_console.width - 2) * .7), root_console.height - 2)
    inventory_panel.set_colors(fg=(220, 220, 220), bg=(0, 0, 50))
    equipped_panel = tdl.Console(int((root_console.width - 2) * .3), 30)
    equipped_panel.set_colors(fg=(220, 220, 220), bg=(0, 30, 0))
    # height = root height - heading x2 - space between panels - equipment panel height
    tooltip_panel = tdl.Console(equipped_panel.width, root_console.height - 34)
    tooltip_panel.set_colors(fg=(255, 255, 255), bg=(10, 10, 10))
    tooltip_panel.set_mode('scroll')

    selected_index = 0
    current_top = 0

    while True:
        # clear console
        root_console.clear()

        # titles
        root_console.draw_str(1, 0, 'INVENTORY', fg=(255, 255, 0), bg=None)
        root_console.draw_str(int((root_console.width - 2) * .7 + 2), 0, 'EQUIPPED', fg=(255, 255, 0), bg=None)
        root_console.draw_str(int((root_console.width - 2) * .7 + 2), 32, 'TOOLTIP', fg=(200, 200, 200), bg=None)

        # inventory list panel
        inventory_panel.clear()

        text_y = 0
        text_x = 0
        max_lines = root_console.height - 2
        for index, item in enumerate(player.inventory.items[current_top:current_top+max_lines]):
            text_color = (200, 200, 200)
            item_text = f'{str(item)}'
            if index + current_top == selected_index:
                text_color = (255, 255, 0)
                if item.is_equipable():
                    if item == player.weapon or item == player.armor:
                        # unequip
                        item_text = f'{item_text}  [U]nequip'
                    else:
                        # equip
                        item_text = f'{item_text}  [E]quip'
                if item.can_activate_outside_encounter():
                    item_text = f'{item_text}  [A]ctivate'
                if item != player.weapon and item != player.armor:
                    item_text = f'{item_text}  [D]rop'
            inventory_panel.draw_str(text_x, text_y, item_text, fg=text_color)
            text_y += 1

        # draw panel
        root_console.blit(inventory_panel, 1, 1)

        # equipped panel
        equipped_panel.clear()
        # TODO: handle long lines of text
        equipped_panel.draw_str(1, 1, 'WEAPON:')
        equipped_panel.draw_str(2, 2, f'{player.weapon.name if player.weapon else "EMPTY"}')
        equipped_panel.draw_str(1, 4, 'ARMOR:')
        equipped_panel.draw_str(2, 5, f'{player.armor.name if player.armor else "EMPTY"}')

        root_console.blit(equipped_panel, 2 + inventory_panel.width, 1)

        # draw tooltip
        tooltip_panel.clear()
        if selected_index < len(player.inventory.items):
            selected_item: Item = player.inventory.items[selected_index]
            if selected_item.description:
                tooltip_panel.move(0, 0)
                tooltip_panel.print_str(selected_item.description)
        root_console.blit(tooltip_panel, 2 + inventory_panel.width, 33)

        tdl.flush()

        user_input = wait_for_keys([
            'ESCAPE',
            'UP',
            'DOWN',
            'ENTER',
            'i',
            'u',
            'e',
            'a',
            'd'
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

        elif user_input == 'd' and selected_index < len(player.inventory.items):
            # drop the item from inventory
            # TODO: add item to room like treasure?
            selected_item: Item = player.inventory.items[selected_index]
            game.log(f'Dropped {selected_item.name} to the floor. Gone Forever.')
            player.inventory.remove_item(selected_item)
            if selected_index >= len(player.inventory.items):
                selected_index = max(0, len(player.inventory.items) - 1)

        elif user_input == 'a' and selected_index < len(player.inventory.items):
            item_to_use: Item = player.inventory.items[selected_index]
            if item_to_use.can_activate_outside_encounter() and item_to_use.can_activate_on_player():
                result_text = item_to_use.activate(player)
                if result_text:
                    player.inventory.remove_item(item_to_use)
                    game.log(result_text, fg=(255, 255, 0))

        elif user_input == 'u' and selected_index < len(player.inventory.items):
            item_to_unequip: Item = player.inventory.items[selected_index]
            if not player.is_item_equipped(item_to_unequip):
                continue
            response = player.unequip_item(item_to_unequip)
            if response:
                game.log(response)

        elif user_input == 'e' and selected_index < len(player.inventory.items):
            item_to_equip: Item = player.inventory.items[selected_index]
            if not item_to_equip.is_equipable() or player.is_item_equipped(item_to_equip):
                continue
            for_log = player.equip_item(item_to_equip)
            if for_log:
                game.log(for_log)

        elif user_input == 'ESCAPE' or user_input == 'i':
            return GameState.ROOM

    return GameState.ROOM
