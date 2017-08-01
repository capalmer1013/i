#!/usr/bin/python
import curses
import time
import random

# heres how you make a 64 bit seed
'{0:064b}'.format(random.getrandbits(64))
class character:
    def __init__(self, x, y, icon="O"):
        self.x = x
        self.y = y
        self.nextX = 0
        self.nextY = 0
        self.icon = icon
        self.lastMove = 0
        self.speed = .1

    def moveX(self, magnitude):
        if time.time() - self.lastMove >= self.speed:
            self.nextX += magnitude
            self.lastMove = time.time()

    def moveY(self, magnitude):
        if time.time() - self.lastMove >= self.speed:
            self.nextY += magnitude
            self.lastMove = time.time()

    def draw(self, scr):
        scr.addch(self.y, self.x, " ")
        scr.addch(self.nextY, self.nextX, self.icon)
        self.x = self.nextX
        self.y = self.nextY

    def collision(self, listOfObjects, max_X=0, max_Y=0):
        if max_X and max_Y:
            if self.nextX == max_X or self.nextY == max_Y:
                return True

        if (self.nextX, self.nextY) in listOfObjects:
            return True
        else:
            return False

    def undoMove(self):
        self.nextX = self.x
        self.nextY = self.y

class wall:
    def __init__(self, x, y, icon="X"):
        self.x = x
        self.y = y
        self.icon = icon

    def draw(self, scr):
        scr.addch(self.y, self.x, self.icon, curses.color_pair(1))

    def moved(self):
        return False


def main(scr):
    listOfObjects = []
    objectPos = []
    running = True
    scr.nodelay(1)
    scr.border()
    scr.timeout(1)
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
    max_y, max_x = scr.getmaxyx()
    player = character(2, 2, "i")
    for _ in range(100):
        listOfObjects.append(wall(random.randint(2, max_x-1), random.randint(2, max_y-1),curses.ACS_BLOCK))

    for each in listOfObjects:
        each.draw(scr)
        objectPos.append((each.x, each.y))

    while running:
        c = scr.getch()
        if c == ord('q'):
            running = False
        elif c == curses.KEY_UP:
            player.moveY(-1)

        elif c == curses.KEY_DOWN:
            player.moveY(1)

        elif c == curses.KEY_RIGHT:
            player.moveX(1)

        elif c == curses.KEY_LEFT:
            player.moveX(-1)

        if player.collision(objectPos):
            player.undoMove()

        player.draw(scr)

        for each in listOfObjects:
            if each.moved():
                each.draw(scr)
                objectPos.remove((each.previousX, each.previousY))
                objectPos.append((each.x, each.y))

if __name__ == "__main__":
    curses.wrapper(main)
