# Problem: https://adventofcode.com/2023/day/4
import sys
import re

RE_WHITESPACE = re.compile(r'\s+')


def get_line_numbers(line: str) -> dict:
    numbers_str = line.split(': ')[1]
    split_number_groups = numbers_str.split('|')
    winning_numbers = [
        int(x) for x in RE_WHITESPACE.split(split_number_groups[0])
        if x.strip() != ''
    ]
    received_numbers = [
        int(x) for x in RE_WHITESPACE.split(split_number_groups[1])
        if x.strip() != ''
    ]

    return {
        'winning_numbers': sorted(winning_numbers),
        'received_numbers': sorted(received_numbers)
    }


def get_points(line_numbers: dict) -> int:
    winning_numbers = line_numbers['winning_numbers']
    received_numbers = line_numbers['received_numbers']
    points = 0

    for received_number in received_numbers:
        if received_number in winning_numbers:
            points += 1

    # Point counts double for every match
    return int(2 ** (points - 1)) if points > 0 else 0


def part1(data: list[str]):
    total_points = 0
    for line in data:
        line_parsed = get_line_numbers(line)
        card_points = get_points(line_parsed)
        print(line, 'Points: ', card_points)
        total_points += card_points
    print(f'Total points: {total_points}')


def part2(data: list[str]):
    lines = []
    for line in data:
        line_parsed = get_line_numbers(line)
        lines.append(line_parsed)

    # TODO: Complete
    pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <input_file>')
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        data = [line.strip() for line in f.readlines()]

    # Start here
    if len(sys.argv) > 2 and sys.argv[2] == '2':
        part2(data)
    else:
        part1(data)
