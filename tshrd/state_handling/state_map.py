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

    # rooms
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

                if room.encounter and room.encounter == 'monster':
                    color = (180, 0, 0)
                elif room.encounter and room.encounter == 'shrine':
                    color = (255, 255, 200)
                elif room.encounter and room.encounter == 'treasure':
                    color = (200, 200, 0)
                elif room.encounter and room.encounter == 'trap':
                    color = (149, 108, 53)
                elif room.encounter and room.encounter == 'stairs':
                    color = (0, 200, 235)

                map_console.draw_char(xx, yy, t, bg=None, fg=color)

    root_console.blit(map_console)

    # legend
    x = root_console.width - 20
    y = 1
    root_console.draw_str(x, y, 'LEGEND', bg=None, fg=(255, 255, 255))
    y += 1
    root_console.draw_str(x, y, '# Shrine', bg=None, fg=(255, 255, 200))
    y += 1
    root_console.draw_str(x, y, '# Treasure', bg=None, fg=(200, 200, 0))
    y += 1
    root_console.draw_str(x, y, '# Monster', bg=None, fg=(180, 0, 0))
    y += 1
    root_console.draw_str(x, y, '# Trap', bg=None, fg=(149, 108, 53))
    y += 1
    root_console.draw_str(x, y, '# Stairs', bg=None, fg=(0, 200, 235))

    tdl.flush()

    wait_for_keys(['ESCAPE', 'SPACE', 'ENTER', 'm'])

    return GameState.ROOM
