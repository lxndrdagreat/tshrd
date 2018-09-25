import random
from tshrd.utils import weighted_choice
from enum import IntEnum, auto
from typing import Union


class EncounterType(IntEnum):
    START = auto()
    EMPTY = auto()
    SHRINE = auto()
    MONSTER = auto()
    TREASURE = auto()
    TRAP = auto()
    STAIRS = auto()


class Room:
    def __init__(self, x: int, y: int, depth: int=0):
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

        self.encounter: EncounterType = None
        self.encountered = False

        # monster stored here if encounter is a monster
        self.monster = None

        self.items = []

        # Has the player seen this room
        self.discovered = False

    def neighbor_list(self) -> list:
        neighbors = []
        if self.north:
            neighbors.append(self.north)
        if self.south:
            neighbors.append(self.south)
        if self.east:
            neighbors.append(self.east)
        if self.west:
            neighbors.append(self.west)
        return neighbors

    def connect_by_deltas(self, dx: int, dy: int, other_room):
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

    def __repr__(self):
        return f'<tshrd.mapping.Room {self.encounter}>'


class MapInformation:
    def __init__(self, encounter_list: list=(
            (EncounterType.EMPTY, 0.65, True),
            (EncounterType.SHRINE, 0.6, False, 1),
            (EncounterType.MONSTER, 1.3, True),
            (EncounterType.TREASURE, 1.1, True),
            (EncounterType.TRAP, 1.1, True)
    )):
        self.rooms = []
        self.bounds = (0, 0, 0, 0)
        self.size = (0, 0)
        self.depth = 1

        self.encounters = encounter_list

    def calculate_bounds(self, reposition: bool=False):
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
            max_x - min_x + 1,
            max_y - min_y + 1
        )

    def print_with_size(self, room_size: int=4, spacing: int=2, current_room: int=None):
        self.calculate_bounds()
        width = (room_size + (spacing * 2)) * self.size[0]
        height = (room_size + (spacing * 2)) * self.size[1]

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

        encounter_count = {}

        for encounter_type in EncounterType:
            encounter_count[encounter_type] = 0

        have_exit = False
        for room in self.rooms:
            if room.encounter is not None:
                continue

            if room.depth >= self.depth and not have_exit:
                have_exit = True
                room.encounter = EncounterType.STAIRS
                continue

            neighbor_encounters = [r.encounter for r in room.neighbor_list() if r.encounter is not None]

            allowed_encounters = [encounter[0:2] for encounter
                                  in self.encounters
                                  if (encounter[0] not in neighbor_encounters or encounter[2] is True)
                                  and (len(encounter) < 4 or encounter_count[encounter[0]] < encounter[3])]

            if len(allowed_encounters) > 0:
                room.encounter = weighted_choice(allowed_encounters)
                encounter_count[room.encounter] += 1
            else:
                room.encounter = EncounterType.EMPTY
                encounter_count[room.encounter] += 1

    def room_at_position(self, x: int, y: int) -> Union[Room, None]:
        if x < 0 or y < 0 or x >= self.size[0] or y >= self.size[1]:
            return None
        return next((r for r in self.rooms if r.x == x and r.y == y), None)


def connect_rooms(start: tuple, end: tuple, grid: list, room_size: int):

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


def depth_first_build(max_depth: int=4) -> MapInformation:

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
    room.encounter = EncounterType.START

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
