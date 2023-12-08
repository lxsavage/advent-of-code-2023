# Problem: https://adventofcode.com/2023/day/8
import sys
import time


def parse_input(input: list[str]) -> any:
    pass


def part1(input: any):
    pass


def part2(input: any):
    pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <input_file>')
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
