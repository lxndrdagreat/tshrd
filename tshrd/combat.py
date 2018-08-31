import random
from tshrd.characters import Character


class AttackResult:
    def __init__(self):
        self.damage = 0
        self.damage_blocked = 0
        self.defender_killed = False
        self.critical_hit = False
        self.critical_miss = False


def do_attack(attacker: Character, defender: Character) -> AttackResult:
    did_crit = False
    attack_result = AttackResult()

    critical_chance = attacker.combined_crit_chance
    attack_chance = attacker.combined_hit_chance

    # roll for attack on a d100
    attack_roll = random.randint(1, 101)
    did_hit = attack_roll <= attack_chance
    did_crit = attack_roll <= critical_chance

    damage_roll = 0

    if did_hit:
        # roll for damage amount
        damage_roll = random.randint(attacker.min_damage, attacker.max_damage + 1)

        if did_crit:
            # Apply extra damage for critical hit
            damage_roll += attacker.max_damage

    # subtract defender's block from the damage
    damage = max(0, damage_roll - defender.combined_block)

    defender.health -= damage

    attack_result.damage = damage
    attack_result.damage_blocked = defender.combined_block if defender.combined_block < damage_roll else damage_roll
    attack_result.defender_killed = defender.health <= 0
    attack_result.critical_hit = did_crit
    return attack_result
