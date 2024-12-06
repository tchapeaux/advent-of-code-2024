import aoc
from functools import cmp_to_key

raw = aoc.getInputForDay(5)
# raw = aoc.getInputForDay(5, force_filepath="inputs/day05_example.txt")

[rules, updates] = raw.split("\n\n")

rules = [r.split("|") for r in rules.strip().split("\n")]
updates = [u.split(",") for u in updates.strip().split("\n")]


def isValidUpdate(update, rules):
    for rule in rules:
        assert len(rule) == 2
        [before, after] = rule
        if before in update and after in update:
            if update.index(before) >= update.index(after):
                return False
    return True


# Use a custom cmp function to sort according to the rules
def cmpPages(page1, page2):
    for rule in rules:
        if rule[0] == page1 and rule[1] == page2:
            return -1
        if rule[0] == page2 and rule[1] == page1:
            return 1
    return 0


def sortFromRules(update):
    return sorted(update, key=cmp_to_key(cmpPages))


accPart1 = 0
accPart2 = 0

for update in updates:
    if isValidUpdate(update, rules):
        middlePage = update[len(update) // 2]
        accPart1 += int(middlePage)
    else:
        sortedUpdate = sortFromRules(update)
        middlePage = sortedUpdate[len(sortedUpdate) // 2]
        accPart2 += int(middlePage)

print("Part 1", accPart1)
print("Part 2", accPart2)

# 4987 too low
