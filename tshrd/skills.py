from enum import Enum, auto
from typing import Callable


class SkillType(Enum):
    Active = auto()
    Passive = auto()


class Skill:
    def __init__(self, skill_type: SkillType=SkillType.Active, activate_in_combat: bool=False,
                 activate_outside_encounter: bool=False, cooldown: int=1, on_activate: Callable=None):
        self._skill_type: SkillType = skill_type

        self.name: str = None
        self.description: str = None
        self._cooldown: int = cooldown
        self._cooldown_counter: int = 0

        # use cases
        self._activate_in_combat: bool = activate_in_combat
        self._activate_outside_encounter: bool = activate_outside_encounter

        self._activate: Callable = on_activate

    @property
    def type(self) -> SkillType:
        return self._skill_type

    @property
    def can_activate_in_combat(self) -> bool:
        return self._activate_in_combat

    @property
    def can_activate_outside_encounter(self) -> bool:
        return self._activate_outside_encounter

    @property
    def cooldown_done(self) -> bool:
        return self._cooldown_counter == 0

    @property
    def cooldown_rate(self) -> int:
        return self._cooldown

    @property
    def cooldown_left(self) -> int:
        return self._cooldown_counter

    def reset_cooldown(self):
        self._cooldown_counter = 0

    def tick_cooldown(self):
        if self._cooldown_counter > 0:
            self._cooldown_counter -= 1

    def activate(self, game_state):
        if self._activate:
            self._activate(self, game_state)


def _gift_of_the_seer_activate(skill: Skill, game_state):
    pass


SKILL_GIFT_OF_THE_SEER = Skill(SkillType.Active, False, True, 10, _gift_of_the_seer_activate)
SKILL_GIFT_OF_THE_SEER.name = 'Gift of the Seer'
