import time
import threading
from curses import wrapper
import curses

from iterminal.controllers import inputController
from iterminal.models import WorldGrid, Player
from iterminal.views import GameScreen, Debug

EDGEBUFFER = 10


def adjustGameClock(prev_time, stdscr=None):
    delta_time = time.time() - prev_time
    remaining_time = 1 / 30 - delta_time
    if remaining_time > 0:
        if stdscr:
            stdscr.addstr(0, 0, '{}, {}       '.format(*p))
        time.sleep(remaining_time)


def main(stdscr):
    #setup
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.refresh()
    grid = WorldGrid()
    user = Player(grid)
    grid.addObject(user)
    screen = GameScreen(5, 15)
    inputThread = threading.Thread(target=inputController, args=(stdscr, user))
    inputThread.start()

    # main game loop
    while True:
        prev_time = time.time()
        grid.step()
        screen.update(stdscr, grid)
        stdscr.refresh()
        grid.cleanup()
        adjustGameClock(prev_time)

    curses.endwin()



wrapper(main)
