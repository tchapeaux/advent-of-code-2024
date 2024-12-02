import aoc

data = aoc.getLinesForDay(2)

reports = data
levels = [[int(l) for l in report.split(" ")] for report in reports]


def isSafe(levels: list[int]) -> bool:
    assert len(levels) >= 2
    isIncreasing = levels[0] < levels[1]

    for idx, level in enumerate(levels):
        if idx == 0:
            continue
        prevLevel = levels[idx - 1]

        if isIncreasing and level <= prevLevel:
            return False

        if not isIncreasing and level >= prevLevel:
            return False

        if not (1 <= abs(level - prevLevel) <= 3):
            return False

    return True


print("Part 1", len([ls for ls in levels if isSafe(ls)]))

# Brute force-y approach for Part 2
# Iterate over all reports with one level removed

accPart2 = 0

for oneReport in levels:
    for idxToRemove in range(len(oneReport)):
        reportCopy = oneReport[:]
        reportCopy.pop(idxToRemove)
        if isSafe(reportCopy):
            accPart2 += 1
            break

print("Part 2", accPart2)
