import aoc

data = aoc.getInputForDay(1)


leftList = []
rightList = []

for line in data.strip().split("\n"):
    l, r = line.strip().split("   ")
    leftList.append(int(l))
    rightList.append(int(r))

leftList = sorted(leftList)
rightList = sorted(rightList)

accPart1 = 0

for l, r in zip(leftList, rightList):
    diff = abs(r - l)
    accPart1 += diff

print("Part 1", accPart1)


## Part 2

accPart2 = 0

for l in leftList:
    occurrences = rightList.count(l)
    accPart2 += l * occurrences

print("Part 2", accPart2)
