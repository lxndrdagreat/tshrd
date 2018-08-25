import tdl
from tshrd.state_handling import GameState, GameData
from tshrd.monsters import create_monster_for_level
from tshrd.characters import Character
from tshrd.inventory import Inventory, Item
from tshrd.utils import wait_for_keys
from tshrd.combat import do_attack
import random
import math


def state(game: GameData, root_console: tdl.Console) -> GameState:
    if game.current_room.monster is None:
        monster = game.current_room.monster = create_monster_for_level(game.current_level)
    else:
        monster = game.current_room.monster

    player = game.the_player
    player_x = int(root_console.width / 2)
    player_y = 10
    monster_y = 0
    monster_x = player_x
    top = 5
    left = 5
    room_draw_width = game.room_draw_width
    room_draw_height = game.room_draw_height
    center_x = int(math.floor(room_draw_width / 2))
    center_y = int(math.floor(room_draw_height / 2))

    # if you flee a monster and come back, it will return to full health
    monster.reset()

    game.log(f'You encounter a {monster.name}!', (255, 0, 0))

    fighting = True
    did_flee = False

    while fighting:

        # clear
        root_console.clear()

        # draw room
        root_console.draw_rect(left, top, room_draw_width, room_draw_height, '.', (255, 255, 255), (0, 0, 0))
        root_console.draw_frame(left, top, room_draw_width, room_draw_height, '#', (255, 255, 255), (0, 0, 0))
        if game.current_room.north:
            root_console.draw_char(left + center_x, top, '.', (255, 255, 255), (0, 0, 0))
        if game.current_room.south:
            root_console.draw_char(left + center_x, top + room_draw_height - 1, '.', (255, 255, 255), (0, 0, 0))
        if game.current_room.west:
            root_console.draw_char(left, top + center_y, '.', (255, 255, 255), (0, 0, 0))
        if game.current_room.east:
            root_console.draw_char(left + room_draw_width - 1, top + center_y, '.', (255, 255, 255), (0, 0, 0))

        # draw player
        p_x = center_x
        p_y = center_y
        if game.previous_room:
            if game.previous_room == game.current_room.north:
                # came from the north
                p_y = 2
            elif game.previous_room == game.current_room.south:
                # came from the south
                p_y = room_draw_height - 3
            elif game.previous_room == game.current_room.east:
                # came from the east
                p_x = room_draw_width - 3
            elif game.previous_room == game.current_room.west:
                # came from the west
                p_x = 2
        root_console.draw_char(left + p_x, top + p_y, player.tile, bg=None, fg=(255, 255, 255))

        # draw monster
        root_console.draw_char(left + center_x, top + center_y, monster.tile, bg=None, fg=(255, 0, 0))

        # draw the log
        game.draw_log(root_console)

        tried_to_flee = False

        # Draw Monster Information
        root_console.draw_str(monster_x, monster_y, f'{monster.name}')
        root_console.draw_str(monster_x, monster_y + 1, f'HP: {monster.health} / {monster.max_health}')

        # Draw Player Information
        root_console.draw_str(player_x, player_y, f'{player.name}')
        root_console.draw_str(player_x, player_y + 1, f'HP: {player.health} / {player.max_health}')
        root_console.draw_str(player_x, player_y + 2, '[A] Attack')
        root_console.draw_str(player_x, player_y + 3, '[1] Skill')
        root_console.draw_str(player_x, player_y + 4, '[2] Skill')
        root_console.draw_str(player_x, player_y + 5, '[U] Use Item')
        root_console.draw_str(player_x, player_y + 6, '[F] Flee')

        tdl.flush()

        user_input = wait_for_keys(['ESCAPE', 'a', '1', '2', 'f', 'u'])

        if user_input == 'ESCAPE':
            return GameState.CLOSE

        if user_input == 'a':
            game.log(f'You attack the {monster.name}...')
            results = do_attack(player, monster)
            if not results.critical_miss:
                game.log(f'...and hit for {results.damage} damage.')
            else:
                game.log(f'...and miss.')
        elif user_input == '1':
            pass
        elif user_input == '2':
            pass
        elif user_input == 'f':
            game.log('You attempt to flee.')
            tried_to_flee = True
            chance_to_flee = 80
            roll = random.randrange(0, 100)
            if roll <= chance_to_flee:
                did_flee = True
        elif user_input == 'u':
            state_usable_inventory(game, root_console)

        if monster.health <= 0:
            fighting = False
            game.log(f'You slay the {monster.name}!')
            continue

        # monster's turn
        # monster gets a turn even if the player succeeded at fleeing
        results = do_attack(monster, player)
        game.log(f'The {monster.name} attacks...', (255, 0, 0))
        if not results.critical_miss:
            game.log(f'...and hits for {results.damage} damage')
        else:
            game.log(f'...and misses you.')

        if player.health <= 0:
            fighting = False
            # cannot flee if you are dead, Jim
            did_flee = False
            continue
        elif tried_to_flee and not did_flee:
            game.log("You failed to run away", (255, 0, 0))
        elif tried_to_flee and did_flee:
            fighting = False
            continue

    if did_flee:
        # fleeing does not mark the encounter as complete
        text = f'You run away from the {monster.name}, returning to the previous room.'
        game.log(text)
        game.current_room = game.previous_room
        game.previous_room = None
        return GameState.ROOM

    game.current_room.encountered = True

    # killed the monster! yay!
    if monster.health <= 0:
        # TODO reward the player for slaying the monster
        text = f'You have killed the {monster.name}!'
        game.log(text)
        return GameState.ROOM

    # player is dead
    return GameState.GAME_OVER


