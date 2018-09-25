import random
from tshrd.characters import Character


MONSTERS_BASE = (
    {
        'name': 'Rat',
        'tile': 'r'
    },
    {
        'name': 'Bat',
        'tile': 'b',
        'mods': {
            'power': 1
        }
    },
    {
        'name': 'Lizard',
        'tile': 'l',
        'mods': {
            'power': 3,
            'block': 2
        }
    },
    {
        'name': 'Kobold',
        'tile': 'k',
        'mods': {
            'power': 1
        },
        'prefixes': ['Large', 'Small']
    },
    {
        'name': 'Ratman',
        'tile': 'R',
        'mods': {
            'health': 2,
            'power': 1
        }        
    }
)

# These monsters are allowed to have "roles" (ie, "Kobold Warrior")
MONSTERS_WITH_ROLES = (
    'Kobold',
    'Ratman'
)

MONSTER_PREFIX_MODIFIERS = (
    {
        'name': 'Large',
        'mods': {
            'health': 4,
            'block': 1,
            'xp': 1
        }
    },
    {
        'name': 'Dire',
        'mods': {
            'health': 4,
            'block': 2,
            'power': 2,
            'xp': 4
        }
    },
    {
        'name': 'Small',
        'mods': {
            'health': -2,
            'power': -1,
            'xp': -1
        }
    }
)

MONSTER_BASE_DATA_BY_LEVEL = (
    # Level 1
    {
        'health': 4,
        'power': 2,
        'block': 0,
        'xp': 2
    },
    # Level 2
    {
        'health': 6,
        'power': 3,
        'block': 1,
        'xp': 3
    },
    # Level 3
    {
        'health': 8,
        'power': 4,
        'block': 2,
        'xp': 4
    }
)


def create_monster_for_level(level: int=1,
                             monster_pool: list=None,
                             prefix_pool: list=None,
                             force_prefix: bool=False) -> Character:
    monster = Character()
    base_stats = MONSTER_BASE_DATA_BY_LEVEL[level - 1]
    monster.max_health = base_stats['health']
    monster.power = base_stats['power']
    monster.block = base_stats['block']

    monster_base = random.choice(MONSTERS_BASE) if not monster_pool else random.choice([base for base in MONSTERS_BASE if base['name'] in monster_pool])
    if 'mods' in monster_base:
        if 'health' in monster_base['mods']:
            monster.max_health += monster_base['mods']['health']
        if 'power' in monster_base['mods']:
            monster.power += monster_base['mods']['power']
        if 'block' in monster_base['mods']:
            monster.block += monster_base['mods']['block']

    prefix_modifier_chance = 65
    has_prefix_modifier = random.randint(1, 101) <= prefix_modifier_chance or force_prefix
    prefix_mod = None
    if has_prefix_modifier:
        prefix_mod = random.choice(MONSTER_PREFIX_MODIFIERS) if not prefix_pool else random.choice(
            [pref for pref in MONSTER_PREFIX_MODIFIERS if pref['name'] in prefix_pool])
        if 'mods' in prefix_mod:
            if 'health' in prefix_mod['mods']:
                monster.max_health += prefix_mod['mods']['health']
            if 'power' in prefix_mod['mods']:
                monster.power += prefix_mod['mods']['power']
            if 'block' in prefix_mod['mods']:
                monster.block += prefix_mod['mods']['block']

    monster.name = f'{prefix_mod["name"] + " " if prefix_mod else ""}{monster_base["name"]}'
    monster.tile = monster_base['tile']
    monster.reset()

    # experience points
    base_level_xp = base_stats['xp']
    prefix_bonus_xp = prefix_mod['xp'] if prefix_mod and 'xp' in prefix_mod else 0
    final_xp = base_level_xp - prefix_bonus_xp
    monster.experience = final_xp

    return monster


def tests():
    # for testing purposes

    random.seed(42)

    level = 1

    for i in range(0, 5):
        m = create_monster_for_level(level)

        print(f'{m.name}    HP: {m.max_health}  POWER: {m.power}  BLOCK: {m.block}')


if __name__ == '__main__':
    tests()
