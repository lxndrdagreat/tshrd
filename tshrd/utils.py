# utility functions
import tdl
import random


class WindowClosedException(Exception):
    pass


def wait_for_keys(keys=('ENTER', 'SPACE', 'ESCAPE',)) -> str:
    """
    Helper function that waits until one of the provided keys is pressed,
    then returns that key's string code.

    Will also raise an exception if the window is closed.
    """
    # TODO: allow using regex (i.e., a-z)
    e = tdl.event.key_wait()
    while not ((e.key and e.key in keys) or (e.char and e.char in keys)):
        if tdl.event.is_window_closed():
            raise WindowClosedException()
        e = tdl.event.key_wait()

    if e.key and e.key == 'CHAR':
        if e.shift:
            return e.char.capitalize()
        return e.char
    return e.key


def draw_player_status_bar(the_player, x: int, y: int, root_console: tdl.Console):
    """
    Helper function that draws the player's status bar at the bottom
    of the screen.
    """
    root_console.draw_rect(0, root_console.height - 3, root_console.width, 3, None, bg=(200, 200, 200))

    name = f'@{the_player.name}'
    food = f'FOOD: {the_player.food}'
    health = f'{the_player.health}/{the_player.max_health}HP'
    level = f'LEVEL {the_player.level}'
    xp = f'{the_player.experience}/{the_player.experience_to_next_level}XP'

    root_console.draw_str(x, y, name, fg=(0, 0, 0), bg=None)

    x += len(name) + 4

    root_console.draw_str(x, y, health, fg=(0, 0, 0), bg=None)

    x += len(health) + 4

    root_console.draw_str(x, y, food, fg=(0, 0, 0), bg=None)

    x += len(food) + 4

    root_console.draw_str(x, y, level, fg=(0, 0, 0), bg=None)

    x += len(level) + 4

    root_console.draw_str(x, y, xp, fg=(0, 0, 0), bg=None)


def weighted_choice(choices):
    """
    Returns a random item from a list based on weight
    :param choices:
    :return:
    """
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    assert False, 'Shouldn\'t get here'
