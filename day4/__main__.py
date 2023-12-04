# Problem: https://adventofcode.com/2023/day/4
import sys


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <input_file>')
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        data = [line.strip() for line in f.readlines()]

    # Start here
    pass
