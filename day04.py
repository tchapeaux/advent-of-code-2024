import aoc

grid = aoc.getCellsForDay(4)
# grid = aoc.getCellsForDay(4, force_filepath="inputs/day04_example.txt")


countPart1 = 0

for y in range(len(grid)):
    for x in range(len(grid[y])):
        if grid[y][x] == "X":
            for dir in [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
                (1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1),
            ]:
                coords = [
                    (x + step * dir[0], y + step * dir[1])
                    for step in range(len("XMAS"))
                ]
                word = [
                    grid[_y][_x]
                    for (_x, _y) in coords
                    if 0 <= _x < len(grid[0]) and 0 <= _y < len(grid)
                ]

                if "".join(word) == "XMAS":
                    countPart1 += 1

print("Part 1", countPart1)


# Part 2

countPart2 = 0

for y in range(len(grid)):
    for x in range(len(grid[y])):
        if grid[y][x] == "A":
            # We need two valid diagos to validate the A

            validDiagoCount = 0

            for diagos in [
                [(-1, -1), (1, 1)],
                [(-1, 1), (1, -1)],
            ]:
                coords = [(x + d[0], y + d[1]) for d in diagos]
                word = [
                    grid[_y][_x]
                    for (_x, _y) in coords
                    if 0 <= _x < len(grid[0]) and 0 <= _y < len(grid)
                ]

                if "".join(word) in ["SM", "MS"]:
                    validDiagoCount += 1
            if validDiagoCount == 2:
                countPart2 += 1

print("Part 2", countPart2)
