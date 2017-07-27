import time

class baseCharacter:
    # base class for all characters, npc's, players to inheirit from
    def __init__(self):
        pass

    def moveX(self, magnitude):
        if time.time() - self.lastMove >= self.speed:
            self.nextX += magnitude
            self.lastMove = time.time()
            
    def moveY(self, magnitude):
        if time.time() - self.lastMove >= self.speed:
            self.nextY += magnitude
            self.lastMove = time.time()
            
    def draw(self, scr):
        scr.addch(self.y, self.x,  " ")
        scr.addch(self.nextY, self.nextX, self.icon)
        self.x = self.nextX
        self.y - self.nextY

    def collision(self, listOfObjects, max_X=0, max_y=0):
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
        

class mainPlayer:
    def __init__(self, x, y, icon="i"):
        self.x = x
        self.y = y
        self.nextX = 0
        self.nextY = 0
        self.icon = icon
        self.lastMove = 0
        self.speed = .1
        
    def moveX(self, mag):
        pass
