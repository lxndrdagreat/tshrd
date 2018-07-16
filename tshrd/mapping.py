import random
from utils import weighted_choice


class Room(object):
    def __init__(self, x, y, depth=0):
        self.x = x
        self.y = y
        self.depth = depth

        self.north = None
        self.south = None
        self.east = None
        self.west = None

        self.connected_north = False
        self.connected_south = False
        self.connected_east = False
        self.connected_west = False

        self.tried_north = False
        self.tried_south = False
        self.tried_east = False
        self.tried_west = False

        self.encounter = None
        self.encountered = False

        # monster stored here if encounter is a monster
        self.monster = None

        self.items = []

        # Has the player seen this room
        self.discovered = False

    def connect_by_deltas(self, dx, dy, other_room):
        if dy == -1:
            self.north = other_room
            self.tried_north = True

            other_room.south = self
            other_room.tried_south = True
        elif dy == 1:
            self.south = other_room
            self.tried_south = True

            other_room.north = self
            other_room.tried_north = True
        elif dx == -1:
            self.west = other_room
            self.tried_west = True

            other_room.east = self
            other_room.tried_east = True
        elif dx == 1:
            self.east = other_room
            self.tried_east = True

            other_room.west = self
            other_room.tried_west = True


class MapInformation(object):
    def __init__(self):
        self.rooms = []
        self.bounds = (0, 0, 0, 0)
        self.size = (0, 0)
        self.depth = 1

        self.encounters = [
            ('empty', 0.65),
            ('shrine', 0.8),
            ('monster', 1.3),
            ('treasure', 1.1),
            ('trap', 0.9)
        ]

    def calculate_bounds(self, reposition=False):
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0

        for room in self.rooms:
            min_x = min(min_x, room.x)
            min_y = min(min_y, room.y)
            max_x = max(max_x, room.x)
            max_y = max(max_y, room.y)

        if reposition:
            for room in self.rooms:
                room.x += abs(min_x)
                room.y += abs(min_y)

            max_x += abs(min_x)
            max_y += abs(min_y)
            min_x = 0
            min_y = 0

        self.bounds = (
            min_x,
            min_y,
            max_x,
            max_y
        )

        self.size = (
            max_x - min_x,
            max_y - min_y
        )

    def print_with_size(self, room_size=4, spacing=2, current_room=None):
        self.calculate_bounds()
        width = (room_size + (spacing * 2)) * self.size[0]
        height = (room_size + (spacing * 2)) * self.size[1]
        # print("{} x {}".format(width, height))

        grid = []

        for y in range(0, height):
            grid.append([])
            for x in range(0, width):
                grid[y].append('#')

        # rooms
        for room in self.rooms:
            x = room.x * (room_size + spacing) + spacing
            y = room.y * (room_size + spacing) + spacing
            # print("{}, {}".format(x, y))
            for xx in range(x, x + room_size):
                for yy in range(y, y + room_size):
                    grid[yy][xx] = '.'

        # connections
        for room in self.rooms:
            if room.north and not room.connected_north:
                room.connected_north = True
                room.north.connected_south = True
                connect_rooms((room.x * (room_size + spacing) + spacing, room.y * (room_size + spacing) + spacing),
                              (room.north.x * (room_size + spacing) + spacing,
                               room.north.y * (room_size + spacing) + spacing), grid, room_size)
            if room.south and not room.connected_south:
                room.connected_south = True
                room.south.connected_north = True
                connect_rooms((room.x * (room_size + spacing) + spacing, room.y * (room_size + spacing) + spacing),
                              (room.south.x * (room_size + spacing) + spacing,
                               room.south.y * (room_size + spacing) + spacing), grid, room_size)
            if room.east and not room.connected_east:
                room.connected_east = room.east.connected_west = True
                connect_rooms((room.x * (room_size + spacing) + spacing, room.y * (room_size + spacing) + spacing),
                              (room.east.x * (room_size + spacing) + spacing,
                               room.east.y * (room_size + spacing) + spacing), grid, room_size)
            if room.west and not room.connected_west:
                room.connected_west = room.west.connected_east = True
                connect_rooms((room.x * (room_size + spacing) + spacing, room.y * (room_size + spacing) + spacing),
                              (room.west.x * (room_size + spacing) + spacing,
                               room.west.y * (room_size + spacing) + spacing), grid, room_size)

        if current_room is not None:
            room = self.rooms[current_room]
            x = room.x * (room_size + spacing) + spacing + int(room_size / 2)
            y = room.y * (room_size + spacing) + spacing + int(room_size / 2)
            grid[y][x] = '@'

        for y in range(0, height):
            line = ''
            for x in range(0, width):
                line += grid[y][x]

            print(line)

    def generate_encounters(self):

        have_exit = False
        for room in self.rooms:
            if room.encounter is not None:
                continue

            if room.depth >= self.depth and not have_exit:
                have_exit = True
                room.encounter = 'stairs'
                continue

            room.encounter = weighted_choice(self.encounters)


