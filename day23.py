import aoc
from typing import Tuple, Set, Dict

data = aoc.getLinesForDay(23)
# data = aoc.getLinesForDay(23, force_filepath="inputs/day23_example.txt")

Computer = str
Network = Dict[Computer, Set[Computer]]


links: Network = dict()
for line in data:
    a, b = line.split("-")
    if a not in links:
        links[a] = set()
    if b not in links:
        links[b] = set()

    links[a].add(b)
    links[b].add(a)

LAN3 = Tuple[Computer, Computer, Computer]

# Find sets of 3 interconnected computers
# Optimize this by only considering b within the neighbors of a, and c within the neighbors of b
validLan3s: Set[LAN3] = set()
for a in links:
    for b in links[a]:
        for c in links[b]:
            if a == b or b == c or a == c:
                continue
            if (
                a in links[b]
                and a in links[c]
                and b in links[a]
                and b in links[c]
                and c in links[a]
                and c in links[b]
            ):
                canonicalSet = list(sorted([a, b, c]))
                validLan3s.add((canonicalSet[0], canonicalSet[1], canonicalSet[2]))

# Count those where at least one starts with t
print("Part 1", len([s for s in validLan3s if any([c.startswith("t") for c in s])]))


# Find the biggest clique

# Intuition: the computer forming the biggest clique are those who appear the most in the 3-cliques
# (This seem to be verified by the example, even if it requires additional pruning)

computerSeqCount: Dict[Computer, int] = dict()
for lan3 in validLan3s:
    for c in lan3:
        if c not in computerSeqCount:
            computerSeqCount[c] = 0
        computerSeqCount[c] += 1

maxSeqCount = max(computerSeqCount.values())
mostPopularComputers = [
    c for c in computerSeqCount.keys() if computerSeqCount[c] == maxSeqCount
]
print(
    "out of",
    len(links),
    "computers,",
    len(mostPopularComputers),
    "appear in",
    maxSeqCount,
    "3-cliques",
)

# Check all combinations in decreasing length order
# (Spoiler for my input: this was overkill because the full combination was the answer)
from itertools import combinations

for cliqueSize in range(len(mostPopularComputers), 0, -1):
    for clique in combinations(mostPopularComputers, cliqueSize):
        if all([a is b or b in links[a] for a in clique for b in clique]):
            print("Part 2", len(clique), ",".join(sorted(clique)))
            exit()
