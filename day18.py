import aoc

import heapq
from typing import Tuple, Set, List, Dict

WIDTH = 71
HEIGHT = 71
PART1_SUBSET = 1024

data = aoc.getLinesForDay(18)


# data = aoc.getLinesForDay(18, force_filepath="inputs/day18_example.txt")
# WIDTH = 7
# HEIGHT = 7
# PART1_SUBSET = 12

Coord = Tuple[int, int]

corrupted: Set[Coord] = set()

for line in data[:PART1_SUBSET]:
    (x, y) = map(int, line.split(","))
    corrupted.add((x, y))

NEIGHBORS_4 = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def doADijkstra(start: Coord, end: Coord) -> Tuple[int, Dict[Coord, Coord]]:
    to_visit: List[Tuple[int, Coord]] = []
    bestKnownDistance: Dict[Coord, int] = {}
    bestPathPrev: Dict[Coord, Coord] = {}

    to_visit.append((0, start))
    bestKnownDistance[start] = 0

    while len(to_visit) > 0:
        nextBest = heapq.heappop(to_visit)
        currentDist, currentCoord = nextBest

        if currentDist > bestKnownDistance[currentCoord]:
            continue

        if currentCoord == end:
            return (currentDist, bestPathPrev)

        neighbors = (
            (currentCoord[0] + dx, currentCoord[1] + dy) for dx, dy in NEIGHBORS_4
        )
        for n in neighbors:

            if n in corrupted:
                continue

            if n[0] < 0 or n[0] >= WIDTH or n[1] < 0 or n[1] >= HEIGHT:
                continue

            if n not in bestKnownDistance:

                bestKnownDistance[n] = currentDist + 1
                bestPathPrev[n] = currentCoord
                heapq.heappush(to_visit, (currentDist + 1, n))

    # End not found, no path exist
    return (-1, {})


# Display grid
"""
for y in range(HEIGHT):
    for x in range(WIDTH):
        print("#" if (x, y) in corrupted else ".", end="")
    print("")
"""


minPathLength, _ = doADijkstra((0, 0), (WIDTH - 1, HEIGHT - 1))
print("Part 1", minPathLength)

# Part 2
# Add byte one by one until there is no path to find

for line in data[PART1_SUBSET:]:
    (x, y) = map(int, line.split(","))
    corrupted.add((x, y))
    minPathLength, _ = doADijkstra((0, 0), (WIDTH - 1, HEIGHT - 1))
    if minPathLength == -1:
        print("Part 2", f"{x},{y}")
        break
