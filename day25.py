import aoc

data = aoc.getInputForDay(25)

_schematics = data.strip().split("\n\n")

keys = set()
locks = set()

for _s in _schematics:
    s = tuple(tuple(c for c in line) for line in _s.split("\n"))

    if all([c == "." for c in s[0]]):
        keys.add(s)
    elif all([c == "." for c in s[-1]]):
        locks.add(s)
    else:
        raise ValueError("Invalid schematic")


def getLockHeights(lock):
    lockHeight = len(lock)
    lockWidth = len(lock[0])
    heights = []

    for rowIdx in range(lockWidth):
        for colIdx in range(lockHeight):
            if lock[colIdx][rowIdx] == ".":
                heights.append(colIdx - 1)
                break

    return tuple(heights)


def getKeyHeights(key):
    keyHeight = len(key)
    keyWidth = len(key[0])
    heights = []

    for rowIdx in range(keyWidth):
        for colIdx in range(keyHeight - 1, -1, -1):
            if key[colIdx][rowIdx] == ".":
                heights.append(keyHeight - colIdx - 2)
                break

    return tuple(heights)


exampleLock = [
    ["#", "#", "#", "#", "#"],
    [".", "#", "#", "#", "#"],
    [".", "#", "#", "#", "#"],
    [".", "#", "#", "#", "#"],
    [".", "#", ".", "#", "."],
    [".", "#", ".", ".", "."],
    [".", ".", ".", ".", "."],
]


exampleKey = [
    [".", ".", ".", ".", "."],
    ["#", ".", ".", ".", "."],
    ["#", ".", ".", ".", "."],
    ["#", ".", ".", ".", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", ".", "#", "#", "#"],
    ["#", "#", "#", "#", "#"],
]

assert getLockHeights(exampleLock) == (0, 5, 3, 4, 3)
assert getKeyHeights(exampleKey) == (5, 0, 2, 1, 3)


def doFit(lockHeights, keyHeights):
    assert len(lockHeights) == len(keyHeights)
    for l, k in zip(lockHeights, keyHeights):
        if l + k > 5:
            return False
    return True


fitCount = 0
for key in keys:
    for lock in locks:
        if doFit(getLockHeights(lock), getKeyHeights(key)):
            fitCount += 1

print("Part 1", fitCount)