def state_usable_inventory(game: GameData, root_console: tdl.Console):
    # Used for player-inventory interaction during the combat

    the_player = game.the_player
    # get user's inventory that is allowed to be used in combat
    available_items = [item for item in the_player.inventory.items if item.can_activate_in_combat()]

    # set up console
    inventory_console = tdl.Console(int(root_console.width / 2), root_console.height - 23)
    inventory_console.set_colors(fg=(200, 200, 200), bg=(0, 0, 90))

    selected_index = 0
    current_top = 0

    while True:
        inventory_console.clear()
        inventory_console.draw_str(1, 0, 'COMBAT ITEMS:')

        text_y = 2
        text_x = 1
        counter = 1
        max_lines = 14

        if len(available_items) > 0:
            for index, item in enumerate(available_items[current_top:current_top+max_lines]):
                text_color = (200, 200, 200)
                if index + current_top == selected_index:
                    text_color = (255, 255, 0)
                inventory_console.draw_str(text_x, text_y, f'{str(item)}', fg=text_color)
                text_y += 1
                counter += 1
        else:
            inventory_console.draw_str(text_x, text_y, 'YOU HAVE NO ITEMS THAT CAN BE USED')

        # blit to root and flush
        root_console.blit(inventory_console, int(root_console.width / 2), 0)
        tdl.flush()

        user_input = wait_for_keys(['ENTER', 'ESCAPE', 'SPACE', 'UP', 'DOWN'])
        if user_input in ('ENTER', 'SPACE', ):
            if len(available_items) == 0:
                continue
            item_to_use: Item = available_items[selected_index]
            result_text = None
            if item_to_use.can_activate_on_player():
                result_text = item_to_use.activate(the_player)
            elif item_to_use.can_activate_on_monster():
                result_text = item_to_use.activate(game.current_room.monster)
            if result_text:
                the_player.inventory.remove_item(item_to_use)
                game.log(result_text, fg=(255, 255, 0))
            break

        elif user_input == 'ESCAPE':
            # nevermind
            return False

        elif user_input == 'UP':
            # scroll selection up and scroll list up if needed
            if current_top <= 0 and selected_index <= 0:
                # TODO: maybe loop around to bottom of list?
                continue
            selected_index -= 1
            if selected_index < current_top:
                current_top = selected_index

        elif user_input == 'DOWN':
            # scroll selection down and scroll list down if needed
            if selected_index >= len(available_items) - 1:
                # TODO: maybe loop around to top of list?
                continue

            selected_index += 1
            if selected_index >= current_top + max_lines:
                current_top = selected_index

    return True
