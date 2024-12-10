import aoc

grid = aoc.getCellsForDay(10)
# grid = aoc.getCellsForDay(10, force_filepath="inputs/day10_example.txt")

heightsCoords = {}

for y in range(len(grid)):
    for x in range(len(grid[y])):
        if grid[y][x] == ".":
            # Only used in some examples
            continue

        height = int(grid[y][x])
        if height not in heightsCoords:
            heightsCoords[height] = set()

        heightsCoords[height].add((x, y))


def isNeighbors(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2

    return abs(x2 - x1) + abs(y2 - y1) == 1


# mapping from coords to the set of reachable 9s
endsReachableFrom = {}

# mapping from coords to the number of paths to a reachable 9s
rankingsFrom = {}

# Initialize countReachableFrom
for coord in heightsCoords[9]:
    endsReachableFrom[coord] = set([coord])
    rankingsFrom[coord] = 1


for height in range(8, -1, -1):
    for coord in heightsCoords[height]:
        for heightPlusOneNode in heightsCoords[height + 1]:
            if not isNeighbors(coord, heightPlusOneNode):
                continue

            validNeighbor = heightPlusOneNode
            if validNeighbor in endsReachableFrom:
                if coord not in endsReachableFrom:
                    endsReachableFrom[coord] = set()
                endsReachableFrom[coord].update(endsReachableFrom[validNeighbor])
            if validNeighbor in rankingsFrom:
                if coord not in rankingsFrom:
                    rankingsFrom[coord] = 0
                rankingsFrom[coord] += rankingsFrom[validNeighbor]


print("Part 1", sum([len(endsReachableFrom[coord]) for coord in heightsCoords[0]]))
print("Part 2", sum([rankingsFrom[coord] for coord in heightsCoords[0]]))
