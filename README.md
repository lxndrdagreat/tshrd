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