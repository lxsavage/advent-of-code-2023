# Problem: https://adventofcode.com/2023/day/5
import sys
import re
import itertools
import time

VERBOSE = False
RE_WHITESPACE = re.compile(r'\s+')


def parse_maps(data: list[str]) -> (list[int], list[dict]):
    """
    Parse the input data into a list of maps.
    :param data: The raw lines of the input data
    :return: A tuple, where the first element is the seeds and the second is
             the maps
    """
    seeds = [int(x) for x in RE_WHITESPACE.split(data[0].strip())[1:]]
    results: list[dict] = []
    current_map: dict = None
    for line in data[1:]:
        if line.strip() == '':
            continue
        elif line.strip().endswith('map:'):
            if current_map:
                results.append(current_map.copy())

            map_line_name = line.strip().replace(' map:', '')
            current_map = {
                'name': map_line_name,
                'maps': []
            }
            continue
        else:
            current_map['maps'].append(
                tuple(map(int, line.strip().split(' ')))
            )
    results.append(current_map.copy())
    return (seeds, results)


def map_seed_to_location(seed: int, maps: list[dict]) -> int:
    result = seed
    for map in maps:
        for (destination, source, range_) in map['maps']:
            if result >= source and result < source + range_:
                result = destination + (result - source)
                break
    return result


def part1(seeds: list[int], maps: list[dict]):
    min_seed = sys.maxsize
    for seed in seeds:
        location = map_seed_to_location(seed, maps)
        print(seed, location)
        if location < min_seed:
            min_seed = location

    print('Lowest Location number:', min_seed)


def part2(seeds: list[int], maps: list[dict]):
    """
    Brute force solution, may take a while to run (>5 mins)
    """
    def is_match(bounds: list[(int, int)], value: int) -> bool:
        for (lower, upper) in bounds:
            if value >= lower and value < upper:
                return True
        return False

    seed_ranges: list[(int, int)] = list(
        map(lambda x: (x[0], x[0] + x[1]),
            itertools.batched(seeds, 2))
    )
    reversed_maps = []
    for submap in reversed(maps):
        reversed_maps.append({
            'name': submap['name'],
            'maps': [(source, destination, range_) for (destination, source, range_) in submap['maps']]
        })

    for location in range(0, sys.maxsize):
        if is_match(seed_ranges, map_seed_to_location(location, reversed_maps)):
            print(f'Found seed {map_seed_to_location(location, reversed_maps)} at location: {location}')
            break


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <input_file> [2]')
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        data = [line.strip() for line in f.readlines()]

    seeds, seed_maps = parse_maps(data)
    if VERBOSE:
        for seed_map in seed_maps:
            print(seed_map['name'])
            for (destination, source, range_) in seed_map['maps']:
                print(f'{destination} <- {source} + {range_}')
        print()

    if len(sys.argv) > 2 and sys.argv[2] == '2':
        start_time = time.time()
        part2(seeds, seed_maps)
        elapsed = time.time() - start_time
        print(f'Elapsed time: {elapsed / 60.} minutes')
    else:
        part1(seeds, seed_maps)
