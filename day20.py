import aoc

from typing import Tuple, Set, List, Dict
import heapq

grid = aoc.getCellsForDay(20)
# grid = aoc.getCellsForDay(20, force_filepath="inputs/day20_example.txt")

Coord = Tuple[int, int]

walls: Set[Coord] = set()

for y, line in enumerate(grid):
    for x, char in enumerate(line):
        if char == "#":
            walls.add((x, y))
        elif char == "S":
            start: Coord = (x, y)
        elif char == "E":
            end: Coord = (x, y)

assert start
assert end

# Find the best path from start to end while avoiding walls
# According to the instructions, we can assume there is only one path
# So we do a quick Dikjstra

to_visit: List[Tuple[int, Coord]] = []
bestDistance: Dict[Coord, int] = dict()
bestPrevious: Dict[Coord, Coord] = dict()

to_visit.append((0, start))
while len(to_visit) > 0:
    currentBestDist, currentBestCoord = heapq.heappop(to_visit)

    if currentBestCoord == end:
        break

    for n in (
        (currentBestCoord[0] + d[0], currentBestCoord[1] + d[1])
        for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]
    ):
        if n not in walls and n not in bestDistance:
            bestDistance[n] = currentBestDist + 1
            bestPrevious[n] = currentBestCoord

            heapq.heappush(to_visit, (currentBestDist + 1, n))

# Reconstruct path from start to end
path: List[Coord] = [end]
while start not in path:
    last = path[-1]
    next = bestPrevious[last]
    assert next
    path.append(next)

path = list(reversed(path))

# print("Best path length", len(path) - 1)

# Find cheat patterns
# so (i, j) such that dist(path[i], path[j]) == 1 and j - i > TRESHOLD
# in Part 2, this becomes dist(path[i], path[j]) <= cheatTime

Cheat = Tuple[Coord, Coord]


def findCheats(timeSavedTreshold: int, cheatTime: int) -> Dict[int, Set[Cheat]]:
    cheats: Dict[int, Set[Cheat]] = dict()

    for i in range(len(path)):
        for j in range(i + timeSavedTreshold, len(path)):

            start = path[i]
            end = path[j]

            manhattanDist = abs(end[0] - start[0]) + abs(end[1] - start[1])

            if manhattanDist <= cheatTime:
                timeSaved = j - i - manhattanDist
                if timeSaved < timeSavedTreshold:
                    continue

                if timeSaved not in cheats:
                    cheats[timeSaved] = set()
                cheats[timeSaved].add((start, end))

    return cheats


part1Cheats = findCheats(100, 2)
print("Part 1", sum(len(part1Cheats[t]) for t in part1Cheats.keys()))

part2Cheats = findCheats(100, 20)
print("Part 2", sum(len(part2Cheats[t]) for t in part2Cheats.keys()))
