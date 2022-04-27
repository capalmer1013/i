class GameScreen:
    def __init__(self, xoffset, yoffset):
        self.xoffset = xoffset
        self.yoffset = yoffset

    def update(self, stdscr, grid):
        g = grid.getGrid()
        for i in range(len(g)):
            for j in range(len(g[i])):
                stdscr.addch(i+self.xoffset, j+self.yoffset, g[i][j])

class Debug:
    def __init__(self):
        pass
