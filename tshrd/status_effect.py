from enum import Enum, auto


class StatusEffectType(Enum):
    Stunned = auto()
    Shielded = auto()


class AppliedStatusEffect:
    def __init__(self, status: StatusEffectType, duration: int):
        self.status_effect = status
        self.duration = duration

    def is_done(self) -> bool:
        return self.duration <= 0

    def tick(self) -> bool:
        self.duration -= 1
        return self.duration <= 0
