import aoc
from typing import List, Tuple

data = aoc.getInputForDay(9)

# Example data
# data = "12345"
# data = "2333133121414131402"

instructions = [int(i) for i in data.strip()]

DiskZone = Tuple[int, int, int]  # index, size, content
disk: List[DiskZone] = []

# Parse input into disk
currentIndex = 0
currentId = 0
isFileToggle = True
for i in instructions:
    if i > 0:
        newZone: DiskZone = (currentIndex, i, currentId if isFileToggle else -1)
        disk.append(newZone)
        currentIndex += i

        if isFileToggle:
            currentId += 1

    isFileToggle = not isFileToggle


def hasEmptySpace(disk: List[DiskZone]) -> bool:
    return any([zone[2] == -1 for zone in disk])


def cleanupDiskRepresentation(disk: List[DiskZone]) -> None:
    while disk[-1][2] == -1:
        disk.pop()

    disk = [z for z in disk if z[1] != 0]


def isDiskValid(disk: List[DiskZone]) -> bool:
    """Check integrity of disk data and zone coherence"""
    currentIndex = 0
    for zoneIdx, zone in enumerate(disk):
        if zone[0] != currentIndex:
            print("!!", currentIndex, disk[: zoneIdx + 1])
            return False
        currentIndex += zone[1]

    return True


def defragPart1(disk):
    # Fill empty spaces (-1) by blocks from the end
    while hasEmptySpace(disk):
        # Find first empty space
        emptyIndices = [i for i in range(len(disk)) if disk[i][2] == -1]
        firstEmptyIndex = emptyIndices[0]
        firstEmptyBlock = disk[firstEmptyIndex]

        # Find last block
        lastBlock = disk[-1]
        assert lastBlock[2] != -1

        if lastBlock[1] == firstEmptyBlock[1]:
            # Place the last block exactly in the empty space
            disk = (
                disk[:firstEmptyIndex]
                + [(firstEmptyBlock[0], firstEmptyBlock[1], lastBlock[2])]
                + disk[firstEmptyIndex + 1 : -1]
            )
        elif lastBlock[1] > firstEmptyBlock[1]:
            # Reduce the last block and keep the remainder at the end
            disk = (
                disk[:firstEmptyIndex]
                + [(firstEmptyBlock[0], firstEmptyBlock[1], lastBlock[2])]
                + disk[firstEmptyIndex + 1 : -1]
                + [(lastBlock[0], lastBlock[1] - firstEmptyBlock[1], lastBlock[2])]
            )
        elif lastBlock[1] < firstEmptyBlock[1]:
            # Place the last block in the empty space then reduce the empty space
            disk = (
                disk[:firstEmptyIndex]
                + [(firstEmptyBlock[0], lastBlock[1], lastBlock[2])]
                + [
                    (
                        firstEmptyBlock[0] + lastBlock[1],
                        firstEmptyBlock[1] - lastBlock[1],
                        -1,
                    )
                ]
                + disk[firstEmptyIndex + 1 : -1]
            )
        cleanupDiskRepresentation(disk)

    return disk


def defragPart2(disk):

    biggestFile = max([z[2] for z in disk])

    for currentFile in reversed(range(biggestFile + 1)):
        assert isDiskValid(disk)

        fileZoneIdx = [i for i in range((len(disk))) if disk[i][2] == currentFile][0]
        fileZone = disk[fileZoneIdx]
        fileZoneSize = fileZone[1]

        # Find first empty zone with sufficient size
        for emptyZoneIdx, e in enumerate(disk):
            if emptyZoneIdx < fileZoneIdx and e[2] == -1 and e[1] >= fileZoneSize:
                # Place the file zone here
                disk = (
                    disk[:emptyZoneIdx]
                    + [(e[0], fileZoneSize, currentFile)]
                    + [(e[0] + fileZoneSize, e[1] - fileZoneSize, -1)]
                    + disk[emptyZoneIdx + 1 : fileZoneIdx]
                    + [(fileZone[0], fileZone[1], -1)]
                    + disk[fileZoneIdx + 1 :]
                )

                cleanupDiskRepresentation(disk)
                break

    return disk


def getCheckum(disk: List[DiskZone]) -> int:
    acc = 0
    currentIndex = 0
    for zone in disk:
        if zone[2] == -1:
            currentIndex += zone[1]
        else:
            for i in range(zone[1]):
                acc += currentIndex * zone[2]
                currentIndex += 1

    return acc


fragDisk1 = defragPart1(disk[:])
checksumPart1 = getCheckum(fragDisk1)
print("Part 1", checksumPart1)

fragDisk2 = defragPart2(disk[:])
checksumPart2 = getCheckum(fragDisk2)
print("Part 2", checksumPart2)
