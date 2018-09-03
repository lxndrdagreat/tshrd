import tdl
from tshrd.utils import wait_for_keys
from tshrd.state_handling import GameData, GameState
from tshrd.characters import Character, create_player


def state(game: GameData, root_console: tdl.Console) -> GameState:

    # minimum points for stats:
    min_power = 1
    min_block = 1
    min_health = 6

    # values
    starting_power = min_power
    starting_block = min_block
    starting_health = min_health
    name = ''
    name_max_length = 12

    # points to spend
    points_left = 8

    active = 'name'

    normal_color = (255, 255, 255)
    active_color = (255, 255, 0)

    while True:
        root_console.clear()

        # page title
        root_console.draw_str(1, 0, 'CREATE YOUR CHARACTER')

        left = 1
        top = 2

        # Player Name
        root_console.draw_str(left, top, f'NAME: {name}', fg=active_color if active == 'name' else normal_color)

        # Power
        top += 2
        power_text = f'POWER: {starting_power}'
        if starting_power > min_power:
            power_text = f'{power_text}  [LEFT] Decrease'
        if points_left > 0:
            power_text = f'{power_text}  [RIGHT] Increase'
        root_console.draw_str(left, top, power_text, fg=active_color if active == 'power' else normal_color)

        # Block
        top += 2
        block_text = f'BLOCK: {starting_block}'
        if starting_block > min_block:
            block_text = f'{block_text}  [LEFT] Decrease'
        if points_left > 0:
            block_text = f'{block_text}  [RIGHT] Increase'
        root_console.draw_str(left, top, block_text, fg=active_color if active == 'block' else normal_color)

        # Health
        top += 2
        health_text = f'HEALTH: {starting_health}'
        if starting_health > min_health:
            health_text = f'{health_text}  [LEFT] Decrease'
        if points_left > 0:
            health_text = f'{health_text}  [RIGHT] Increase'
        root_console.draw_str(left, top, health_text, fg=active_color if active == 'health' else normal_color)

        # show remaining points
        top += 4
        root_console.draw_str(left, top, f'POINTS REMAINING: {points_left}', fg=(255, 0, 0))

        # Help
        top += 4
        root_console.draw_str(left, top, '*Use UP/DOWN to change active field.')

        tdl.flush()

        if active == 'name':
            alpha = list('qwertyuiopasdfghjklzxcvbnm')
            alpha.extend([
                    'ESCAPE',
                    'DOWN',
                    'UP',
                    'SPACE',
                    'BACKSPACE',
                    'ENTER',
                    '1'
                ])
            user_input = wait_for_keys(alpha)

            if user_input == 'ESCAPE':
                # quit the game
                return GameState.CLOSE

            elif user_input == 'ENTER':
                # start game with current stats
                break

            elif user_input == '1':
                # TODO: remove this shortcut
                name = 'Player'
                starting_health = 10
                starting_power = 4
                starting_block = 2
                break

            elif user_input == 'UP':
                active = 'health'

            elif user_input == 'DOWN':
                active = 'power'

            elif user_input == 'BACKSPACE':
                if len(name) > 0:
                    name = name[:-1]

            elif len(name) < name_max_length:
                if user_input == 'SPACE':
                    name += ' '

                else:
                    name += user_input

        elif active == 'power':
            user_input = wait_for_keys([
                'ESCAPE',
                'DOWN',
                'UP',
                'LEFT',
                'RIGHT',
                'ENTER'
            ])

            if user_input == 'ESCAPE':
                # quit the game
                return GameState.CLOSE

            elif user_input == 'ENTER':
                # start game with current stats
                break

            elif user_input == 'UP':
                active = 'name'

            elif user_input == 'DOWN':
                active = 'block'

            elif user_input == 'LEFT' and starting_power > min_power:
                starting_power -= 1
                points_left += 1

            elif user_input == 'RIGHT' and points_left > 0:
                starting_power += 1
                points_left -= 1

        elif active == 'block':
            user_input = wait_for_keys([
                'ESCAPE',
                'DOWN',
                'UP',
                'LEFT',
                'RIGHT',
                'ENTER'
            ])

            if user_input == 'ESCAPE':
                # quit the game
                return GameState.CLOSE
            elif user_input == 'ENTER':
                # start game with current stats
                break

            elif user_input == 'UP':
                active = 'power'

            elif user_input == 'DOWN':
                active = 'health'

            elif user_input == 'LEFT' and starting_block > min_block:
                starting_block -= 1
                points_left += 1

            elif user_input == 'RIGHT' and points_left > 0:
                starting_block += 1
                points_left -= 1

        elif active == 'health':
            user_input = wait_for_keys([
                'ESCAPE',
                'DOWN',
                'UP',
                'LEFT',
                'RIGHT',
                'ENTER'
            ])

            if user_input == 'ESCAPE':
                # quit the game
                return GameState.CLOSE

            elif user_input == 'ENTER':
                # start game with current stats
                break

            elif user_input == 'UP':
                active = 'block'

            elif user_input == 'DOWN':
                active = 'name'

            elif user_input == 'LEFT' and starting_health > min_health:
                starting_health -= 1
                points_left += 1

            elif user_input == 'RIGHT' and points_left > 0:
                starting_health += 1
                points_left -= 1

    # make the player

    game.the_player = create_player(name, starting_power, starting_block, starting_health)

    # start game
    return GameState.ROOM