def connect_rooms(start, end, grid, room_size):

    x = start[0]
    y = start[1]

    ex = end[0]
    ey = end[1]

    if ex - x < ey - y:
        ex += int(room_size / 2)
        x += int(room_size / 2)
    else:
        ey += int(room_size / 2)
        y += int(room_size / 2)

    while x != ex or y != ey:
        if grid[y][x] == '#':
            grid[y][x] = '_'
        if x < ex:
            x += 1
        elif x > ex:
            x -= 1

        if y < ey:
            y += 1
        elif y > ey:
            y -= 1


def depth_first_build(max_depth=4):

    # create starting room

    # add it to the stack

    # while the stack has rooms,
    # take the last room
    # grab a random direction that has not been explored
    # make the connecting room and add it to the stack
    # if all directions have been explored, remove from the stack

    the_map = MapInformation()
    the_map.depth = max_depth

    stack = []

    room = Room(0, 0)
    room.encounter = 'start'

    stack.append(room)
    the_map.rooms.append(room)

    while len(stack) > 0:
        room = stack[len(stack)-1]

        explorable = []

        # if all directions have been explored, remove from stack
        if not room.tried_north:
            explorable.append(0)
        if not room.tried_south:
            explorable.append(1)
        if not room.tried_east:
            explorable.append(2)
        if not room.tried_west:
            explorable.append(3)

        if len(explorable) == 0 or room.depth > max_depth:
            stack.pop()
            continue

        if len(explorable) == 1:
            which = explorable[0]
        else:
            which = random.choice(explorable)

        dx = 0
        dy = 0        

        if which == 0:
            # north
            room.tried_north = True
            dy = -1
        elif which == 1:
            # south
            room.tried_south = True
            dy = 1
        elif which == 2:
            # east
            room.tried_east = True
            dx = 1
        elif which == 3:
            # west
            room.tried_west = True
            dx = -1

        x = room.x + dx
        y = room.y + dy

        spot_taken = [r for r in the_map.rooms if r.x == x and r.y == y]
        if len(spot_taken) > 0:
            # something already exists here
            continue

        # random chance to NOT create room
        no_hall = weighted_choice([
            (True, 0.6),
            (False, 1.0)
        ])

        if not no_hall:
            next_room = Room(x, y, room.depth + 1)
            room.connect_by_deltas(dx, dy, next_room)
            the_map.rooms.append(next_room)
            stack.append(next_room)

    return the_map


def build_test_html():
    the_map = depth_first_build(50)

    the_map.calculate_bounds(True)

    the_map.generate_encounters()

    room_size = 1

    spacing_pixels = 10

    room_size_pixels = room_size * 25

    # the_map.print_with_size()

    with open('template.html', 'r') as template_file:
        html = template_file.read()

    lines = []

    for room in the_map.rooms:
        room_x = room.x * (room_size_pixels + spacing_pixels)
        room_y = room.y * (room_size_pixels + spacing_pixels)
        extra_classes = ''
        if room.encounter and room.encounter == 'start':
            extra_classes = 'start'
        elif room.encounter and room.encounter == 'monster':
            extra_classes = 'encounter monster'
        elif room.encounter and room.encounter == 'stairs':
            extra_classes = 'end'
        elif room.encounter and room.encounter == 'trap':
            extra_classes = 'encounter trap'
        elif room.encounter and room.encounter == 'shrine':
            extra_classes = 'encounter shrine'
        elif room.encounter and room.encounter == 'treasure':
            extra_classes = 'encounter treasure'
        line = '<div class="room {}" style="left: {}px; top: {}px; width: {}px; height: {}px;"></div>'.format(
            extra_classes,
            room_x,
            room_y,
            room_size_pixels,
            room_size_pixels)
        lines.append(line)

        if room.north:
            hall = '<div class="hall ns" style="left: {}px; top: {}px; width: {}px; height: {}px;"></div>'.format(
                room_x + (int(room_size_pixels * 0.45)),
                room_y - spacing_pixels,
                int(room_size_pixels * 0.1),
                spacing_pixels
            )
            lines.append(hall)

        if room.south:
            hall = '<div class="hall ns" style="left: {}px; top: {}px; width: {}px; height: {}px;"></div>'.format(
                room_x + (int(room_size_pixels * 0.45)),
                room_y + room_size_pixels,
                int(room_size_pixels * 0.1),
                spacing_pixels
            )
            lines.append(hall)

        if room.east:
            hall = '<div class="hall ew" style="left: {}px; top: {}px; width: {}px; height: {}px;"></div>'.format(
                room_x + room_size_pixels,
                room_y + (int(room_size_pixels * 0.45)),
                spacing_pixels,
                int(room_size_pixels * 0.1)
            )
            lines.append(hall)

        if room.west:
            hall = '<div class="hall ew" style="left: {}px; top: {}px; width: {}px; height: {}px;"></div>'.format(
                room_x - spacing_pixels,
                room_y + (int(room_size_pixels * 0.45)),
                spacing_pixels,
                int(room_size_pixels * 0.1)
            )
            lines.append(hall)

    all_parts = ''.join(lines)

    html = html.replace('{ DATA }', all_parts)

    with open('output.html', 'w') as output_file:
        output_file.write(html)

if __name__ == '__main__':

    build_test_html()
