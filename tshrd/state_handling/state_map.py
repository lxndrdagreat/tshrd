import tdl
from tshrd.state_handling import GameData, GameState
from tshrd.utils import wait_for_keys


def state(game: GameData, root_console: tdl.Console) -> GameState:

    root_console.clear()
    tdl.flush()

    room_size = 5
    spacing = 0

    the_map = game.current_map

    total_width = (room_size + (spacing * 2)) * the_map.size[0]
    total_height = (room_size + (spacing * 2)) * the_map.size[1]

    map_console = tdl.Console(total_width, total_height)
    # map_console.set_colors(fg=(255, 255, 255), bg=(0, 0, 100))
    map_console.clear()

    legend_scheme = {
        'monster': (180, 0, 0),
        'shrine': (255, 255, 200),
        'treasure': (200, 200, 0),
        'trap': (149, 108, 53),
        'stairs': (0, 200, 235),
        'empty': (255, 255, 255)
    }

    # draw the rooms
    map_center_x = 0
    map_center_y = 0
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
            map_center_x = x + int(room_size / 2)
            map_center_y = y + int(room_size / 2)
            map_console.draw_char(x + int(room_size / 2), y + int(room_size / 2), game.the_player.tile, fg=(255, 255, 255))

    src_x = max(map_center_x - 15, 0)
    src_y = max(map_center_y - 15, 0)
    root_console.draw_rect(0, 0, 30, 30, None, bg=(50, 50, 50))
    root_console.blit(map_console, 0, 0, 30, 30, src_x, src_y, 1.0, 0.0)

    # legend
    x = root_console.width - 20
    y = 1
    root_console.draw_str(x, y, 'LEGEND', bg=None, fg=(255, 255, 255))
    y += 1
    root_console.draw_str(x, y, '# Shrine', bg=None, fg=legend_scheme['shrine'])
    y += 1
    root_console.draw_str(x, y, '# Treasure', bg=None, fg=legend_scheme['treasure'])
    y += 1
    root_console.draw_str(x, y, '# Monster', bg=None, fg=legend_scheme['monster'])
    y += 1
    root_console.draw_str(x, y, '# Trap', bg=None, fg=legend_scheme['trap'])
    y += 1
    root_console.draw_str(x, y, '# Stairs', bg=None, fg=legend_scheme['stairs'])
    y += 1
    root_console.draw_str(x, y, '# Empty', bg=None, fg=legend_scheme['empty'])

    # bottom bar
    root_console.draw_rect(0, root_console.height - 3, root_console.width, 3, None, bg=(200, 200, 200))
    root_console.draw_str(1, root_console.height - 2, '[ESC] back', fg=(0, 0, 0), bg=None)
    # root_console.draw_str(20, root_console.height - 2, '[Arrow Keys] scroll map', fg=(0, 0, 0), bg=None)

    tdl.flush()

    wait_for_keys(['ESCAPE', 'SPACE', 'ENTER', 'm'])

    return GameState.ROOM
