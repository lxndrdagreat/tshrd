import random
from tshrd.utils import weighted_choice


PREFIXES = ('', 'Bloody', 'Dirty', 'Shiny', 'Evil', 'Blessed', 'Broken', 'Tarnished', 'Mastercraft', 'Rusty', 'Conqueror\'s')
SUFFIXES = ('', 'Of Pain', 'Of Doom', 'Of Chaos', 'Of Light')
WEAPONS = ('Sword', 'Dagger', 'Staff', 'Hammer', 'Mace', 'Flail')
ARMORS = ('Chain Mail', 'Plate Mail', 'Scale Mail', 'Leather Jerkin', 'Cuirass')


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


class Weapon(Item):
    def __init__(self, name: str, description: str=None):
        Item.__init__(self, name, description)

        self._equipable = True

        # percentage
        self._multiplier_min = 1.1
        self._multiplier_max = 1.15

    def get_multiplier_range(self):
        return self._multiplier_min, self._multiplier_max

    def multiplier(self):
        return random.uniform(self._multiplier_min, self._multiplier_max)


def generate_random_weapon(level: int) -> Weapon:
    name = '{} {} {}'.format(random.choice(PREFIXES), random.choice(WEAPONS), random.choice(SUFFIXES)).strip()

    weapon = Weapon(name)

    return weapon


class Armor(Item):
    def __init__(self, name: str, description: str=None):
        Item.__init__(self, name, description)

        self._equipable = True

        # percentage
        self._multiplier_min = 1.1
        self._multiplier_max = 1.15

    def get_multiplier_range(self):
        return self._multiplier_min, self._multiplier_max

    def multiplier(self):
        return random.uniform(self._multiplier_min, self._multiplier_max)


def generate_random_armor(level: int) -> Armor:
    name = '{} {} {}'.format(random.choice(PREFIXES), random.choice(ARMORS), random.choice(SUFFIXES)).strip()

    armor = Armor(name)

    return armor


class Potion(Item):
    def __init__(self, name: str, level: str, description: str=None):
        Item.__init__(self, name, description)

        self._activate_in_combat = True
        self._activate_outside_encounter = True

        self.uses = 1

        self.level = level

    def reset(self):
        self.uses = 1


class HealthPotion(Potion):
    def __init__(self, level: str):
        Potion.__init__(self, 'Health Potion', level)
        self._activate_on_player = True

    def activate(self, target) -> str:
        amount = 3
        if self.level == 'medium':
            amount = 5
        elif self.level == 'major':
            amount = 10
        elif self.level == 'mega':
            amount = 15
        amount_healed = target.heal(amount)
        return f'You drank a {self.level} Health Potion and were healed for {amount_healed} damage.'


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
                pot = HealthPotion('minor')
            elif level < 10:
                pot = HealthPotion('medium')
            elif level < 15:
                pot = HealthPotion('major')
            else:
                pot = HealthPotion('mega')
            loot.append(pot)
        elif kind == 'weapon':
            weapon = generate_random_weapon(level)
            loot.append(weapon)
        elif kind == 'armor':
            armor = generate_random_armor(level)
            loot.append(armor)
        elif kind == 'food':
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
