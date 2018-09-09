import random
from tshrd.utils import weighted_choice
from enum import IntEnum, Enum, auto
import math


WEAPON_TYPES = ('Sword', 'Dagger', 'Staff', 'Hammer', 'Mace', 'Flail')
ARMOR_TYPES = ('Chain Mail', 'Plate Mail', 'Scale Mail', 'Leather Jerkin', 'Cuirass')


class Item(object):
    def __init__(self, name: str, description: str=None):
        self.name = name
        self.description = description
        self.value = 0

        # use cases
        self._activate_in_combat = False
        self._activate_outside_encounter = False
        self._activate_on_player = False
        self._activate_on_monster = False

        # is the item able to be equipped (most items are not)
        self._equipable = False

    def is_equipable(self):
        return self._equipable

    def can_activate_in_combat(self):
        return self._activate_in_combat

    def can_activate_outside_encounter(self):
        return self._activate_outside_encounter

    def can_activate_on_player(self):
        return self._activate_on_player

    def can_activate_on_monster(self):
        return self._activate_on_monster

    def activate(self, target) -> str:
        pass

    def __repr__(self):
        return self.name


class Gold(Item):
    def __init__(self, amount: int):
        Item.__init__(self, 'Gold')

        self.amount = amount
        self.value = amount

    def __repr__(self):
        return '{} gold pieces'.format(self.amount)


class WeaponPrefix(Enum):
    Cursed = auto()
    Blessed = auto()
    Broken = auto()
    Mastercraft = auto()
    Heavy = auto()


class WeaponSuffix(Enum):
    Pain = auto()
    Doom = auto()
    Adventuring = auto()
    Vampirism = auto()


class Weapon(Item):
    def __init__(self, name: str, description: str=None):
        Item.__init__(self, name, description)

        self._equipable = True

        self.hit_chance_modifier: int = 0
        self.crit_chance_modifier: int = 1
        self.damage: int = 2

        # life stealing properties of the weapon
        self.life_steal_chance = 0
        self.life_steal_percent = .5

        self.prefix: WeaponPrefix = None
        self.suffix: str = None


def generate_random_weapon(level: int, prefix_chance: int=50, suffix_chance: int=50) -> Weapon:
    weapon_type = random.choice(WEAPON_TYPES)
    weapon_name = weapon_type
    # TODO: determine random prefix with a weighted system
    prefix: WeaponPrefix = random.choice([pre for pre in WeaponPrefix])
    has_prefix = random.randint(1, 101) <= prefix_chance
    if has_prefix:
        weapon_name = f'{prefix.name} {weapon_name}'
    has_suffix = random.randint(1, 101) <= suffix_chance
    # TODO: determine random suffix with a weighted system
    suffix: WeaponSuffix = random.choice([suf for suf in WeaponSuffix])
    if has_suffix:
        weapon_name = f'{weapon_name} of {suffix.name}'

    weapon = Weapon(weapon_name)

    base_damage = 2 * level
    damage = base_damage
    if has_prefix:
        weapon.prefix = prefix
        if prefix == WeaponPrefix.Blessed:
            # add bonus damage
            damage += level
        elif prefix == WeaponPrefix.Cursed:
            # reduce damage
            damage = max(math.ceil(base_damage / 2.0), damage - level)
        elif prefix == WeaponPrefix.Mastercraft:
            # increased crit range
            weapon.crit_chance_modifier = 5
        elif prefix == WeaponPrefix.Heavy:
            # decreased hit chance
            weapon.hit_chance_modifier = -20
        elif prefix == WeaponPrefix.Broken:
            # weapon is basically useless
            damage = level
    if has_suffix:
        weapon.suffix = suffix
        if suffix == WeaponSuffix.Pain and (has_prefix is False or prefix != WeaponPrefix.Broken):
            damage += base_damage
        if suffix == WeaponSuffix.Vampirism:
            # twenty percent chance of stealing 50% (default) of damage dealt as health
            weapon.life_steal_chance = 20

    weapon.damage = damage

    return weapon


class ArmorPrefix(Enum):
    Swift = auto()
    Dodging = auto()
    Mastercraft = auto()


class ArmorSuffix(Enum):
    Adventuring = auto()
    Fleeing = auto()


class Armor(Item):
    def __init__(self, name: str, block: int=0, description: str=None):
        Item.__init__(self, name, description)

        self._equipable = True
        self.block = block
        self.dodge_chance = 0
        self.prefix: ArmorPrefix = None
        self.suffix: ArmorSuffix = None


