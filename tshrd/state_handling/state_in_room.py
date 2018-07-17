import tdl
import math
from tshrd.utils import wait_for_keys, draw_player_status_bar
from tshrd.state_handling import GameData, GameState


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
        center_x = math.floor(room_draw_width / 2)
        center_y = math.floor(room_draw_height / 2)

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
            if game.current_room.encounter == 'monster':
                root_console.draw_char(left + center_x, top + center_y, game.current_room.monster.tile, bg=None, fg=(255, 255, 255))

    # draw the log
    game.draw_log(root_console)

    tdl.flush()

    user_input = wait_for_keys([
        'ESCAPE',
        'UP',
        'DOWN',
        'LEFT',
        'RIGHT',
        'm'
    ])

    if user_input == 'UP':
        return GameState.MOVE_NORTH

    elif user_input == 'DOWN':
        return GameState.MOVE_SOUTH

    elif user_input == 'LEFT':
        return GameState.MOVE_WEST

    elif user_input == 'RIGHT':
        return GameState.MOVE_EAST

    if user_input == 'ESCAPE':
        return GameState.CLOSE

    if user_input == 'm':
        return GameState.MAP

    return GameState.ROOM
