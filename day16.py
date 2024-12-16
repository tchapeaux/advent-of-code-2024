import aoc

import sys
from typing import Tuple, Set, NamedTuple, Dict, List

grid = aoc.getCellsForDay(16)
# grid = aoc.getCellsForDay(16, force_filepath="inputs/day16_example.txt")
# grid = aoc.getCellsForDay(16, force_filepath="inputs/day16_example2.txt")
# grid = aoc.getCellsForDay(16, force_filepath="inputs/day16_other_zigzag.txt")
# grid = aoc.getCellsForDay(16, force_filepath="inputs/day16_other_open_maze.txt")

## Let's go
sys.setrecursionlimit(15000)

Coord = Tuple[int, int]


Direction = Coord


DIRECTIONS = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}


class State(NamedTuple):
    coord: Coord
    direction: Direction
    score: int
    pathBefore: List[Coord]


walls: Set[Coord] = set()

for y, line in enumerate(grid):
    for x, c in enumerate(line):
        if c == "S":
            startCoord = (x, y)
        elif c == "E":
            endCoord = (x, y)
        elif c == "#":
            walls.add((x, y))

initialDirection: Direction = DIRECTIONS["E"]


def turnRight(direction: Direction) -> Direction:
    if direction == DIRECTIONS["N"]:
        return DIRECTIONS["E"]
    elif direction == DIRECTIONS["E"]:
        return DIRECTIONS["S"]
    elif direction == DIRECTIONS["S"]:
        return DIRECTIONS["W"]
    elif direction == DIRECTIONS["W"]:
        return DIRECTIONS["N"]

    raise Exception(f"Unknown direction {direction}")


def turnLeft(direction: Direction) -> Direction:
    if direction == DIRECTIONS["N"]:
        return DIRECTIONS["W"]
    elif direction == DIRECTIONS["W"]:
        return DIRECTIONS["S"]
    elif direction == DIRECTIONS["S"]:
        return DIRECTIONS["E"]
    elif direction == DIRECTIONS["E"]:
        return DIRECTIONS["N"]

    raise Exception(f"Unknown direction {direction}")


bestKnownScore: Dict[Coord, int] = dict()


def getMinPathFor(walls: Set[Coord], end: Coord, state: State) -> int:
    # print(state)
    if state.coord in bestKnownScore and state.score >= bestKnownScore[state.coord]:
        return -1
    bestKnownScore[state.coord] = state.score

    nextCoord: Coord = (
        state.coord[0] + state.direction[0],
        state.coord[1] + state.direction[1],
    )

    if nextCoord == end:
        finalScore = state.score + 1
        if end not in bestKnownScore or bestKnownScore[end] > finalScore:
            bestKnownScore[end] = finalScore

        print("Found path")
        print(getPathRepr(state))
        print("score", finalScore)
        print("==")

        return 1

    goStraightScore: int = -1
    if nextCoord not in walls:
        goStraightScore = getMinPathFor(
            walls,
            end,
            State(
                nextCoord,
                state.direction,
                1 + state.score,
                state.pathBefore + [state.coord],
            ),
        )

    turnRightScore: int = -1
    rightDir: Direction = turnRight(state.direction)
    rightCoord: Coord = (
        state.coord[0] + rightDir[0],
        state.coord[1] + rightDir[1],
    )
    if rightCoord not in walls:
        turnRightScore = getMinPathFor(
            walls,
            end,
            State(
                rightCoord,
                rightDir,
                1001 + state.score,
                state.pathBefore + [state.coord],
            ),
        )

    turnLeftScore: int = -1
    leftDir: Direction = turnLeft(state.direction)
    leftCoord: Coord = (state.coord[0] + leftDir[0], state.coord[1] + leftDir[1])
    if leftCoord not in walls:
        turnLeftScore = getMinPathFor(
            walls,
            end,
            State(
                leftCoord, leftDir, 1001 + state.score, state.pathBefore + [state.coord]
            ),
        )

    if goStraightScore == turnRightScore == turnLeftScore == -1:
        return -1

    minScore = min(
        s for s in (goStraightScore, turnRightScore, turnLeftScore) if s > -1
    )

    if minScore == goStraightScore:
        return 1 + minScore
    if minScore == turnRightScore or minScore == turnLeftScore:
        return 1001 + minScore

    raise Exception(
        "Unexpected state", goStraightScore, turnRightScore, turnLeftScore, minScore
    )


def getPathRepr(state: State) -> str:
    pathStr = ""
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in walls:
                pathStr += "#"
            elif (x, y) == state.coord:
                pathStr += "@"
            elif (x, y) in state.pathBefore:
                pathStr += "O"
            else:
                pathStr += "."
        pathStr += "\n"

    return pathStr


# 73408 too high
print(
    "Part 1", getMinPathFor(walls, endCoord, State(startCoord, initialDirection, 0, []))
)
print("best known", bestKnownScore[endCoord])
