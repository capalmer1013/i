import curses
from iterminal.constants import UP, DOWN, LEFT, RIGHT


def inputController(stdscr, p):
    while True:
        key = stdscr.getch()
        #stdscr.addstr(0, 0, str(key))
        dirDict = {curses.KEY_UP: UP, curses.KEY_DOWN: DOWN, curses.KEY_LEFT: LEFT, curses.KEY_RIGHT: RIGHT}
        shootDict = {ord('w'): UP, ord('a'): LEFT, ord('s'): DOWN, ord('d'): RIGHT}
        if key in dirDict.keys():
            p.move(dirDict[key])
        elif key in shootDict.keys():
            p.shoot(shootDict[key])