def generate_random_armor(level: int, prefix_chance: int=35, suffix_chance: int=20) -> Armor:
    base_name = random.choice(ARMOR_TYPES)

    has_prefix = random.randint(1, 101) <= prefix_chance
    has_suffix = random.randint(1, 101) <= suffix_chance

    # TODO determine prefix and suffix with a weighted system
    prefix = None if not has_prefix else random.choice([pre for pre in ArmorPrefix])
    suffix = None if not has_suffix else random.choice([suf for suf in ArmorSuffix])

    name = base_name

    block = level
    dodge_chance = 0
    if has_prefix:
        name = f'{prefix.name} {name}'
        if prefix == ArmorPrefix.Mastercraft:
            # boost block
            block += 2
        elif prefix == ArmorPrefix.Dodging:
            # give the armor a small amount of chance to dodge an attack entirely
            dodge_chance = 10

    if has_suffix:
        name = f'{name} of {suffix.name}'

    armor = Armor(name, block)
    armor.dodge_chance = dodge_chance
    armor.suffix = suffix
    armor.prefix = prefix

    return armor


class PotionStrength(IntEnum):
    Minor = auto()
    Medium = auto()
    Major = auto()
    Mega = auto()


class Potion(Item):
    def __init__(self, name: str, level: PotionStrength, description: str=None):
        Item.__init__(self, name, description)

        self._activate_in_combat = True
        self._activate_outside_encounter = True

        self.uses = 1

        self.level = level

    def reset(self):
        self.uses = 1

    def __repr__(self):
        return f'{self.level.name} {self.name}'


class HealthPotion(Potion):
    def __init__(self, level: PotionStrength):
        Potion.__init__(self, 'Health Potion', level)
        self._activate_on_player = True

        self._amount_per_level = {
            PotionStrength.Minor: 3,
            PotionStrength.Medium: 5,
            PotionStrength.Major: 10,
            PotionStrength.Mega: 15
        }

        self.description = f'Heals you for {self._amount_per_level[self.level]} hit points.'

    def activate(self, target) -> str:
        amount = self._amount_per_level.get(self.level, 3)
        amount_healed = target.heal(amount)
        return f'You drank a {self.level.name} Health Potion and were healed for {amount_healed} damage.'


class Inventory(object):
    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items

    def add_item(self, item: Item):
        if item not in self._items:
            self._items.append(item)

    def add_items(self, items):
        for item in items:
            if item not in self._items:
                self._items.append(item)

    def remove_item(self, item: Item):
        if item in self._items:
            self._items.remove(item)


LOOT_TABLE_BY_LEVEL = (
    (
        # Level 1
        ('health_potion', 1.0),
        ('weapon', 1.0),
        ('armor', 1.0),
        ('food', 1.0),
        ('gold', 1.0)
    ),
    (
        # Level 2
        ('health_potion', 1.0),
        ('weapon', 1.0),
        ('armor', 1.0),
        ('food', 1.0),
        ('gold', 1.0)
    )
)


def generate_random_loot(level: int, num_items: int=1) -> list:
    loot = []

    gold_amount = 0

    for i in range(0, num_items):
        kind = weighted_choice(
            LOOT_TABLE_BY_LEVEL[level-1] if len(LOOT_TABLE_BY_LEVEL) >= level - 1
            else LOOT_TABLE_BY_LEVEL[len(LOOT_TABLE_BY_LEVEL)-1])

        if kind == 'health_potion':
            if level < 5:
                pot = HealthPotion(PotionStrength.Minor)
            elif level < 10:
                pot = HealthPotion(PotionStrength.Medium)
            elif level < 15:
                pot = HealthPotion(PotionStrength.Major)
            else:
                pot = HealthPotion(PotionStrength.Mega)
            loot.append(pot)
        elif kind == 'weapon':
            weapon = generate_random_weapon(level)
            loot.append(weapon)
        elif kind == 'armor':
            armor = generate_random_armor(level)
            loot.append(armor)
        elif kind == 'food':
            amount = random.randint(max(1, level - 2), level + 3)
            for a in range(1, amount + 1):
                loot.append('Food')
        elif kind == 'gold':
            amount = random.randint(level, level + 5)
            gold_amount += amount

    if gold_amount > 0:
        gold = Gold(gold_amount)
        loot.append(gold)

    return loot


def test():

    level = 1

    loot = generate_random_loot(level, 10)

    for prize in loot:
        print(prize)


if __name__ == '__main__':
    test()
