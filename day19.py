import aoc
from typing import List, Dict, Sequence
from functools import cache


data = aoc.getInputForDay(19)


Pattern = str
Towel = str

TowelCombination = List[Towel]

# Parse data
dataTop, dataBottom = data.split("\n\n")
towels: Sequence[Towel] = dataTop.strip().split(", ")
patterns: Sequence[Pattern] = dataBottom.strip().split("\n")

possiblePatternsCount = 0


@cache
def isPossible(pattern: Pattern) -> bool:
    if len(pattern) == 0:
        return True

    for t in towels:
        if pattern.startswith(t):
            if isPossible(pattern[len(t) :]):
                return True

    return False


for p in patterns:
    possible = isPossible(p)
    if possible:
        possiblePatternsCount += 1

print("Part 1", possiblePatternsCount)

# Part 2


@cache
def countPossible(pattern: Pattern) -> int:
    if len(pattern) == 0:
        return 1

    thisCount = 0
    for t in towels:
        if pattern.startswith(t):
            thisCount += countPossible(pattern[len(t) :])

    return thisCount


print("Part 2", sum(countPossible(p) for p in patterns))
