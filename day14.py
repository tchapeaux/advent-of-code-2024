import aoc

import math
from typing import NamedTuple, Tuple, List, Dict, Mapping

data = aoc.getLinesForDay(14)
# data = aoc.getLinesForDay(14, force_filepath="inputs/day14_example.txt")

# Constants and typing

GRID_WIDTH = 101
GRID_HEIGHT = 103

# Example constants
# GRID_WIDTH = 11
# GRID_HEIGHT = 7

Coord = Tuple[int, int]


class Robot(NamedTuple):
    initialPos: Coord
    speed: Coord


# Parse input

robots: List[Robot] = []

for line in data:
    pos, speed = line.split(" ")
    px, py = pos[2:].split(",")
    sx, sy = speed[2:].split(",")
    robot = Robot((int(px), int(py)), (int(sx), int(sy)))
    robots.append(robot)

# Find position after 100s


def posAfter(robot: Robot, t: int) -> Coord:
    px, py = robot.initialPos
    sx, sy = robot.speed
    return ((px + sx * t) % GRID_WIDTH, (py + sy * t) % GRID_HEIGHT)


robotsPosAfter100s: List[Coord] = []

for robot in robots:
    robotsPosAfter100s.append(posAfter(robot, 100))


# Count robots in each quadrant

# Top-Left
quad1Count = len(
    [
        c
        for c in robotsPosAfter100s
        if c[0] < math.floor(GRID_WIDTH / 2) and c[1] < math.floor(GRID_HEIGHT / 2)
    ]
)

# Top-Right
quad2Count = len(
    [
        c
        for c in robotsPosAfter100s
        if c[0] >= math.ceil(GRID_WIDTH / 2) and c[1] < math.floor(GRID_HEIGHT / 2)
    ]
)

# Bottom left
quad3Count = len(
    [
        c
        for c in robotsPosAfter100s
        if c[0] < math.floor(GRID_WIDTH / 2) and c[1] >= math.ceil(GRID_HEIGHT / 2)
    ]
)

# Bottom right
quad4Count = len(
    [
        c
        for c in robotsPosAfter100s
        if c[0] >= math.ceil(GRID_WIDTH / 2) and c[1] >= math.ceil(GRID_HEIGHT / 2)
    ]
)

print("Part 1", quad1Count * quad2Count * quad3Count * quad4Count)
# 182008200 too low

# Part 2
# Let's find if there is a loop

savedStates: Mapping[int, Dict[Coord, int]] = dict()

foundLoop = None
# hardcode my value to avoid recalculating at each step
foundLoop = (0, 10403)

for t in range(20000):
    if foundLoop:
        break

    robotsAfterT = [posAfter(robot, t) for robot in robots]
    savedStates[t] = dict()
    for coord in robotsAfterT:
        if coord not in savedStates[t]:
            savedStates[t][coord] = 1
        savedStates[t][coord] += 1

    # print("state", t, savedStates[t])

    # check if this state has been encountered before
    currentState = savedStates[t]
    for t2 in range(t):
        pastState = savedStates[t2]
        if currentState == pastState:
            print("FOUND LOOP", t2, t - t2)
            foundLoop = (t2, t - t2)
            break

assert foundLoop

# We found a loop of more than 10k steps
# Let's suppose that the easter egg is when robots are in formation, so close to each other
# So let's find T with the minimum number of standalone robots (robots with no neighbors)

minStandaloneRobots = len(robots)
tMin = -1

for t in range(foundLoop[0], foundLoop[0] + foundLoop[1] + 1):
    robotsAfterT = [posAfter(robot, t) for robot in robots]

    countStandalone = 0
    for coord in robotsAfterT:
        isStandalone = all(
            neigh not in robotsAfterT
            for neigh in (
                (coord[0] - 1, coord[1]),
                (coord[0] + 1, coord[1]),
                (coord[0], coord[1] - 1),
                (coord[0], coord[1] + 1),
            )
        )
        countStandalone += 1 if isStandalone else 0

    if countStandalone < minStandaloneRobots:
        minStandaloneRobots = countStandalone
        tMin = t

print("Part 2", tMin, minStandaloneRobots)

# Just for fun, let's display the result


def displayState(state: Mapping[Coord, int]):
    print("==")
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x, y) in state:
                print("#", end="")
            else:
                print(".", end="")
        print()


displayState({posAfter(robot, tMin): 1 for robot in robots})
