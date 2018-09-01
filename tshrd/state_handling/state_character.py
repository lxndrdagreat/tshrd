import tdl
from tshrd.utils import wait_for_keys
from tshrd.state_handling import GameData, GameState
from tshrd.characters import Character


def state(game: GameData, root_console: tdl.Console) -> GameState:

    player: Character = game.the_player

    while True:
        root_console.clear()

        # page title
        root_console.draw_str(1, 0, 'CHARACTER')

        left = 1
        top = 2

        # basic player info
        root_console.draw_str(left, top, f'NAME: {player.name}')
        top += 1
        root_console.draw_str(left, top, f'HP: {player.health}/{player.max_health}')
        top += 1
        root_console.draw_str(left,
                              top,
                              f'LEVEL {player.level}  ({player.experience}/{player.experience_to_next_level}XP)')
        top += 1
        root_console.draw_str(left, top, f'FOOD: {player.food}')

        # base stats
        top += 3
        root_console.draw_str(left, top, f'POWER: {player.power}')
        top += 1
        root_console.draw_str(left, top, f'BLOCK: {player.block}')

        # combat stats
        top += 3
        root_console.draw_str(left, top, f'HIT CHANCE: {player.combined_hit_chance}%')
        top += 1
        root_console.draw_str(left, top, f'CRIT CHANCE: {player.combined_crit_chance}%')
        top += 1
        root_console.draw_str(left, top, f'DAMAGE: {player.min_damage}-{player.max_damage}')

        # level-up point application
        top += 5
        root_console.draw_str(left, top, f'UNSPENT POINTS: {player.unspent_points}', fg=(255, 255, 0))
        if player.unspent_points > 0:
            top += 1
            root_console.draw_str(left + 2, top, f'[1] INCREASE MAX HEALTH (+1)')
            top += 1
            root_console.draw_str(left + 2, top, f'[2] INCREASE POWER (+1)')
            top += 1
            root_console.draw_str(left + 2, top, f'[3] INCREASE BLOCK (+1)')

        tdl.flush()

        user_input = wait_for_keys(
            [
                'ESCAPE',
                'LEFT',
                'RIGHT',
                'DOWN',
                'UP',
                'c',
                '1',
                '2',
                '3'
            ]
        )

        if user_input == 'ESCAPE' or user_input == 'c':
            return GameState.ROOM

        elif player.unspent_points > 0:
            if user_input == '1':
                # increase max health
                player.max_health += 1
                player.spend_points(1)
            elif user_input == '2':
                # increase power
                player.power += 1
                player.spend_points(1)
            elif user_input == '3':
                # increase block
                player.block += 1
                player.spend_points(1)

        else:
            continue
