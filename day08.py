import aoc

import itertools

data = aoc.getCellsForDay(8)
# data = aoc.getCellsForDay(8, force_filepath="inputs/day08_example.txt")

WIDTH = len(data[0])
HEIGHT = len(data)


def isInGrid(x, y) -> bool:
    return 0 <= x < WIDTH and 0 <= y < HEIGHT


nodes = {}

for y in range(len(data)):
    for x in range(len(data[y])):
        if data[y][x] != ".":
            label = data[y][x]
            if label not in nodes:
                nodes[label] = set()
            nodes[label].add((x, y))


def findNextNode(startNode, endNode):
    delta = (
        endNode[0] - startNode[0],
        endNode[1] - startNode[1],
    )
    return (
        endNode[0] + delta[0],
        endNode[1] + delta[1],
    )


antiNodes = {}  # Part 1
antiNodes2 = {}  # Part 2
for label in nodes:
    antiNodes[label] = set()
    antiNodes2[label] = set()

    # Trick: the antennas are also antinodes as soon as there is a pair
    if len(nodes[label]) > 1:
        antiNodes2[label].update(nodes[label])

    for antenna1, antenna2 in itertools.product(nodes[label], nodes[label]):
        if antenna1 == antenna2:
            continue

        startNode = antenna1
        endNode = antenna2

        print("")

        while isInGrid(endNode[0], endNode[1]):
            antiNode = findNextNode(startNode, endNode)

            print(startNode, endNode, antiNode)

            if isInGrid(antiNode[0], antiNode[1]):
                if startNode == antenna1:
                    antiNodes[label].add(antiNode)

                antiNodes2[label].add(antiNode)

            startNode = endNode
            endNode = antiNode


# Count unique locations (remove duplicates)
uniqueLocs = set()
for coord in antiNodes.values():
    uniqueLocs.update(coord)

uniqueLocs2 = set()
for coord in antiNodes2.values():
    uniqueLocs2.update(coord)

print("Part 1", len(uniqueLocs))
print("Part 2", len(uniqueLocs2))


for y in range(HEIGHT):
    for x in range(WIDTH):
        if (x, y) in uniqueLocs2:
            print("X", end="")
        else:
            print(data[y][x], end="")
    print()
