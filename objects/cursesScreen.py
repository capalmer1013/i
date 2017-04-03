import curses


def main(scr):
    scr.nodelay(1)
    scr.timeout(1)
    scr.border()
    curses.echo()
    max_y, max_x = scr.getmaxyx()

    mainWindow = curses.newwin(25, 75, 3, 3)
    chatWindow = curses.newwin(10, 50, 28, 3)
    infoWindow = curses.newwin(10, 25, 28, 53)

    mainWindow.border()
    chatWindow.border()
    infoWindow.border()

    running = True
    scr.refresh()
    mainWindow.addstr(0, 0, "GameWindow", curses.A_REVERSE)
    chatWindow.addstr(0, 0, "ChatWindow", curses.A_REVERSE)
    infoWindow.addstr(0, 0, "InfoWindow", curses.A_REVERSE)

    chatWindow.addstr(1, 1, ">>> ")


    mainWindow.refresh()
    infoWindow.refresh()
    chatWindow.refresh()



    while running:
        c = scr.getch()

        if c == ord('q'):
            running = False

if __name__ == "__main__":
    curses.wrapper(main)
