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
    attacks = 0
    defenses = 0
    did_crit = False
    attack_result = AttackResult()

    critical_chance = attacker.crit_chance
    attack_chance = attacker.hit_chance
    defense_chance = defender.block_chance

    for i in range(0, attacker.power):
        # roll a d100
        attack_roll = random.randint(1, 101)        
        if attack_roll <= attack_chance:
            attacks += 1
            if attack_roll <= critical_chance:
                did_crit = True

    for i in range(0, defender.block):
        # roll a d100
        defense_roll = random.randint(1, 101)        
        if defense_roll <= defense_chance:
            defenses += 1

    damage = 0

    # If the attacker scored a critical hit, double the attacks value
    if did_crit:
        attacks *= 2

    if attacks - defenses > 0:
        damage = attacks - defenses

    defender.health -= damage

    attack_result.damage = damage
    attack_result.damage_blocked = defenses
    attack_result.defender_killed = defender.health <= 0
    attack_result.critical_hit = did_crit
    attack_result.critical_miss = attacks == 0
    return attack_result
