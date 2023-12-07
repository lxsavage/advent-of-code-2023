# Problem: https://adventofcode.com/2023/day/6
import sys
import time
import re
import math

# Set to True to print out more information for debugging purposes
VERBOSE = False

# Regular expressions
RE_WHITESPACE = re.compile(r'\s+')


def parse_input_p1(input: list[str]) -> list[dict[str, int]]:
    times = []
    distances = []
    for line in input:
        if line.startswith('Time'):
            nums = RE_WHITESPACE.split(line)[1:]
            times.extend([int(num) for num in nums if num.isdigit()])
        elif line.startswith('Distance'):
            nums = RE_WHITESPACE.split(line)[1:]
            distances.extend([int(num) for num in nums if num.isdigit()])

    # [{time: int, distance: int}]
    result = []
    for i in range(0, len(times)):
        result.append({
            'time': times[i],
            'distance': distances[i]
        })

    return result


def parse_input_p2(input: list[str]) -> dict[str, int]:
    result = {}
    for line in input:
        result['time' if line.startswith('Time')
               else 'distance'] = int(''.join(RE_WHITESPACE.split(line)[1:]))
    return result


def get_record_breaking_interval(record: dict[str, int]) -> (int, int):
    # Utilize the quadratic formula to derive the intersection between:
    # f(t) = 9 and f(t) = t(2T - t)
    time_float = float(record['time'])
    distance_float = float(record['distance'])
    sqrt_part = math.sqrt(time_float ** 2 - 4 * distance_float)
    minimum = .5 * (record['time'] - sqrt_part)
    maximum = .5 * (record['time'] + sqrt_part)
    return (math.floor(minimum), math.ceil(maximum))


def calculate_record_beating_strategies(input: list[dict[str, int]]):
    ways_to_beat_records = 1
    for record in input:
        minimum, maximum = get_record_breaking_interval(record)
        number_of_ways_to_win = maximum - minimum - 1
        ways_to_beat_records *= number_of_ways_to_win
        if VERBOSE:
            print(f'Time: {record["time"]}, Distance: {record["distance"]}',
                  end='\t')
            print(f'Interval: [{minimum}, {maximum}]')
            print(f'\tNumber of ways to win: {number_of_ways_to_win}',
                  end='\n\n')

    print(f'Number of ways to beat records: {ways_to_beat_records}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <input_file>')
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        input = [line.strip() for line in f.readlines()]

    start_time = time.time()
    if len(sys.argv) > 2 and sys.argv[2] == '2':
        calculate_record_beating_strategies([parse_input_p2(input)])
    else:
        calculate_record_beating_strategies(parse_input_p1(input))

    completion_time = round((time.time() - start_time) * 1000, 4)
    print(f'--- Completed in {completion_time} ms ---')
