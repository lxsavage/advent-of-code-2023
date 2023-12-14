# Problem: https://adventofcode.com/2023/day/13
import sys
import time

vprint = print if '-v' in sys.argv else lambda *a, **k: None


def parse_input(input: list[str]) -> list[list[str]]:
    result = [[]]
    for line in input:
        if line == '':
            result.append([])
        else:
            result[-1].append(line)

    return result


def find_reflective_row(input: list[str]) -> int | None:
    def test_reflection(row: int) -> bool:
        for offset in range(1, len(input) - row):
            vprint(f'\t[{row - offset + 1}]: {input[row - offset + 1]}'
                   f'== [{row + offset}]: {input[row + offset]}')
            if row - offset < -1 or row + offset >= len(input):
                return True
            elif input[row - offset + 1] != input[row + offset]:
                return False
        return True

    # This will be the index of the row above the reflection line
    for j in range(0, len(input) - 1):
        vprint(f'Testing row {j}')
        if test_reflection(j):
            return j
    return None


def find_reflective_col(input: list[str]) -> int | None:
    def cols_equal(col1: int, col2: int) -> bool:
        for row in range(len(input)):
            if input[row][col1] != input[row][col2]:
                return False
        return True

    def test_reflection(col: int) -> bool:
        for offset in range(1, len(input[0]) - col):
            if col - offset < -1 or col + offset >= len(input[0]):
                return True
            elif not cols_equal(col - offset + 1, col + offset):
                return False
        return True

    # This will be the index of the left side of the reflection line
    for j in range(0, len(input[0]) - 1):
        vprint(f'Testing col {j}')
        if test_reflection(j):
            return j
    return None


def part1(input: list[list[str]]):
    pattern_note_sum = 0
    for pattern in input:
        for i, row in enumerate(pattern):
            vprint(i, row)
        vprint()
        reflective_row = find_reflective_row(pattern)
        if reflective_row is not None:
            pattern_note = 100 * (reflective_row + 1)
            vprint(f'Row {reflective_row} is reflective')
            vprint(f'Pattern note: {pattern_note}')
            pattern_note_sum += pattern_note
            continue

        reflective_col = find_reflective_col(pattern)
        if reflective_col is not None:
            pattern_note = reflective_col + 1
            vprint(f'Col {reflective_col} is reflective')
            vprint(f'Pattern note: {pattern_note}')
            pattern_note_sum += pattern_note
            continue

        vprint('No reflective rows or columns found')

    print(f'Pattern note sum: {pattern_note_sum}')


def part2(input: list[list[str]]):
    pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <input_file> [2] [-v]')
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        input = parse_input([line.strip() for line in f.readlines()])

    start_time = time.time()
    if len(sys.argv) > 2 and '2' in sys.argv:
        part2(input)
    else:
        part1(input)

    completion_time = round(time.time() - start_time, 4)
    print(f'--- Completed in {completion_time} seconds ---')
