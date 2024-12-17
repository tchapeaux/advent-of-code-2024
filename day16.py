import aoc
import heapq

from typing import Tuple, Set, NamedTuple, Dict, List

grid = aoc.getCellsForDay(16)
# grid = aoc.getCellsForDay(16, force_filepath="inputs/day16_example.txt")
# grid = aoc.getCellsForDay(16, force_filepath="inputs/day16_example2.txt")
# grid = aoc.getCellsForDay(16, force_filepath="inputs/day16_other_zigzag.txt")
# grid = aoc.getCellsForDay(16, force_filepath="inputs/day16_other_open_maze.txt")


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


def getMinPathFor(
    walls: Set[Coord], end: Coord, startState: State
) -> Tuple[int, Dict[State, Set[State]]]:
    # Do a Dijkstra
    # Return both the minimal path length and the dictionaries of previous nodes to reconstruct
    # multiple best paths

    minDistanceKnown: Dict[State, int] = dict()
    bestPathComesFrom: Dict[State, Set[State]] = dict()

    to_visit: List[Tuple[int, State]] = []
    heapq.heappush(to_visit, (0, startState))

    while len(to_visit) > 0:
        nextBest = heapq.heappop(to_visit)
        currentDist, currentState = nextBest

        if currentState.coord == end:
            return (currentDist, bestPathComesFrom)

        # Explore other states
        candidatesNextAndDistance: List[Tuple[State, int]] = []

        # go straight
        straightCoord = (
            currentState.coord[0] + currentState.direction[0],
            currentState.coord[1] + currentState.direction[1],
        )
        if straightCoord not in walls:
            candidatesNextAndDistance.append(
                (
                    State(
                        straightCoord,
                        currentState.direction,
                    ),
                    currentDist + 1,
                )
            )

        # turn right if cell to the right is not a wall
        rightDirection: Direction = turnRight(currentState.direction)
        rightCoord = (
            currentState.coord[0] + rightDirection[0],
            currentState.coord[1] + rightDirection[1],
        )
        if rightCoord not in walls:
            candidatesNextAndDistance.append(
                (
                    State(
                        currentState.coord,
                        rightDirection,
                    ),
                    currentDist + 1000,
                )
            )

        # turn left if cell to the left is not a wall
        leftDirection: Direction = turnLeft(currentState.direction)
        leftCoord = (
            currentState.coord[0] + leftDirection[0],
            currentState.coord[1] + leftDirection[1],
        )
        if leftCoord not in walls:
            candidatesNextAndDistance.append(
                (
                    State(
                        currentState.coord,
                        leftDirection,
                    ),
                    currentDist + 1000,
                )
            )

        for nextState, nextDist in candidatesNextAndDistance:
            if (
                nextState not in minDistanceKnown
                or nextDist < minDistanceKnown[nextState]
            ):
                minDistanceKnown[nextState] = nextDist
                bestPathComesFrom[nextState] = set([currentState])
                heapq.heappush(to_visit, (nextDist, nextState))

            elif nextDist == minDistanceKnown[nextState]:
                bestPathComesFrom[nextState].add(currentState)

    raise Exception("No path to end found")


bestLength, bestPreviousNodes = getMinPathFor(
    walls, endCoord, State(startCoord, initialDirection)
)

print("Part 1", bestLength)

# Reconstruct all best paths with a floodfill from the end
visited: Set[State] = set()
to_visit: Set[State] = set()

to_visit.update([state for state in bestPreviousNodes if state.coord == endCoord])

while len(to_visit) > 0:
    state = to_visit.pop()
    visited.add(state)

    assert state in bestPreviousNodes
    for prevState in bestPreviousNodes[state]:
        if prevState not in visited:
            to_visit.add(prevState)

print("Part 2", len(set([s.coord for s in visited])))
