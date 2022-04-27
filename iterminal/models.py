from iterminal.constants import UP, DOWN, LEFT, RIGHT, WORLD_HEIGHT, WORLD_WIDTH
from copy import copy, deepcopy


class BaseGameObject:
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char
        self.die = False

    def move(self, dir, amt=1):
        if dir == UP:
            if self.y > 0:
                self.y -= amt
        elif dir == DOWN:
            if self.y < WORLD_HEIGHT-1:
                self.y += amt
        elif dir == LEFT:
            if self.x > 0:
                self.x -= amt
        elif dir == RIGHT:
            if self.x < WORLD_WIDTH-1:
                self.x += amt

    def step(self):
        raise NotImplementedError


class WorldGrid:
    def __init__(self):
        self.grid = [['.'] * WORLD_WIDTH for _ in range(WORLD_HEIGHT)]
        self.gameObjects = []

    def addObject(self, obj):
        self.gameObjects.append(obj)

    def getGrid(self):
        tmp = deepcopy(self.grid)
        for each in self.gameObjects:
            try:
                tmp[each.y][each.x] = each.char
            except IndexError:
                each.die = True

        return tmp

    def step(self):
        for each in self.gameObjects:
            each.step()

    def cleanup(self):
        self.gameObjects = [x for x in self.gameObjects if not x.die]


class Bullet(BaseGameObject):
    def __init__(self, x, y, dir):
        super().__init__(x, y, 'o')
        self.dir = dir
        self.speed = 4 if dir in [LEFT, RIGHT] else 1
        self.stepCount = 0
        self.maxStepCount = 10

    def step(self):
        self.move(self.dir, amt=self.speed)
        self. stepCount += 1
        if self.stepCount > self.maxStepCount:
            self.die = True


class Player(BaseGameObject):
    def __init__(self, gameObject, x=WORLD_WIDTH//2, y=WORLD_HEIGHT//2):
        super().__init__(x, y, 'i')
        self.gameObject = gameObject

    def shoot(self, dir):
        self.gameObject.addObject(Bullet(self.x, self.y, dir))

    def step(self):
        pass


