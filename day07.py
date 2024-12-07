import aoc

data = aoc.getLinesForDay(7)

equations = []

for line in data:
    l, r = line.split(": ")
    r = r.split(" ")
    equations.append((int(l), [int(_r) for _r in r]))


def isValidEquation(
    testValue: int, operators: list[int], withConcatenation: bool = False
) -> bool:
    assert len(operators) > 0

    if len(operators) == 1:
        return operators[0] == testValue

    # Test + and * options
    operatorsSum = [operators[0] + operators[1]] + operators[2:]
    if isValidEquation(testValue, operatorsSum, withConcatenation):
        return True

    operatorsMul = [operators[0] * operators[1]] + operators[2:]
    if isValidEquation(testValue, operatorsMul, withConcatenation):
        return True

    if withConcatenation:
        operatorsConcat = [int(str(operators[0]) + str(operators[1]))] + operators[2:]
        if isValidEquation(testValue, operatorsConcat, withConcatenation):
            return True

    return False


accPart1 = 0
accPart2 = 0

for e in equations:
    if isValidEquation(e[0], e[1], False):
        accPart1 += e[0]
        accPart2 += e[0]
    elif isValidEquation(e[0], e[1], True):
        accPart2 += e[0]

print("Part 1", accPart1)
print("Part 2", accPart2)
