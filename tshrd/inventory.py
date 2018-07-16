import random
from tshrd.utils import weighted_choice


PREFIXES = ('', 'Bloody', 'Dirty', 'Shiny', 'Evil', 'Blessed', 'Broken', 'Tarnished', 'Mastercraft', 'Rusty', 'Conqueror\'s')
SUFFIXES = ('', 'Of Pain', 'Of Doom', 'Of Chaos', 'Of Light')
WEAPONS = ('Sword', 'Dagger', 'Staff', 'Hammer', 'Mace', 'Flail')
ARMORS = ('Chain Mail', 'Plate Mail', 'Scale Mail', 'Leather Jerkin', 'Cuirass')


class Inventory(object):
    def __init__(self):
        self.items = []


class Item(object):
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
        self.value = 0

        # use cases
        self._activate_in_combat = False
        self._activate_outside_encounter = False

        # equipability (most items are not)
        self._equipable = False

    def is_equipable(self):
        return self._equipable

    def can_activate_in_combat(self):
        return self._activate_in_combat

    def can_activate_outside_encounter(self):
        return self._activate_outside_encounter

    def activate(self, target):
        pass

    def __repr__(self):
        return self.name


class Gold(Item):
    def __init__(self, amount):
        Item.__init__(self, 'Gold')

        self.amount = amount
        self.value = amount

    def __repr__(self):
        return '{} gold pieces'.format(self.amount)


class Weapon(Item):
    def __init__(self, name, description=None):
        Item.__init__(self, name, description)

        self._equipable = True

        # percentage
        self._multiplier_min = 1.1
        self._multiplier_max = 1.15

    def get_multiplier_range(self):
        return self._multiplier_min, self._multiplier_max

    def multiplier(self):
        return random.uniform(self._multiplier_min, self._multiplier_max)


def generate_random_weapon(level):
    name = '{} {} {}'.format(random.choice(PREFIXES), random.choice(WEAPONS), random.choice(SUFFIXES)).strip()

    weapon = Weapon(name)

    return weapon


class Armor(Item):
    def __init__(self, name, description=None):
        Item.__init__(self, name, description)

        self._equipable = True

        # percentage
        self._multiplier_min = 1.1
        self._multiplier_max = 1.15

    def get_multiplier_range(self):
        return self._multiplier_min, self._multiplier_max

    def multiplier(self):
        return random.uniform(self._multiplier_min, self._multiplier_max)


def generate_random_armor(level):
    name = '{} {} {}'.format(random.choice(PREFIXES), random.choice(ARMORS), random.choice(SUFFIXES)).strip()

    armor = Armor(name)

    return armor


class Potion(Item):
    def __init__(self, name, level, description=None):
        Item.__init__(self, name, description)

        self._activate_in_combat = True
        self._activate_outside_encounter = True

        self.uses = 1

        self.level = level

    def reset(self):
        self.uses = 1

    def activate(self, target):
        pass


class HealthPotion(Potion):
    def __init__(self, level):
        Potion.__init__(self, 'Health Potion', level)

    def activate(self, target):
        amount = 3
        if self.level == 'medium':
            amount = 5
        elif self.level == 'major':
            amount = 10
        elif self.level == 'mega':
            amount = 15
        target.heal(amount)


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


def generate_random_loot(level, num_items=1):
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
