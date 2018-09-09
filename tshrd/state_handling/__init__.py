from tshrd.characters import Character
from tshrd.inventory import ArmorPrefix
from tshrd.mapping import depth_first_build
from enum import Enum, auto
import random
import tdl


class GameState(Enum):
    ROOM = auto()
    MOVE_NORTH = auto()
    MOVE_SOUTH = auto()
    MOVE_EAST = auto()
    MOVE_WEST = auto()
    ENCOUNTER_SHRINE = auto()
    ENCOUNTER_TREASURE = auto()
    ENCOUNTER_MONSTER = auto()
    ENCOUNTER_TRAP = auto()
    INVENTORY = auto()
    FLED_ENCOUNTER = auto()
    CLOSE = auto()
    NEXT_LEVEL = auto()
    GAME_OVER = auto()
    GAME_RESTART = auto()
    MAP = auto()
    CHARACTER_SHEET = auto()
    CHARACTER_CREATION = auto()


class GameData:
    def __init__(self, player_name: str='Player'):

        self._running = False
        self.current_map = None
        self.current_room = None
        self.previous_room = None
        self.current_level = 0
        self.turn_count = 1
        self.the_player: Character = None

        self.room_draw_width = 9
        self.room_draw_height = 9

        self.state = GameState.ROOM
        self._running = True

        self._log = []

        self.build_map()

        self.log('Your adventure begins in the first room on the first floor of a deadly dungeon.')

    def build_map(self):
        self.current_level += 1
        self.current_map = depth_first_build(4)
        self.current_map.generate_encounters()
        self.current_map.calculate_bounds(True)

        self.current_room = self.current_map.rooms[0]
        self.current_room.discovered = True
        self.previous_room = None

        if self.current_level > 1:
            your_state = 'are healthy'
            if self.the_player.health <= self.the_player.max_health / 4:
                your_state = 'are heavily injured'
            elif self.the_player.health <= self.the_player.max_health * 0.75:
                your_state = 'are injured'
            elif self.the_player.health < self.the_player.max_health:
                your_state = 'have minor injuries'
            self.log(f'You have reached the next level of the dungeon.')
            self.log(f'You {your_state}.')
            self.log(f'You have {self.the_player.food} remaining food.')

    def advance_turn(self):
        self.turn_count += 1
        if self.the_player.armor and self.the_player.armor.prefix == ArmorPrefix.Swift and random.randint(1, 101) <= 40:
            text = 'You conserve your rations.'
            if self.the_player.food <= 0:
                text = 'You fight off the hunger.'
            self.log(text)
            return text
        if self.the_player.food > 0:
            self.the_player.food -= 1
            text = 'You eat 1 food.'
            if self.the_player.food < 10:
                text += ' You are running low on food.'
            self.log(text)
            return text
        else:
            self.the_player.health -= 1
            text = 'You are out of food and are starving. You lose 1 health.'
            self.log(text)
            return text

    def log(self, text: str='\n', fg=(255, 255, 255)):
        self._log.append((text, fg))

    def draw_log(self, root_console: tdl.Console):
        log_width = root_console.width
        log_height = 20
        log_y = root_console.height - 3 - log_height
        log = tdl.Console(log_width, log_height)
        log.set_colors((255, 255, 255), (50, 50, 50))
        log.clear()
        log.set_mode('scroll')
        for entry in self._log:
            log.set_colors(fg=entry[1])
            log.print_str(entry[0])
            log.print_str('\n')
        root_console.blit(log, 0, log_y)
