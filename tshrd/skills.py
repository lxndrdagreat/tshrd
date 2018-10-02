from enum import Enum, auto
from tshrd.mapping import MapInformation, Room
from tshrd.status_effect import StatusEffectType
import random
import math


class SkillType(Enum):
    Active = auto()
    Passive = auto()


class Skill:
    def __init__(self):
        self._skill_type: SkillType = None

        self.name: str = None
        self.description: str = None

        # use cases
        self._activate_in_combat: bool = False
        self._activate_outside_encounter: bool = False

    @property
    def type(self) -> SkillType:
        return self._skill_type

    @property
    def can_activate_in_combat(self) -> bool:
        return self._activate_in_combat

    @property
    def can_activate_outside_encounter(self) -> bool:
        return self._activate_outside_encounter

    def ready(self) -> bool:
        pass


class ActiveSkill(Skill):
    def __init__(self):
        super().__init__()
        self._skill_type = SkillType.Active

    def activate(self, *args, **kwargs) -> bool:
        pass


class PassiveSkill(Skill):
    def __init__(self):
        super().__init__()
        self._skill_type = SkillType.Passive


class ExploreMixin:
    def __init__(self):
        super().__init__()
        self._activate_outside_encounter = True


class CombatMixin:
    def __init__(self):
        super().__init__()
        self._activate_in_combat = True


class OncePerCombatMixin:
    def __init__(self):
        super().__init__()
        self._used_this_combat = False

    def activate(self, *args, **kwargs) -> bool:
        pass


class TurnCooldownMixin:
    def __init__(self):
        super().__init__()
        self._cooldown_turns: int = 1
        self._cooldown_counter: int = 0
        # does using this skill consume a turn
        self._uses_turn: bool = False

    @property
    def cooldown_turns(self) -> int:
        return self._cooldown_turns

    @property
    def cooldown_left(self) -> int:
        return self._cooldown_counter

    @property
    def uses_turn(self) -> bool:
        return self._uses_turn

    def reset_cooldown(self):
        self._cooldown_counter = 0

    def tick(self):
        if self._cooldown_counter > 0:
            self._cooldown_counter -= 1

    def start(self):
        self._cooldown_counter = self._cooldown_turns

    def ready(self) -> bool:
        return self._cooldown_counter == 0


class GiftOfTheSeerSkill(TurnCooldownMixin, ExploreMixin, ActiveSkill):
    def __init__(self):
        super().__init__()
        self.name = 'Gift of the Seer'
        self.description = 'Reveal the encounter of all rooms adjacent to the one you are currently in.'
        self._cooldown_turns = 10

    def activate(self, game_data) -> bool:
        if not self.ready():
            return False

        self.start()

        the_map: MapInformation = game_data.current_map
        current_room: Room = game_data.current_room
        room_x = current_room.x
        room_y = current_room.y

        for x in range(max(0, room_x - 1), min(the_map.size[0], room_x + 2)):
            for y in range(max(0, room_y - 1), min(the_map.size[1], room_y + 2)):
                neighbor_room = the_map.room_at_position(x, y)
                if neighbor_room:
                    neighbor_room.discovered = True

        game_data.log('You peer into the future and learn about the dungeon around you.')

        return True


class WhamCombatSkill(TurnCooldownMixin, CombatMixin, ActiveSkill):
    def __init__(self):
        super().__init__()
        self.name = 'Wham'
        self.description = 'Headbutt the enemy, dealing a little damage and possibly stunning the enemy for one turn.'
        self._cooldown_turns = 3
        self._uses_turn = True

    def activate(self, game_data) -> bool:
        if not self.ready():
            return False
        self.start()

        current_room: Room = game_data.current_room
        monster = current_room.monster

        game_data.log(f'You headbutt the {monster.name} for 1 damage...')
        monster.health -= 1
        if monster.health > 0:
            # chance to stun
            # TODO: change this percentage
            if random.randint(1, 101) <= 100:
                monster.apply_status_effect(StatusEffectType.Stunned, 2)
                game_data.log('...and stun it!')
        else:
            # monster died to a head butt...
            game_data.log('...and kill it!')

        return True


class CureWoundsSkill(TurnCooldownMixin, CombatMixin, ExploreMixin, ActiveSkill):
    def __init__(self):
        super().__init__()
        self.name = 'Cure Wounds'
        self.description = 'Heals for 30% of the caster\'s health.'
        self._cooldown_turns = 4
        self._uses_turn = True

    def activate(self, game_data: 'GameData') -> bool:
        if not self.ready():
            return False
        self.start()

        character: 'Character' = game_data.the_player

        heal = character.heal(int(math.ceil(character.max_health * 0.3)))

        # TODO: handle monsters healing themselves...
        game_data.log(f'You heal for {heal} hit points.')

        return True


class InitiativePassiveSkill(OncePerCombatMixin, CombatMixin, PassiveSkill):
    def __init__(self):
        super().__init__()
        self.name = 'Initiative'
        self.description = 'Your first attack on a monster does bonus damage.'
