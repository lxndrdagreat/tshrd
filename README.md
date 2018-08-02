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