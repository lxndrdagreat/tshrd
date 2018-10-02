from tshrd.inventory import Inventory, Weapon, Armor, HealthPotion, PotionStrength, Item
from tshrd.inventory import generate_random_weapon, generate_random_armor
from tshrd.skills import Skill, SkillType, GiftOfTheSeerSkill, WhamCombatSkill, CureWoundsSkill
from tshrd.status_effect import StatusEffectType, AppliedStatusEffect


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

        # unassigned level-up points
        self._unassigned_points = 0

        # combat stats
        self.power = 0
        self.block = 0
        self.hit_chance = 75
        # by default, if character is "unarmed", crit chance will be 0
        self.crit_chance = 0

        self.weapon: Weapon = None
        self.armor: Armor = None

        self.inventory: Inventory = Inventory()

        # skills
        self.skills: list = []

        # status effects
        self._status_effects: list = []

    def reset(self):
        self.health = self.max_health

    def grant_experience(self, amount: int) -> bool:
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level_up()
            return True
        return False

    def level_up(self):
        self.level += 1
        self._unassigned_points += 2
        self.experience_to_next_level = int(self.experience_to_next_level * 2.5)

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

    def spend_points(self, points: int):
        self._unassigned_points = max(self._unassigned_points - points, 0)

    def apply_status_effect(self, effect: StatusEffectType, duration: int):
        existing = next((status for status in self._status_effects if status.status_effect == effect), None)
        if existing:
            existing.duration += duration
            return
        self._status_effects.append(AppliedStatusEffect(effect, duration))

    def has_status_effect(self, effect: StatusEffectType) -> bool:
        return next((applied for applied in self._status_effects if applied.status_effect == effect), None) is not None

    def tick_status_effects(self):
        for status_effect in self._status_effects:
            # TODO: handle dangerous status effects
            status_effect.tick()
        self._status_effects = [active_status for active_status in self._status_effects if not active_status.is_done()]

    @property
    def active_status_effects(self):
        return self._status_effects

    @property
    def applied_status_effects(self) -> list:
        return self._status_effects

    @property
    def unspent_points(self) -> int:
        return self._unassigned_points

    @property
    def combined_crit_chance(self) -> int:
        chance = self.crit_chance
        if self.weapon:
            chance += self.weapon.crit_chance_modifier
        return chance

    @property
    def combined_hit_chance(self) -> int:
        chance = self.hit_chance
        if self.weapon:
            chance += self.weapon.hit_chance_modifier
        return chance

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
    def combined_dodge_chance(self) -> int:
        chance = 0
        if self.armor:
            chance += self.armor.dodge_chance
        return chance

    @property
    def min_damage(self) -> int:
        return self.power

    @property
    def max_damage(self) -> int:
        damage = self.power
        if self.weapon:
            damage += self.weapon.damage
        return damage

    def get_combat_skills(self) -> list:
        return [skill for skill in self.skills if skill.can_activate_in_combat]

    def get_explore_skills(self) -> list:
        return [skill for skill in self.skills if skill.can_activate_outside_encounter]

    def reset_combat_skills(self):
        for skill in self.get_combat_skills():
            skill.reset_cooldown()

    def tick_skill_cooldowns(self):
        for skill in self.skills:
            skill.tick()


def create_player(name: str='Player', power: int=4, block: int=2, health: int=10) -> Character:
    player = Character()
    player.name = name

    player.block = block
    player.power = power
    player.max_health = player.health = health

    # give player some starting gear
    # player.weapon = Weapon('Shortsword', 'A basic short sword.')
    player.weapon = generate_random_weapon(1, 0, 0)
    # player.armor = Armor('Leather Armor', 1, 'Passable armor made out of leather.')
    player.armor = generate_random_armor(1, 0, 0)
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

    # TODO: remove this temporary skill stuff later
    player.skills.append(GiftOfTheSeerSkill())
    player.skills.append(CureWoundsSkill())
    player.skills.append(WhamCombatSkill())

    return player
