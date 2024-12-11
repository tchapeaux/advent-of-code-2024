import aoc

from functools import cache
from typing import List

data = aoc.getInputForDay(11)
# data = "125 17"

initialStones = [int(x) for x in data.split(" ")]


def transform(stone: int) -> List[int]:
    if stone == 0:
        return [1]
    stoneStr = str(stone)
    if len(stoneStr) % 2 == 0:
        return [
            int(stoneStr[: len(stoneStr) // 2]),
            int(stoneStr[len(stoneStr) // 2 :]),
        ]
    return [stone * 2024]


def step(stones: List[int]) -> List[int]:
    newStones = []
    for s in stones:
        newStones.extend(transform(s))
    return newStones


def countPart1(stones: List[int]) -> int:
    for _ in range(25):
        stones = step(stones)
    return len(stones)


print("Part 1", countPart1(initialStones[:]))


@cache
def getCountofStoneAfterSteps(stone, steps):
    if steps == 0:
        return 1

    # My Codeium copilot auto-filled the next line before I fully knew how to proceed
    # I knew I wanted to do some sort of dynamic programming, but didn't realize I was so close
    return sum(getCountofStoneAfterSteps(s, steps - 1) for s in transform(stone))


print(
    "Part 1",
    sum(getCountofStoneAfterSteps(s, 25) for s in initialStones),
    "(with Part 2 logic)",
)
print("Part 2", sum(getCountofStoneAfterSteps(s, 75) for s in initialStones))

# Another solution would have been to keep a dict of the number of distinct stones values at each step
# (instead of keeping track of them in a big flat list)
# According to the subreddit, this is sufficient to keep computations manageable and does not need a cache
