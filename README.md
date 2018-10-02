# tshrd
The Simple Hard Random Dungeon.

This game is a result of an idea I had for a roguelike. I wanted it to be
very simple (not a complicated RPG or fully-featured roguelike) while still
being difficult. 

## Current State

Very early development, but it should at least be running.

## Requirements

- Python 3.6+
- [tdl library](https://python-tdl.readthedocs.io/en/latest/)

## Setup

- Download/clone this repo
- `cd` into the repo folder
- Install dependencies via `pipenv` or `pip`

## Running the game

If using pipenv:

    pipenv shell

Otherwise, activate a virtualenv your own way (or don't, it is
up to you).

*Finally,*

    python -m tshrd
    
## How to Play

*Most of this section is still being written.*

### Goal

The goal is to get as far in the dungeon as you can before you get killed by
a monster or a trap or you starve to death.

### Moving through the dungeon

Unlike traditional roguelikes, in *tshrd* you do *not* move around one tile at
a time. Instead, you move room-to-room via selecting a direction to travel 
(north, south, etc.).

Each room in the map has a chance to be one of several different encounter
types, including monsters, treasure and shrines. Certain encounter types,
such as monsters, will not allow the player to progress unless they are
resolved.

Every time you move from room you consume some of your food stores, which
function as a turn timer and limit to the game: once you run out of food,
you will lose health every turn instead, until you die.

On each level of the dungeon is a room with stairs to the next level of the
dungeon. The deeper into the dungeon you go, the harder the monsters and
other encounters will be.

### Reaching the end

There is no end to the dungeon. The evil wizard is also insane and
has enchanted the dungeon so that it will always have another level to it.
You will die... it is just a matter of time.

### Key Bindings

Key bindings are somewhat situational, changing depending on what the active
state is. However, here are some common ones:

**Arrow keys:**

Moving between rooms and scrolling the map in the map viewer.

**Escape:**

Exits the game (in most cases).

**i:**

Opens the character's inventory screen.

**y/n:**

Responding yes/no (confirm/deny, etc.) for prompts.

## Items and Gear

The player can equip one weapon and one armor, both of which alter his base
stats. There are also other kinds of items, like potions, which have
various effects.

### Potions

_Coming soon_

### Weapons

There are the following kinds of weapons:

- Sword
- Dagger
- Staff
- Hammer
- Mace
- Flail

_Currently, the different weapon types are purely cosmetic in nature.
Eventually, they will differ more._

Weapons have the following stats:

**Hit chance modifier:** Adjusts the character's chance to hit.

**Crit chance modifier:** Adjusts the character's chance to get a critical
hit. An unarmed character cannot get critical hits.

**Damage:** Weapon damage adds to the possible maximum damage the character
can do in combat.

#### Weapon Suffixes

Different weapon suffixes guarantee specific effects on the weapon.

##### Pain

Weapons with the "of Pain" suffix deal more damage on a successful hit.

##### Vampirism

Weapons with the "of Vampirism" suffix have a _chance_ to heal the wielder
after doing damage.

##### Adventuring

These weapons boost the amount of _XP_ gained by the wielder when they
kill monsters.

##### Doom

When damage is dealt, if the target's remaining health is only `1`
hit point, then the target takes bonus damage and is killed.

#### Weapon Prefixes

##### Heavy

Heavy weapons are unwieldly, making the bearer slower and therefore less
likely to hit their target.

##### Blessed

Blessed weapons gain a damage bonus.

##### Cursed

Cursed weapons deal less damage.

##### Broken

A broken weapon is basically useless... but it might be better than going
empty-handed.

##### Mastercraft

A weapon truly crafted by a master blacksmith, these weapons have an expanded
critical range, making the wielder more likely to score a critical hit.

### Armor

These are the kinds of armor in the game:

- Chain Mail
- Plate Mail
- Scale Mail
- Leather Jerkin
- Cuirass

_Currently these different types of armor are cosmetic only._

Armors have the follow attributes:

**Block:** adds to the character's defense.

#### Armor Suffixes

##### Adventuring

These armors boost the amount of _XP_ gained by the wearer when they
kill monsters.

##### Fleeing

The armor of the coward. These armors will defend the wearer from attacks
when they try to flee combat.

#### Armor Prefixes

##### Swift

_Swift_ armor weighs less, allowing better movement. Player have a
chance to consume no food while traveling between rooms.

##### Dodging

_Dodging_ armor gives the wearer a small chance to completely avoid an
attack.

##### Mastercraft

A master armorer crafted this armor, and it absorbs more damage.

## Skills

Skills are special powers (or _moves_) that the player can use to aid his
journey. Skills may be _active_ or _passive_. The player can only _know_ 
two Skills at a time, so in order to learn a new skill he will have to 
replace an old one.

### Active Skills

Active Skills are directly used by the player, assuming they are allowed
to be used at that particular time.

#### Wham!

_Headbutt the enemy, dealing a little damage and possibly stunning_
_the enemy for one turn._

_Can only be used in combat._

_3 turn cooldown._

#### Gift of the Seer

_Reveal the encounter of all rooms adjacent to the_
_one you are currently in._

_Cannot be used during an encounter._

_10 turn cooldown._

_Possibly have a more powerful version that reveals more of the map?_

#### Shield

_Raises your defenses, allowing you to completely block all damage for the_
_next turn._

_Can only be used in combat._

_Does not use up your turn._

_5 turn cooldown._

#### Cure Wounds

_Heal yourself for 30% of your maximum health._

_Consumes 1 turn (so out of combat it will use food resource)._

_4 turn cooldown._

#### Prayer

_Pray for a blessing, giving you an advantage on your next action._

_Can only be used in combat._

_Does not use up your turn._

_3 turn cooldown._

### Passive Skills

Passive Skills have effects that occur based on the description of the skill.
They do not have to be activated.

#### Endurance

_You handle the environment better and are able to spread your food rations_
_out further. You consume less food._

#### One More Step

_While below 20% health, you slowly gain health._

#### Blood of the Warrior

_When you do damage to a monster, you deal extra damage._

#### Lucky

_The coin flips in your favor more often. Your chances for better loot_
_have increased._

#### Initiative

_Your first attack on a monster does bonus damage._

#### Cowardly

_You can always flee a non-boss monster for free._

#### The Best Defense...

_...is a good offense. Your attacks do more damage, but your Block has been reduced._

#### Perception

_You gain an advantage against traps._
