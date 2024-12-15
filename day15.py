import aoc

from typing import List, Tuple, Set, Literal, Dict, Mapping

data = aoc.getInputForDay(15)
# data = aoc.getInputForDay(15, force_filepath="inputs/day15_small_example.txt")
# data = aoc.getInputForDay(15, force_filepath="inputs/day15_small_example_part2.txt")
# data = aoc.getInputForDay(15, force_filepath="inputs/day15_example.txt")

Coord = Tuple[int, int]
Move = Literal["^", "v", "<", ">"]
Tile = Literal[".", "#", "O", "@"]

BoxLinks = Mapping[Coord, Coord]


Walls = Set[Coord]
Boxes = Set[Coord]
Robot = Coord

State = Tuple[Robot, Boxes, Walls, BoxLinks]

gridRaw, movesRaw = data.split("\n\n")
initialRobot: Robot = (-1, -1)
initialBoxes: Boxes = set()
initialWalls: Walls = set()

for y, line in enumerate(gridRaw.split("\n")):
    for x, c in enumerate(line):
        if c == "@":
            initialRobot = (x, y)
        if c == "O":
            initialBoxes.add((x, y))
        if c == "#":
            initialWalls.add((x, y))

assert initialRobot != (-1, -1)
assert len(initialBoxes) > 0
assert len(initialWalls) > 0

moves: List[Move] = [c for c in movesRaw if c in ["^", "v", "<", ">"]]

MOVES: Dict[Move, Coord] = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


def doMove(state: State, move: Move) -> State:
    robot, boxes, walls, _ = state

    newRobot = (
        robot[0] + MOVES[move][0],
        robot[1] + MOVES[move][1],
    )

    if newRobot in walls:
        return state

    if newRobot not in boxes:
        # robot is on a free space, return early
        return (newRobot, boxes, walls, _)

    assert newRobot in boxes
    lineOfBoxes: List[Coord] = []
    newBoxes = boxes.copy()
    currentBox = newRobot

    while currentBox in newBoxes:
        lineOfBoxes.append(currentBox)
        nextBox = (
            currentBox[0] + MOVES[move][0],
            currentBox[1] + MOVES[move][1],
        )

        if nextBox in walls:
            return state

        if nextBox not in newBoxes:
            # Remove first box and place it at the end
            newBoxes.remove(newRobot)
            newBoxes.add(nextBox)
            break

        currentBox = nextBox

    return (newRobot, newBoxes, walls, _)


def getStateRepr(state: State) -> str:
    stateStr = ""

    minX = min([w[0] for w in state[2]])
    maxX = max([w[0] for w in state[2]])
    minY = min([w[1] for w in state[2]])
    maxY = max([w[1] for w in state[2]])

    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            if (x, y) in state[2]:
                stateStr += "#"
            elif (x, y) in state[1]:
                stateStr += "O"
            elif (x, y) == state[0]:
                stateStr += "@"
            else:
                stateStr += "."

        stateStr += "\n"

    return stateStr


def countCoordinates(state: State) -> int:
    _, boxes, _, joinedBoxes = state

    # If there are joined boxes, only consider the leftmost one
    leftMostBoxes = set(
        [b for b in boxes if b not in joinedBoxes or b[0] < joinedBoxes[b][0]]
    )

    return sum(100 * b[1] + b[0] for b in leftMostBoxes)


currentState: State = (initialRobot, initialBoxes, initialWalls, dict())

for moveIdx, move in enumerate(moves):
    currentState = doMove(currentState, move)
    # print("Move", moveIdx + 1, move)
    # print(getStateRepr(currentState))

print("Part 1", countCoordinates(currentState))

# Construct state for part 2

initialRobot2 = (initialRobot[0] * 2, initialRobot[1])

initialBoxes2 = set()
joinedBoxes: Mapping[Coord, Coord] = dict()
for box in initialBoxes:
    newbox1 = (box[0] * 2, box[1])
    newbox2 = (box[0] * 2 + 1, box[1])
    initialBoxes2.add(newbox1)
    initialBoxes2.add(newbox2)
    joinedBoxes[newbox1] = newbox2
    joinedBoxes[newbox2] = newbox1

initialWalls2 = set()
for wall in initialWalls:
    newWall1 = (wall[0] * 2, wall[1])
    newWall2 = (wall[0] * 2 + 1, wall[1])
    initialWalls2.add(newWall1)
    initialWalls2.add(newWall2)


def doMove2(state: State, move: Move) -> State:
    robot, boxes, walls, joinedBoxes = state

    newRobot = (
        robot[0] + MOVES[move][0],
        robot[1] + MOVES[move][1],
    )

    if newRobot in walls:
        return state

    if newRobot not in boxes:
        # robot is on a free space, move it early
        return (newRobot, boxes, walls, joinedBoxes)

    # robot is in a box
    # Find all boxes that should be moved as a result
    # If any is blocked by a wall, cancel the move
    newBoxes = boxes.copy()
    newJoinedBoxes: BoxLinks = dict(joinedBoxes).copy()
    visited: Set[Coord] = set()
    to_visit: Set[Coord] = set([newRobot])

    while len(to_visit) > 0:
        coord = to_visit.pop()

        if coord in visited:
            continue

        if coord in walls:
            return state

        if coord in newBoxes:
            nextCoord = (
                coord[0] + MOVES[move][0],
                coord[1] + MOVES[move][1],
            )
            to_visit.add(nextCoord)
            to_visit.add(joinedBoxes[coord])

            visited.add(coord)

    # Remove all visited coords from boxes then replace them by
    # their moved position
    # Also update the joinedBoxes dict
    # This must be done in two steps to avoid overriding values

    joinedBoxesToAdd = set()

    for coord in visited:
        assert coord in newBoxes
        newBoxes.remove(coord)

        if coord in newJoinedBoxes:
            joinedBoxesToAdd.add(
                (
                    (coord[0] + MOVES[move][0], coord[1] + MOVES[move][1]),
                    (
                        newJoinedBoxes[coord][0] + MOVES[move][0],
                        newJoinedBoxes[coord][1] + MOVES[move][1],
                    ),
                )
            )
            del newJoinedBoxes[coord]

    for coord in visited:
        newBoxes.add(
            (
                coord[0] + MOVES[move][0],
                coord[1] + MOVES[move][1],
            )
        )

    for coord1, coord2 in joinedBoxesToAdd:
        newJoinedBoxes[coord1] = coord2

    return (newRobot, newBoxes, walls, newJoinedBoxes)


currentState2 = (initialRobot2, initialBoxes2, initialWalls2, joinedBoxes)


for moveIdx, move in enumerate(moves):
    # print("Move", moveIdx + 1, move)
    currentState2 = doMove2(currentState2, move)
    # print(getStateRepr(currentState2))

print("Part 2", countCoordinates(currentState2))

## 2258982 too high
## 2905268 too high
