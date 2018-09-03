import tdl
from tshrd.state_handling import GameData, GameState
from tshrd.utils import wait_for_keys
from tshrd.mapping import EncounterType


def state(game: GameData, root_console: tdl.Console) -> GameState:

    root_console.clear()
    tdl.flush()

    room_size = 5
    spacing = 0

    the_map = game.current_map

    total_width = (room_size + (spacing * 2)) * the_map.size[0]
    total_height = (room_size + (spacing * 2)) * the_map.size[1]

    map_console = tdl.Console(total_width, total_height)

    legend_scheme = {
        EncounterType.MONSTER: (180, 0, 0),
        EncounterType.SHRINE: (255, 255, 200),
        EncounterType.TREASURE: (200, 200, 0),
        EncounterType.TRAP: (149, 108, 53),
        EncounterType.STAIRS: (0, 200, 235),
        EncounterType.EMPTY: (255, 255, 255)
    }

    # legend
    x = root_console.width - 20
    y = 1
    root_console.draw_str(x, y, 'LEGEND', bg=None, fg=(255, 255, 255))
    y += 1
    root_console.draw_str(x, y, '# Shrine', bg=None, fg=legend_scheme[EncounterType.SHRINE])
    y += 1
    root_console.draw_str(x, y, '# Treasure', bg=None, fg=legend_scheme[EncounterType.TREASURE])
    y += 1
    root_console.draw_str(x, y, '# Monster', bg=None, fg=legend_scheme[EncounterType.MONSTER])
    y += 1
    root_console.draw_str(x, y, '# Trap', bg=None, fg=legend_scheme[EncounterType.TRAP])
    y += 1
    root_console.draw_str(x, y, '# Stairs', bg=None, fg=legend_scheme[EncounterType.STAIRS])
    y += 1
    root_console.draw_str(x, y, '# Empty', bg=None, fg=legend_scheme[EncounterType.EMPTY])
    y += 1
    root_console.draw_str(x, y, '@ Player', bg=None, fg=(255, 255, 255))

    # bottom bar
    root_console.draw_rect(0, root_console.height - 3, root_console.width, 3, None, bg=(200, 200, 200))
    root_console.draw_str(1, root_console.height - 2, '[ESC] back', fg=(0, 0, 0), bg=None)
    root_console.draw_str(15, root_console.height - 2, '[Arrow Keys] scroll map', fg=(0, 0, 0), bg=None)
    root_console.draw_str(50, root_console.height - 2, '[Enter] center map', fg=(0, 0, 0), bg=None)

    map_center_x = game.current_room.x * (room_size + spacing) + spacing
    map_center_y = game.current_room.y * (room_size + spacing) + spacing

    # draw the rooms
    while True:
        map_console.clear()
        for room in [room for room in the_map.rooms if room.discovered]:
            x = room.x * (room_size + spacing) + spacing
            y = room.y * (room_size + spacing) + spacing

            for xx in range(x, x + room_size):
                for yy in range(y, y + room_size):
                    t = '.'
                    if xx == x or xx == x + room_size - 1 or yy == y or yy == y + room_size - 1:
                        t = '#'
                    if room.north and yy == y and xx == x + 2:
                        t = '.'
                    if room.south and yy == y + room_size - 1 and xx == x + 2:
                        t = '.'
                    if room.east and yy == y + 2 and xx == x + room_size - 1:
                        t = '.'
                    if room.west and yy == y + 2 and xx == x:
                        t = '.'

                    color = (255, 255, 255)

                    if room.encounter and room.encounter in legend_scheme:
                        color = legend_scheme[room.encounter]

                    map_console.draw_char(xx, yy, t, bg=None, fg=color)

            if room == game.current_room:
                map_console.draw_char(x + int(room_size / 2), y + int(room_size / 2), game.the_player.tile, fg=(255, 255, 255))

        src_x = max(map_center_x - 15, 0)
        src_y = max(map_center_y - 15, 0)
        root_console.draw_rect(0, 0, 30, 30, ' ', bg=(50, 50, 50))
        root_console.blit(map_console, 0, 0, 30, 30, src_x, src_y, 1.0, 0.0)

        tdl.flush()
        response = wait_for_keys(['ESCAPE', 'SPACE', 'ENTER', 'm', 'UP', 'DOWN', 'LEFT', 'RIGHT'])
        if response in ['ESCAPE', 'SPACE', 'm']:
            break
        # scroll the map
        if response == 'UP':
            if map_center_y > 0:
                map_center_y -= 1
        elif response == 'DOWN':
            if map_center_y < total_height - 1:
                map_center_y += 1
        elif response == 'LEFT':
            if map_center_x > 0:
                map_center_x -= 1
        elif response == 'RIGHT':
            if map_center_x < total_width - 1:
                map_center_x += 1
        elif response == 'ENTER':
            # recenter the map
            map_center_x = game.current_room.x * (room_size + spacing) + spacing
            map_center_y = game.current_room.y * (room_size + spacing) + spacing

    return GameState.ROOM
