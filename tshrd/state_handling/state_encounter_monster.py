import tdl
from tshrd.state_handling import GameState, GameData
from tshrd.monsters import create_monster_for_level
from tshrd.characters import Character
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

    # if you flee a monster and come back, it will return to full health
    monster.reset()

    root_console.clear()
    text = f'You encounter a {monster.name}!'
    root_console.draw_str(int(root_console.width / 2) - int(len(text) / 2), 10, text)
    tdl.flush()
    if wait_for_keys() == 'ESCAPE':
        # quit game
        return GameState.CLOSE
    root_console.clear()
    tdl.flush()

    # Set up log area
    log_inner_width: int = math.floor(root_console.width / 2) - 2
    log_inner_height: int = root_console.height - 2
    log_console = tdl.Console(log_inner_width, log_inner_height)
    log_console.set_colors(fg=(0, 0, 0), bg=(200, 200, 200))
    log_console.clear()
    log_console.set_mode('scroll')
    log_lines = []

    fighting = True
    did_flee = False

    while fighting:

        root_console.clear()
        root_console.draw_frame(int(math.floor(root_console.width / 2)), 0, log_inner_width + 2, root_console.height, '#',
                                fg=(255, 255, 255))

        # add new lines to the log
        for line in log_lines:
            log_console.print_str(line)
            log_console.print_str('\n')
        log_lines = []
        root_console.blit(log_console, int(math.floor(root_console.width / 2)) + 1, 1)

        tried_to_flee = False

        # Draw Monster Information
        root_console.draw_str(1, 0, f'{monster.name}')
        root_console.draw_str(1, 1, f'HP: {monster.health} / {monster.max_health}')

        # Draw Player Information
        root_console.draw_str(1, root_console.height - 6, f'{player.name}')
        root_console.draw_str(1, root_console.height - 5, f'HP: {player.health} / {player.max_health}')
        root_console.draw_str(1, root_console.height - 4, '[A] Attack')
        root_console.draw_str(1, root_console.height - 3, '[1] Skill')
        root_console.draw_str(1, root_console.height - 2, '[2] Skill')
        root_console.draw_str(1, root_console.height - 1, '[F] Flee')

        tdl.flush()

        user_input = wait_for_keys(['ESCAPE', 'a', '1', '2', 'f'])

        if user_input == 'ESCAPE':
            return GameState.CLOSE

        if user_input == 'a':
            log_lines.append(f'You attack the {monster.name}...')
            # results = player.attack_character(monster)
            results = do_attack(player, monster)
            if not results.critical_miss:
                log_lines.append(f'...and hit for {results.damage} damage.')
            else:
                log_lines.append(f'...and miss.')
        elif user_input == '1':
            pass
        elif user_input == '2':
            pass
        elif user_input == 'f':
            log_lines.append('You attempt to flee.')
            tried_to_flee = True
            chance_to_flee = 80
            roll = random.randrange(0, 100)
            if roll <= chance_to_flee:
                did_flee = True

        if monster.health <= 0:
            fighting = False
            log_lines.append(f'You slay the {monster.name}!')
            continue

        # monster's turn
        # monster gets a turn even if the player succeeded at fleeing
        results = do_attack(monster, player)
        log_lines.append(f'The {monster.name} attacks...')
        if not results.critical_miss:
            log_lines.append(f'...and hits for {results.damage} damage')
        else:
            log_lines.append(f'...and misses you.')

        if player.health <= 0:
            fighting = False
            # cannot flee if you are dead, Jim
            did_flee = False
            continue
        elif tried_to_flee and not did_flee:
            log_lines.append("You failed to run away")
        elif tried_to_flee and did_flee:
            fighting = False
            continue

    for line in log_lines:
        game.log(line)

    if did_flee:
        # fleeing does not mark the encounter as complete
        root_console.clear()
        text = f'You run away from the {monster.name}, returning to the previous room.'
        game.log(text)
        root_console.draw_str(root_console.width / 2 - len(text) / 2, 10, text)
        tdl.flush()
        if wait_for_keys() == 'ESCAPE':
            # escape
            return GameState.CLOSE
        game.current_room = game.previous_room
        game.previous_room = None
        return GameState.ROOM

    game.current_room.encountered = True

    # killed the monster! yay!
    if monster.health <= 0:
        # TODO reward the player for slaying the monster
        root_console.clear()
        text = f'You have killed the {monster.name}!'
        game.log(text)
        root_console.draw_str(root_console.width / 2 - len(text) / 2, 10, text)
        tdl.flush()
        if wait_for_keys() == 'ESCAPE':
            # escape
            return GameState.CLOSE
        return GameState.ROOM

    # player is dead
    return GameState.GAME_OVER
