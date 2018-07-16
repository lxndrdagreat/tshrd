from tshrd.state_handling import GameData, GameState
from tshrd.state_handling import state_encounter_monster, state_game_over, state_encounter_shrine, state_encounter_trap, \
    state_encounter_treasure, state_in_room, state_map, state_move
from tshrd.utils import WindowClosedException
import tdl
import os
import random


def start():
    random.seed(42)

    active_game = None
    active_state = GameState.GAME_RESTART
    font_path = os.path.join(os.path.dirname(__file__), 'arial10x10.png')
    tdl.set_font(font_path, greyscale=True, altLayout=True)
    root_console = tdl.init(80, 50, title='TSHRD v0.1', fullscreen=False)
    tdl.setFPS(20)

    state_handlers = {
        GameState.ROOM: state_in_room.state,
        GameState.MOVE_NORTH: state_move.state,
        GameState.MOVE_WEST: state_move.state,
        GameState.MOVE_EAST: state_move.state,
        GameState.MOVE_SOUTH: state_move.state,
        GameState.ENCOUNTER_MONSTER: state_encounter_monster.state,
        GameState.ENCOUNTER_TRAP: state_encounter_trap.state,
        GameState.ENCOUNTER_SHRINE: state_encounter_shrine.state,
        GameState.ENCOUNTER_TREASURE: state_encounter_treasure.state,
        GameState.GAME_OVER: state_game_over.state,
        GameState.MAP: state_map.state
    }

    while not tdl.event.is_window_closed() and active_state != GameState.CLOSE:
        if active_state == GameState.GAME_RESTART:
            # create a new game
            active_game = GameData()
            active_state = GameState.ROOM
            continue
        active_game.state = active_state
        try:
            state_update = state_handlers[active_state](active_game, root_console)
            if state_update:
                active_state = state_update
        except WindowClosedException:
            # game over
            break


if __name__ == '__main__':

    start()
