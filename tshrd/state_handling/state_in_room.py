import tdl
import math
from tshrd.utils import wait_for_keys, draw_player_status_bar
from tshrd.state_handling import GameData, GameState
from tshrd.mapping import EncounterType
from tshrd.skills import ActiveSkill, TurnCooldownMixin


def state(game: GameData, root_console: tdl.Console) -> GameState:

    root_console.clear()
    draw_player_status_bar(game.the_player, 1, root_console.height - 2, root_console)

    # draw the room
    if game.current_room:
        # odd number of tiles makes "centering" easier
        room_draw_width = game.room_draw_width
        room_draw_height = game.room_draw_height

        top = 5
        left = 5
        center_x = int(math.floor(room_draw_width / 2))
        center_y = int(math.floor(room_draw_height / 2))

        for x in range(0, room_draw_width):
            for y in range(0, room_draw_height):
                tile = '.'
                if x == 0 or y == 0 or x == room_draw_width - 1 or y == room_draw_height - 1:
                    tile = '#'
                if game.current_room.north and x == math.floor(room_draw_width / 2) and y == 0:
                    tile = '.'
                if game.current_room.south and x == math.floor(room_draw_width / 2) and y == room_draw_height - 1:
                    tile = '.'
                if game.current_room.west and x == 0 and y == math.floor(room_draw_height / 2):
                    tile = '.'
                if game.current_room.east and x == room_draw_width - 1 and y == math.floor(room_draw_height / 2):
                    tile = '.'
                root_console.draw_char(left + x, top + y, tile, bg=None, fg=(255, 255, 255))

        # draw the player in the room
        p_x = math.floor(room_draw_width / 2)
        p_y = math.floor(room_draw_height / 2)
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
        root_console.draw_char(left + p_x, top + p_y, '@', bg=None, fg=(255, 255, 255))

        # draw encounter
        if game.current_room.encounter and not game.current_room.encountered:
            if game.current_room.encounter == EncounterType.MONSTER:
                root_console.draw_char(left + center_x, top + center_y, game.current_room.monster.tile, bg=None, fg=(255, 255, 255))

            elif game.current_room.encounter == EncounterType.STAIRS:
                game.log('You find stairs to the next level! Press [ENTER] to advance.', (0, 200, 235))

    # draw info bar
    info_con = tdl.Console(int(root_console.width / 2), root_console.height - 21)
    info_con.set_colors(fg=(220, 220, 220), bg=(0, 0, 50))
    info_con.clear()
    left = 1
    top = 1
    info_con.draw_str(left, top, 'MOVE:')
    top += 1
    info_con.draw_str(left, top, '[UP] North')
    top += 1
    info_con.draw_str(left, top, '[DOWN] South')
    top += 1
    info_con.draw_str(left, top, '[RIGHT] East')
    top += 1
    info_con.draw_str(left, top, '[LEFT] West')
    top += 2
    if len(game.the_player.get_explore_skills()) > 0:
        info_con.draw_str(left, top, 'SKILLS:')
        top += 1
        for index, skill in enumerate(game.the_player.get_explore_skills(), 1):
            skill_text = f'{skill.name}'
            if not skill.ready():
                skill_text = f'{skill_text} ({skill.cooldown_left} turns)'

            info_con.draw_str(left, top, f'[{index}] {skill_text}')
            top += 1
        top += 1
    info_con.draw_str(left, top, 'MENU:')
    top += 1
    info_con.draw_str(left, top, '[m] Map')
    top += 1
    info_con.draw_str(left, top, '[i] Inventory')
    top += 1
    info_con.draw_str(left, top, '[c] Character')
    top += 1
    info_con.draw_str(left, top, '[ESC] Quit')
    root_console.blit(info_con, int(root_console.width / 2), 0)

    # draw the log
    game.draw_log(root_console)

    tdl.flush()

    user_input = wait_for_keys([
        'ESCAPE',
        'UP',
        'DOWN',
        'LEFT',
        'RIGHT',
        'ENTER',
        'i',
        'm',
        'c',
        '1',
        '2'
    ])

    if user_input == 'UP':
        return GameState.MOVE_NORTH

    elif user_input == 'DOWN':
        return GameState.MOVE_SOUTH

    elif user_input == 'LEFT':
        return GameState.MOVE_WEST

    elif user_input == 'RIGHT':
        return GameState.MOVE_EAST

    elif user_input == 'ESCAPE':
        return GameState.CLOSE

    elif user_input == 'm':
        return GameState.MAP

    elif user_input == 'i':
        return GameState.INVENTORY

    elif user_input == 'c':
        return GameState.CHARACTER_SHEET

    elif user_input == 'ENTER':
        return GameState.NEXT_LEVEL

    elif user_input == '1' and len(game.the_player.get_explore_skills()) > 0:
        # User skill 1
        skill: ActiveSkill = game.the_player.get_explore_skills()[0]
        if skill.ready():
            if skill.activate(game):
                if skill.uses_turn:
                    game.advance_turn()

    elif user_input == '2' and len(game.the_player.get_explore_skills()) > 1:
        # User skill 2
        skill: ActiveSkill = game.the_player.get_explore_skills()[1]
        if skill.ready():
            if skill.activate(game):
                if skill.uses_turn:
                    game.advance_turn()

    return GameState.ROOM
