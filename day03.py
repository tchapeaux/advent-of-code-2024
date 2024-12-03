import aoc
import re

instr = aoc.getInputForDay(3).strip()

print(instr)

# Part 1
# Use regex to extract valid muls
pattern = r"mul\((\d{1,3}),(\d{1,3})\)"

matchesPart1 = re.findall(pattern, instr)

matchesPart2 = list(re.finditer(pattern, instr))
matchesPart2.extend(re.finditer(r"do\(\)", instr))
matchesPart2.extend(re.finditer(r"don't\(\)", instr))

matchesPart2.sort(key=lambda x: x.start())

accPart2 = 0
isActive = True

for match in matchesPart2:
    rawMatch = match.group()
    if "don't(" in rawMatch:
        isActive = False
    if "do(" in rawMatch:
        isActive = True
    if "mul(" in rawMatch:
        if isActive:
            accPart2 += int(match.groups(0)[0]) * int(match.groups(0)[1])

print("Part 2", accPart2)
