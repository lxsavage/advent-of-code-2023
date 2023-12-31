# Problem: https://adventofcode.com/2023/day/0
import sys
import time

vprint = print if '-v' in sys.argv else lambda *a, **k: None


def parse_input(input: list[str]) -> any:
    pass


def part1(input: any):
    pass


def part2(input: any):
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
