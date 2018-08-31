from tshrd.inventory import Inventory, Weapon, Armor, HealthPotion, PotionStrength, Item


class Character(object):
    def __init__(self):
        self.name = ''

        self.tile = '@'
        self.health = 0
        self.max_health = 0
        self.food = 0
        self.experience = 0
        self.experience_to_next_level = 0
        self.level = 1

        # combat stats
        self.power = 0
        self.block = 0
        self.hit_chance = 75
        # by default, if character is "unarmed", crit chance will be 0
        self.crit_chance = 0

        self.weapon: Weapon = None
        self.armor: Armor = None

        self.inventory: Inventory = Inventory()

    def reset(self):
        self.health = self.max_health

    def grant_experience(self, amount: int):
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience_to_next_level = self.experience_to_next_level * 1.5

    def take_damage(self, amount: int) -> int:
        amount = amount - self.get_block()
        self.health -= amount
        return amount

    def heal(self, amount: int) -> int:
        # Heal the character for the given amount. Cannot go above max health.
        new_health = min(self.max_health, self.health + amount)
        amount_changed = new_health - self.health
        self.health = new_health
        return amount_changed

    def is_item_equipped(self, item: Item) -> bool:
        return item == self.weapon or item == self.armor

    def unequip_item(self, item: Item) -> str:
        if item == self.weapon:
            self.weapon = None
            return f'You unequipped your weapon, {item.name}'
        elif item == self.armor:
            self.armor = None
            return f'You unequipped your armor, {item.name}'
        return None

    def equip_item(self, item: Item) -> str:
        if self.is_item_equipped(item):
            return f'{item.name} is already equipped.'
        if isinstance(item, Weapon):
            self.weapon = item
        elif isinstance(item, Armor):
            self.armor = item
        return f'You equipped {item.name}'

    @property
    def combined_crit_chance(self) -> int:
        # TODO: add up character stat + stat(s) or items, skills, etc.
        chance = self.crit_chance
        if self.weapon:
            chance += self.weapon.crit_chance_modifier
        return chance

    @property
    def combined_hit_chance(self) -> int:
        # TODO: add up character stat + stat(s) or items, skills, etc.
        return 75

    # @property
    # def combined_block_chance(self) -> int:
    #     # TODO: add up character stat + stat(s) or items, skills, etc.
    #     return 10

    @property
    def combined_block(self) -> int:
        block = self.block
        if self.armor:
            block += self.armor.block
        return block

    @property
    def min_damage(self) -> int:
        return self.power

    @property
    def max_damage(self) -> int:
        damage = self.power
        if self.weapon:
            damage += self.weapon.damage
        return damage


def create_player(name: str='Player') -> Character:
    player = Character()
    player.name = name

    player.block = 2
    player.power = 4
    player.max_health = player.health = 10

    # give player some starting gear
    player.weapon = Weapon('Shortsword', 'A basic short sword.')
    player.armor = Armor('Leather Armor', 1, 'Passable armor made out of leather. You should get some better armor soon if you want to survive.')
    player.inventory.add_item(player.weapon)
    player.inventory.add_item(player.armor)
    player.inventory.add_item(HealthPotion(PotionStrength.Minor))

    # TODO: remove this test later
    for i in range(0, 50):
        hp = HealthPotion(PotionStrength.Minor)
        hp.name += f' {i}'
        player.inventory.add_item(hp)

    player.experience_to_next_level = 10

    player.food = 20

    return player
