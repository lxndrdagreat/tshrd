import random
from tshrd.inventory import Inventory, Item, Weapon, Armor


class Character(object):
    def __init__(self):
        self.name = ''

        self.tile = '@'
        self.power = 0
        self.block = 0
        self.health = 0
        self.max_health = 0
        self.food = 0
        self.experience = 0
        self.experience_to_next_level = 0
        self.level = 1

        self.weapon = None
        self.armor = None

        self.inventory = Inventory()

    def reset(self):
        self.health = self.max_health

    def grant_experience(self, amount):
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience_to_next_level = self.experience_to_next_level * 1.5

    def take_damage(self, amount):
        amount = amount - self.get_block()
        self.health -= amount
        return amount

    def get_attack_power(self):
        return float(self.power) * (self.weapon.multiplier() if self.weapon else random.uniform(0.85, 1.15))

    def get_block(self):
        return float(self.block) * (self.armor.multiplier() if self.armor else 1.0)

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)


def create_player(name: str='Player') -> Character:
    player = Character()
    player.name = name

    player.block = 2
    player.power = 4
    player.max_health = player.health = 10

    player.weapon = Weapon('Shortsword', 'A short sword.')
    player.armor = Armor('Leather Armor')

    player.inventory.items.append(player.weapon)
    player.inventory.items.append(player.armor)

    player.experience_to_next_level = 10

    player.food = 20

    return player
