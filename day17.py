import aoc

import re
import math
from typing import List, Tuple

data = aoc.getInputForDay(17)
# data = aoc.getInputForDay(17, force_filepath="inputs/day17_example.txt")
# data = aoc.getInputForDay(17, force_filepath="inputs/day17_example_2.txt")


registersRaw, programRaw = data.split("\n\n")
registers: List[int] = list(int(x) for x in re.findall(r"(\d+)", registersRaw))
assert len(registers) == 3
program: List[int] = list(int(x) for x in re.findall(r"(\d+)", programRaw))


def getComboValue(registers: List[int], comboOperand: int) -> int:
    assert 0 <= comboOperand <= 7
    if comboOperand <= 3:
        return comboOperand
    if comboOperand == 4:
        return registers[0]
    if comboOperand == 5:
        return registers[1]
    if comboOperand == 6:
        return registers[2]
    else:
        assert comboOperand == 7
        raise Exception("Invalid combo operand")


def showState(registers, program, instrPointer: int):
    print("Registers:", registers)
    print(f"Program: {','.join(str(x) for x in program)}")
    print(f"         {' ' * 2 * instrPointer}^")


def runProgram(
    registersInitialValue: List[int], program: List[int], verbose=False
) -> Tuple[int, int, int, List[int]]:
    """Returns the value of registers A, B, C, then the outputs"""
    registers = registersInitialValue[:]
    instrPointer = 0
    outputs: List[int] = []

    while instrPointer < len(program):
        if verbose:
            showState(registers, program, instrPointer)

        opcode = program[instrPointer]

        if opcode == 0:
            # adv
            combo = program[instrPointer + 1]
            numerator = registers[0]
            denominator = 2 ** getComboValue(registers, combo)
            registers[0] = math.floor(numerator / denominator)
            instrPointer += 2
        elif opcode == 1:
            # bxl
            operand = program[instrPointer + 1]
            registers[1] = registers[1] ^ operand
            instrPointer += 2
        elif opcode == 2:
            # bst
            combo = program[instrPointer + 1]
            registers[1] = getComboValue(registers, combo) % 8
            instrPointer += 2
        elif opcode == 3:
            # jnz
            if registers[0] == 0:
                instrPointer += 2
            else:
                operand = program[instrPointer + 1]
                instrPointer = operand
        elif opcode == 4:
            # bxc
            registers[1] = registers[1] ^ registers[2]
            instrPointer += 2
        elif opcode == 5:
            # out
            combo = program[instrPointer + 1]
            out = getComboValue(registers, combo) % 8
            if verbose:
                print("\tOUT", out)
            outputs.append(out)
            instrPointer += 2
        elif opcode == 6:
            # bdv
            combo = program[instrPointer + 1]
            numerator = registers[0]
            denominator = 2 ** getComboValue(registers, combo)
            registers[1] = math.floor(numerator / denominator)
            instrPointer += 2
        elif opcode == 7:
            # cdv
            combo = program[instrPointer + 1]
            numerator = registers[0]
            denominator = 2 ** getComboValue(registers, combo)
            registers[2] = math.floor(numerator / denominator)
            instrPointer += 2

    if verbose:
        print("Final State")
        showState(registers, program, instrPointer)
        print("Final output")
        print(outputs)

    return registers[0], registers[1], registers[2], outputs


# Examples from instructions
assert runProgram([0, 0, 9], [2, 6])[1] == 1
assert runProgram([10, 0, 0], [5, 0, 5, 1, 5, 4])[3] == [0, 1, 2]
assert runProgram([2024, 0, 0], [0, 1, 5, 4, 3, 0])[3] == [
    4,
    2,
    5,
    6,
    7,
    7,
    7,
    7,
    3,
    1,
    0,
]
assert runProgram([0, 29, 0], [1, 7])[1] == 26
assert runProgram([0, 2024, 43690], [4, 0])[1] == 44354

rA, rB, rC, outputs = runProgram(registers, program)
print("Part 1:", ",".join(str(o) for o in outputs))

# Try to find the value of registers A which causes the program to output itself
for rA in range(0, 10000):
    if rA % 1000 == 0:
        print(rA, "/", 10000)
    _, _, _, outputs = runProgram([rA, 0, 0], program)
    if len(outputs) == len(program) and all(
        outputs[i] == program[i] for i in range(len(program))
    ):
        print("Part 2:", rA)
        break

# I tried to brute-force up to 100,000,000, which took more than a minute, then gave up
# Don't want to decompile the program, so skipping Part 2 for this day (currently...)
