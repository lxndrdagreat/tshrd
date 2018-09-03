import tdl
import math
import time
from tshrd.state_handling import GameData, GameState
from tshrd.mapping import EncounterType


def state(game: GameData, root_console: tdl.Console) -> GameState:
    if not game.current_room:
        return GameState.ROOM

    moved = False

    if game.state == GameState.MOVE_NORTH and game.current_room.north:
        travel_direction('north', root_console)
        game.previous_room = game.current_room
        game.current_room = game.current_room.north
        moved = True

    elif game.state == GameState.MOVE_SOUTH and game.current_room.south:
        travel_direction('south', root_console)
        game.previous_room = game.current_room
        game.current_room = game.current_room.south
        moved = True

    elif game.state == GameState.MOVE_EAST and game.current_room.east:
        travel_direction('east', root_console)
        game.previous_room = game.current_room
        game.current_room = game.current_room.east
        moved = True

    elif game.state == GameState.MOVE_WEST and game.current_room.west:
        travel_direction('west', root_console)
        game.previous_room = game.current_room
        game.current_room = game.current_room.west
        moved = True

    if moved:
        game.current_room.discovered = True
        game.advance_turn()
        if game.current_room.encountered:
            return GameState.ROOM
        if game.current_room.encounter == EncounterType.TREASURE:
            return GameState.ENCOUNTER_TREASURE
        elif game.current_room.encounter == EncounterType.SHRINE:
            return GameState.ENCOUNTER_SHRINE
        elif game.current_room.encounter == EncounterType.MONSTER:
            return GameState.ENCOUNTER_MONSTER
        elif game.current_room.encounter == EncounterType.TRAP:
            return GameState.ENCOUNTER_TRAP
        elif game.current_room.encounter == EncounterType.STAIRS:
            return GameState.ROOM
    return GameState.ROOM


def travel_direction(direction, root_console: tdl.Console):
    """
    self-contained "animation" of moving through a hallway in a certain direction
    """
    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0

    room_draw_width = 9
    room_draw_height = 9

    top = 5
    left = 5

    for x in range(0, room_draw_width):
        for y in range(0, room_draw_height):
            tile = ' '
            if direction == 'north' or direction == 'south':
                if x == math.floor(room_draw_width / 2):
                    tile = '.'
                if x == math.floor(room_draw_width / 2) - 1 or x == math.floor(room_draw_width / 2) + 1:
                    tile = '#'
            elif direction == 'east' or direction == 'west':
                if y == math.floor(room_draw_height / 2):
                    tile = '.'
                if y == math.floor(room_draw_height / 2) - 1 or y == math.floor(room_draw_height / 2) + 1:
                    tile = '#'

            root_console.draw_char(left + x, top + y, tile, bg=None, fg=(255, 255, 255))

    if direction == 'north' or direction == 'south':
        start_x = math.floor(room_draw_width / 2)
        end_x = start_x
    elif direction == 'east' or direction == 'west':
        start_y = math.floor(room_draw_height / 2)
        end_y = start_y

    if direction == 'north':
        start_y = room_draw_height - 1
    elif direction == 'south':
        end_y = room_draw_height - 1
    elif direction == 'east':
        end_x = room_draw_width - 1
    elif direction == 'west':
        start_x = room_draw_width - 1

    x = start_x
    y = start_y
    while x != end_x or y != end_y:
        root_console.draw_char(left + x, top + y, '.', bg=None, fg=(255, 255, 255))

        if direction == 'north':
            y -= 1
        elif direction == 'south':
            y += 1
        elif direction == 'east':
            x += 1
        elif direction == 'west':
            x -= 1

        root_console.draw_char(left + x, top + y, '@', bg=None, fg=(255, 255, 255))
        tdl.flush()
        time.sleep(.1)
