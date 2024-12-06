import aoc
import copy

grid = aoc.getCellsForDay(6)
# grid = aoc.getCellsForDay(6, force_filepath="inputs/day06_example.txt")


# Find guard
startCoord = None
for y in range(len(grid)):
    for x in range(len(grid[y])):
        if grid[y][x] == "^":
            startCoord = (x, y)

assert startCoord


def turnRight(dir):
    if dir == (0, 1):
        return (-1, 0)
    if dir == (-1, 0):
        return (0, -1)
    if dir == (0, -1):
        return (1, 0)
    if dir == (1, 0):
        return (0, 1)

    assert False


def isInGrid(grid, coords):
    x, y = coords
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])


def isObstacle(grid, coords):
    return grid[coords[1]][coords[0]] == "#"


def simulate(grid, startCoord):
    """@returns (visitedCells, isInLoop)"""

    guardCoord = startCoord
    guardDir = (0, -1)  # Always start facing up

    # Keep track of visited cells
    visitedCells = set()
    visitedCells.add(guardCoord)

    # Keep all states (position + direction) so we can detect a loop
    savedStates = set()
    savedStates.add((guardCoord, guardDir))

    while True:
        newCoord = (guardCoord[0] + guardDir[0], guardCoord[1] + guardDir[1])
        newState = (newCoord, guardDir)

        if newState in savedStates:
            # We are in a loop
            return visitedCells, True
        else:
            savedStates.add(newState)

        # Move guard
        if isInGrid(grid, newCoord) and not isObstacle(grid, newCoord):
            guardCoord = newCoord
            visitedCells.add(newCoord)
        elif isInGrid(grid, newCoord) and isObstacle(grid, newCoord):
            guardDir = turnRight(guardDir)
        else:
            break

    return (visitedCells, False)


# Part 1
(visitedCells, isInLoop) = simulate(grid, startCoord)

assert not isInLoop

print("Part 1", len(visitedCells))

# Part 2: find all obstacles which would make the guard path a loop
# Try every position in the path

validObstacles = set()

for simulationIdx, cellCoord in enumerate(visitedCells):
    if cellCoord == startCoord:
        continue

    print(simulationIdx, "/", len(visitedCells))

    # Make a multiverse grid with one obstacle
    newGrid = copy.deepcopy(grid)
    newGrid[cellCoord[1]][cellCoord[0]] = "#"

    (_, isInLoop) = simulate(newGrid, startCoord)
    if isInLoop:
        validObstacles.add(cellCoord)

print("Part 2", len(validObstacles))
