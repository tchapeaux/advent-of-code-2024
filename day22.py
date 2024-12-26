import aoc

data = aoc.getLinesForDay(22)

secrets = [int(x) for x in data]

# Example part 1
# secrets = [1, 10, 100, 2024]

# Example part 2
# secrets = [1, 2, 3, 2024]


def mix(a, b):
    return a ^ b


assert mix(42, 15) == 37


def prune(a):
    return a % 16777216


assert prune(100000000) == 16113920


def nextSecret(secret):
    s = secret

    # Step 1
    s = prune(mix(s, s * 64))

    # Step 2
    s = prune(mix(s, s // 32))

    # Step 3
    s = prune(mix(s, s * 2048))

    return s


assert nextSecret(123) == 15887950


def do2000gens(s):
    for _ in range(2000):
        s = nextSecret(s)
    return s


print("Part 1", sum(map(do2000gens, secrets)))

from typing import Tuple, Set, List

Sequence = Tuple[int, int, int, int]


def extractDigit(s):
    return s % 10


# Find all sequences that appears at least once

seenSequences: Set[Sequence] = set()

for s in secrets:
    digits: List[int] = []
    digits.append(extractDigit(s))
    for _ in range(2000):
        s = nextSecret(s)
        digits.append(extractDigit(s))
        if len(digits) > 4:
            seenSequences.add(
                (
                    digits[-4] - digits[-5],
                    digits[-3] - digits[-4],
                    digits[-2] - digits[-3],
                    digits[-1] - digits[-2],
                )
            )


# Check all seen sequences and find the one producing the most bananas

bestBananaCount = 0

for idx, (s1, s2, s3, s4) in enumerate(seenSequences):
    if idx % 100 == 0:
        print(idx, "/", len(seenSequences))

    bananaCount = 0
    for s in secrets:
        digits: List[int] = []
        digits.append(extractDigit(s))

        for _ in range(2000):
            s = nextSecret(s)
            digits.append(extractDigit(s))

            if len(digits) > 4:
                if (
                    digits[-4] - digits[-5],
                    digits[-3] - digits[-4],
                    digits[-2] - digits[-3],
                    digits[-1] - digits[-2],
                ) == (s1, s2, s3, s4):
                    bananaCount += digits[-1]
                    break

        if bananaCount > bestBananaCount:
            bestBananaCount = bananaCount

print("Part 2", bestBananaCount)
