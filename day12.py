import aoc

from typing import Mapping, Tuple, Set, List

grid = aoc.getCellsForDay(12)
# grid = aoc.getCellsForDay(12, force_filepath="inputs/day12_example_1.txt")
# grid = aoc.getCellsForDay(12, force_filepath="inputs/day12_example_2.txt")
# grid = aoc.getCellsForDay(12, force_filepath="inputs/day12_example_3.txt")


RegionId = int
Coord = Tuple[int, int]

coordToRegion: Mapping[Coord, RegionId] = dict()
regionToCoord: Mapping[RegionId, Set[Coord]] = dict()

# The idea will be
# We explore the grid point by point
# When we encounter an unknown point, we assign it a region then deep-explore its neighbors
# If we encounter a known point, we skip it
# This should get us all regions

for y in range(len(grid)):
    for x in range(len(grid[y])):
        coord = (x, y)
        if coord not in coordToRegion:
            # New region!
            regionId: RegionId = len(regionToCoord)
            regionToCoord[regionId] = set()
            regionPlant = grid[y][x]

            # DFS exploration
            to_visit: Set[Coord] = set([coord])
            while len(to_visit) > 0:
                coord2 = to_visit.pop()
                if coord2 not in coordToRegion:
                    coordToRegion[coord2] = regionId
                    regionToCoord[regionId].add(coord2)

                    neighbors = aoc.get4Neighbors(grid, coord2[0], coord2[1])

                    for xN, yN, plant in neighbors:
                        if (
                            plant == regionPlant
                            and (xN, yN) not in regionToCoord[regionId]
                        ):
                            to_visit.add((xN, yN))


def area(regionId):
    return len(regionToCoord[regionId])


def perimeter(regionId):
    acc = 0
    for coord in regionToCoord[regionId]:
        neighbors = list(aoc.get4Neighbors(grid, coord[0], coord[1]))
        for xN, yN, plant in neighbors:
            if plant != grid[coord[1]][coord[0]]:
                acc += 1
        acc += 4 - len(neighbors)
    return acc


print("Part 1", sum([area(r) * perimeter(r) for r in regionToCoord.keys()]))
# 33633 too low

directions = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}


Edge = Tuple[Coord, str]


def reversedEdge(edge) -> Edge:
    # Return the opposite representation of the same edge
    # eg. 1,1,N is the same as 1,0,S
    if edge[1] == "N":
        return ((edge[0][0], edge[0][1] - 1), "S")
    if edge[1] == "S":
        return ((edge[0][0], edge[0][1] + 1), "N")
    if edge[1] == "W":
        return ((edge[0][0] - 1, edge[0][1]), "E")
    if edge[1] == "E":
        return ((edge[0][0] + 1, edge[0][1]), "W")
    return edge


def findNextEdge(edges, currentEdge):
    candidates: Set[Edge] = set()

    # We follow the perimeter in clockwise order
    # The following edge is either the continuation, or a change of direction in one of the perpendicular directions
    # We use the canonical representation

    if currentEdge[1] == "N":
        # We follow all N edges to the right
        candidates.add(((currentEdge[0][0] + 1, currentEdge[0][1]), "N"))
        candidates.add(((currentEdge[0][0], currentEdge[0][1]), "E"))
        candidates.add(((currentEdge[0][0], currentEdge[0][1] - 1), "E"))
    if currentEdge[1] == "E":
        # We follow all E edges to the bottom
        candidates.add(((currentEdge[0][0], currentEdge[0][1] + 1), "E"))
        candidates.add(((currentEdge[0][0], currentEdge[0][1]), "S"))
        candidates.add(((currentEdge[0][0] + 1, currentEdge[0][1]), "S"))
    if currentEdge[1] == "S":
        # We follow all S edges to the left
        candidates.add(((currentEdge[0][0] - 1, currentEdge[0][1]), "S"))
        candidates.add(((currentEdge[0][0], currentEdge[0][1]), "W"))
        candidates.add(((currentEdge[0][0], currentEdge[0][1] + 1), "W"))
    if currentEdge[1] == "W":
        # We follow all W edges to the top
        candidates.add(((currentEdge[0][0], currentEdge[0][1] - 1), "W"))
        candidates.add(((currentEdge[0][0], currentEdge[0][1]), "N"))
        candidates.add(((currentEdge[0][0] - 1, currentEdge[0][1]), "N"))

    for c in candidates:
        if c in edges:
            return c
        if reversedEdge(c) in edges:
            return reversedEdge(c)

    raise Exception(
        f"edge with no continuation\n\ncurrent: {currentEdge}\n\ncandidates: {candidates}\n\nedges: {edges}"
    )


def countSidesOnSegment(
    edges: Set[Edge], linedCoords: List[Coord], direction: str
) -> int:
    # Check that linedCoords is actually a segment
    assert (
        len(set([c[0] for c in linedCoords])) == 1
        or len(set([c[1] for c in linedCoords])) == 1
    )
    linedCoords = sorted(linedCoords)

    # Follow the line and count continuous edges in direction
    acc = 0
    isOnSide = False
    for c in linedCoords:
        if (c, direction) in edges:
            if not isOnSide:
                acc += 1
            isOnSide = True
        else:
            isOnSide = False

    return acc


def countSides(regionId):
    # Gather all edges
    edges = set()

    for coord in regionToCoord[regionId]:
        for dir in directions.keys():
            neighbor = (coord[0] + directions[dir][0], coord[1] + directions[dir][1])
            if neighbor not in regionToCoord[regionId]:
                edges.add((coord, dir))

    # Find region boundaries
    minX = min([e[0][0] for e in edges])
    maxX = max([e[0][0] for e in edges])
    minY = min([e[0][1] for e in edges])
    maxY = max([e[0][1] for e in edges])

    # Explore the region row by row then col by col, looking for edges on one side or the other

    sidesCount = 0
    for x in range(minX, maxX + 1):
        col = [(x, y) for y in range(minY, maxY + 1)]
        sidesCount += countSidesOnSegment(edges, col, "E")
        sidesCount += countSidesOnSegment(edges, col, "W")
    for y in range(minY, maxY + 1):
        row = [(x, y) for x in range(minX, maxX + 1)]
        sidesCount += countSidesOnSegment(edges, row, "N")
        sidesCount += countSidesOnSegment(edges, row, "S")

    return sidesCount


print("Part 2", sum([area(r) * countSides(r) for r in regionToCoord.keys()]))
