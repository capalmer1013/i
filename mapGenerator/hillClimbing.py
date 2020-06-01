import random
import string
import json

stringList = [char for char in string.ascii_lowercase + string.punctuation + string.digits]
random.shuffle(stringList)

def createPeaks(size, points):
    result = []
    for _ in range(size):
        row = []
        for _ in range(size):
            nums = [random.randint(75, 100)]*points
            blank = [None] * (size * size - points)
            row.append(random.choice(nums + blank))
        result.append(row)
    return result


def printGrid(grid):
    for eachx in grid:
        line = ""
        for eachy in eachx:
            if eachy:
                #line += str(eachy).ljust(3)
                line += stringList[eachy % len(stringList)]
            else:
                line += " "
                #line += " ".ljust(3)

        print(line)


def left(grid, x, y):
    if x > 0:
        if not grid[x-1][y]:
            grid[x-1][y] = abs(grid[x][y] - 1)


def up(grid, x, y):
    if y > 0:
        if not grid[x][y-1]:
            grid[x-1][y] = abs(grid[x][y] - 1)


def right(grid, x, y):
    try:
        if not grid[x+1][y]:
            grid[x+1][y] = abs(grid[x][y] - 1)
    except Exception:
        pass


def down(grid, x, y):
    try:
        if not grid[x][y+1]:
            grid[x][y+1] = abs(grid[x][y] - 1)
    except Exception:
        pass


def addSlope(grid, x, y):
    directions = [left, up, right, down]
    random.choice(directions)(grid, x, y)


def fillGrid(grid, gridDensity):
    for _ in range(gridDensity):
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if grid[x][y]:
                    addSlope(grid, x, y)

    return grid


def fillZeros(grid):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if not grid[x][y]:
                grid[x][y] = 1
    return grid


a = createPeaks(75, 75)
a = fillGrid(a, 20)
#a = fillZeros(a)

printGrid(a)
json.dump(a, open("test.json", "w"))