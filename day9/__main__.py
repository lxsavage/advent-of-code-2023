# Problem: https://adventofcode.com/2023/day/9
import sys
import time

vprint = print if '-v' in sys.argv else lambda *a, **k: None


def parse_input(input: list[str]) -> list[list[int]]:
    sequences = []
    for line in input:
        sequences.append([int(x) for x in line.split(' ')])
    return sequences


def generate_delta_sequence(sequence: list[int]) -> list[int]:
    deltas = []
    all_zeroes = True
    vprint('\t', sequence)
    for i in range(1, len(sequence)):
        delta = sequence[i] - sequence[i - 1]
        deltas.append(delta)
        if delta != 0:
            all_zeroes = False

    if all_zeroes:
        return sequence + [0]
    else:
        sub_deltas = generate_delta_sequence(deltas)
        deltas.append(sub_deltas[-1] + deltas[-1])
        return deltas


def part1(input: list[list[int]]):
    next_sum = 0
    for sequence in input:
        delta_sequence = generate_delta_sequence(sequence)
        next_number = sequence[-1] + delta_sequence[-1]
        next = next_number
        next_sum += next
        vprint(sequence)
        vprint(f'\tNext number: {next}')

    print(f'Sum of all predicted numbers: {next_sum}')


def part2(input: list[list[int]]):
    next_sum = 0
    for sequence in input:
        reversed_sequence = list(reversed(sequence))
        delta_sequence = generate_delta_sequence(reversed_sequence)
        next_number = reversed_sequence[-1] + delta_sequence[-1]
        next = next_number
        next_sum += next
        vprint(sequence)
        vprint(f'\tPrevious number: {next}')

    print(f'Sum of all predicted numbers: {next_sum}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <input_file> [2] [-v]')
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        input = parse_input([line.strip() for line in f.readlines()])

    start_time = time.time()
    if len(sys.argv) > 2 and sys.argv[2] == '2':
        part2(input)
    else:
        part1(input)

    completion_time = round(time.time() - start_time, 4)
    print(f'--- Completed in {completion_time} seconds ---')
