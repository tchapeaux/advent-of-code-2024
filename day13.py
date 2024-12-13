import aoc
from typing import Tuple, NamedTuple, List
from functools import lru_cache

data = aoc.getInputForDay(13)
# data = aoc.getInputForDay(13, force_filepath="inputs/day13_example.txt")

# Type definitions

A_COST = 3
B_COST = 1

Coord = Tuple[int, int]


class Game(NamedTuple):
    a: Coord
    b: Coord
    prize: Coord


def strToCoord(s: str) -> Coord:
    a, b = s.split(", ")
    a = int(a[2:])
    b = int(b[2:])
    return (a, b)


# Parse input

games: List[Game] = []

for game in data.strip().split("\n\n"):
    a, b, prize = game.strip().split("\n")
    a = strToCoord(a.split(": ")[1])
    b = strToCoord(b.split(": ")[1])
    prize = strToCoord(prize.split(": ")[1])

    games.append(Game(a, b, prize))


@lru_cache(maxsize=10000)
def findMinCostFor(game: Game, currentPos: Coord = (0, 0)) -> int:
    # print(currentPos, game.prize)

    if currentPos == game.prize:
        return 0

    if currentPos[0] > game.prize[0] or currentPos[1] > game.prize[1]:
        return -1

    # Check A path
    newPosA = (currentPos[0] + game.a[0], currentPos[1] + game.a[1])
    costsA = findMinCostFor(game, newPosA)

    # Check B path
    newPosB = (currentPos[0] + game.b[0], currentPos[1] + game.b[1])
    costsB = findMinCostFor(game, newPosB)

    if costsA == -1 and costsB == -1:
        # Impossible to reach the prize
        return -1

    if costsA == -1:
        return B_COST + costsB

    if costsB == -1:
        return A_COST + costsA

    return min(A_COST + costsA, B_COST + costsB)


accPart1 = 0

for gameIdx, game in enumerate(games):
    moves = findMinCostFor(game)
    if moves > -1:
        accPart1 += moves

print("Part 1", accPart1)

# For Part 2, we might prefer to do some maths
# we need to find A and B such that
# XP = A * XA + B * XB
# YP = A * YA + B * YB
# with A > 0 and B > 0
# While minimizing A_COST * A + B_COST * B

# ...One ChatGpt chat later...
# https://chatgpt.com/share/675c4a19-9e00-800a-afed-1c20c0713836
# (I'm a prompt engineer)


def findMinCostWithMaths(game: Game) -> int:
    """This function was entirely written by AI"""
    # Compute the denominator for 'a'
    denominator_a = game.a[0] * game.b[1] - game.a[1] * game.b[0]

    # Compute the numerator for 'a'
    numerator_a = game.prize[0] * game.b[1] - game.prize[1] * game.b[0]

    # Compute 'a'
    a = numerator_a / denominator_a

    # Compute 'b'
    b = (game.prize[0] - a * game.a[0]) / game.b[0]

    if a.is_integer() and b.is_integer():
        return A_COST * int(a) + B_COST * int(b)

    return -1


# Check the part 2 function returns the same value as part 1

for g in games:
    test = findMinCostWithMaths(g)
    expected = findMinCostFor(g)
    assert test == expected

accPart2 = 0
CALIBRATION = 10000000000000

for game in games:
    changedGame = Game(
        game.a, game.b, (game.prize[0] + CALIBRATION, game.prize[1] + CALIBRATION)
    )

    moves = findMinCostWithMaths(changedGame)
    if moves > -1:
        accPart2 += moves

print("Part 2", accPart2)
