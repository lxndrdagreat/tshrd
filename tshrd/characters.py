from tshrd.inventory import Inventory, Weapon, Armor, HealthPotion


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

    @property
    def crit_chance(self) -> int:
        return 1

    @property
    def hit_chance(self) -> int:
        return 75

    @property
    def block_chance(self) -> int:
        return 10


def create_player(name: str='Player') -> Character:
    player = Character()
    player.name = name

    player.block = 2
    player.power = 4
    player.max_health = player.health = 10

    # give player some starting gear
    player.weapon = Weapon('Shortsword', 'A short sword.')
    player.armor = Armor('Leather Armor')
    player.inventory.add_item(player.weapon)
    player.inventory.add_item(player.armor)
    player.inventory.add_item(HealthPotion('minor'))

    # TODO: remove this test later
    for i in range(0, 25):
        hp = HealthPotion('minor')
        hp.name += f' {i}'
        player.inventory.add_item(hp)

    player.experience_to_next_level = 10

    player.food = 20

    return player
