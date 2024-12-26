import aoc
from typing import NamedTuple, Set, Mapping, Literal, Tuple

data = aoc.getInputForDay(24)
# data = aoc.getInputForDay(24, force_filepath="inputs/day24_mini_example.txt")

Wire = str
GateType = Literal["AND", "OR", "XOR"]


class Gate(NamedTuple):
    inputs: Tuple[Wire, Wire]
    output: Wire
    type: GateType


wireValues: Mapping[Wire, int] = dict()
gates: Set[Gate] = set()

_ivs, _gates = data.strip().split("\n\n")
for iv in _ivs.split("\n"):
    wireName, wireValue = iv.split(": ")
    wireValues[wireName] = int(wireValue)
    assert int(wireValue) == 0 or int(wireValue) == 1

for gate in _gates.strip().split("\n"):
    in1, gType, in2, _, out = gate.split(" ")
    assert gType in ["AND", "OR", "XOR"]
    gates.add(Gate((in1, in2), out, gType))

# Part 1 : Simulate all gates until all wires are active
while any([gate.output not in wireValues for gate in gates]):

    updatedGate = False

    for gate in gates:
        if gate.output in wireValues:
            continue

        if all([i in wireValues for i in gate.inputs]):
            if gate.type == "AND":
                wireValues[gate.output] = (
                    wireValues[gate.inputs[0]] & wireValues[gate.inputs[1]]
                )
            elif gate.type == "OR":
                wireValues[gate.output] = (
                    wireValues[gate.inputs[0]] | wireValues[gate.inputs[1]]
                )
            elif gate.type == "XOR":
                wireValues[gate.output] = (
                    wireValues[gate.inputs[0]] ^ wireValues[gate.inputs[1]]
                )
            else:
                raise ValueError(f"Unknown gate type {gate.type}")

            updatedGate = True

    if not updatedGate:
        raise ValueError("No gate could be updated")

zOutputs = reversed(sorted([w for w in wireValues if w.startswith("z")]))

binNumber = "".join([str(wireValues[z]) for z in zOutputs])
decNumber = int(binNumber, 2)

print("Part 1", decNumber)
# 27736402580757 too low
