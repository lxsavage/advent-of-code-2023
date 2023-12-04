# Problem: https://adventofcode.com/2023/day/2
import sys

MAX_RED_CUBES = 12
MAX_GREEN_CUBES = 13
MAX_BLUE_CUBES = 14


def game_is_possible(game: dict) -> bool:
    for round in game['rounds']:
        if round['red'] > MAX_RED_CUBES or round['green'] > MAX_GREEN_CUBES \
                or round['blue'] > MAX_BLUE_CUBES:
            return False
    return True


def minimum_cubes_power(game: dict) -> int:
    min_cubes = {
        'red': 0,
        'green': 0,
        'blue': 0
    }

    for round in game['rounds']:
        if round['red'] > min_cubes['red']:
            min_cubes['red'] = round['red']
        if round['green'] > min_cubes['green']:
            min_cubes['green'] = round['green']
        if round['blue'] > min_cubes['blue']:
            min_cubes['blue'] = round['blue']

    return min_cubes['red'] * min_cubes['green'] * min_cubes['blue']


def get_round_counts(round_raw: str) -> dict:
    result = {
        'red': 0,
        'green': 0,
        'blue': 0
    }

    round_split = round_raw.split(',')
    for item in round_split:
        item_split = item.strip().split(' ')
        item_count = int(item_split[0])
        item_color = item_split[1]
        result[item_color] = item_count
    return result


def read_input(path: str) -> list[dict]:
    games = []
    with open(path, "r") as f:
        for line in f.readlines():
            if line.strip() == '':
                continue

            line_split = line.strip().split(":")
            game_struct = {
                'id': int(line_split[0].split(' ')[1]),
                'rounds': []
            }
            rounds_split = line_split[1].split(';')
            for round_split in rounds_split:
                game_struct['rounds'].append(get_round_counts(round_split))
            games.append(game_struct)
    return games


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <input_file>')
        sys.exit(1)

    games = read_input(sys.argv[1])
    part2_mode = len(sys.argv) > 2 and sys.argv[2] == '2'

    # Part 2
    if part2_mode:
        min_power_sum = 0
        for game in games:
            min_power_sum += minimum_cubes_power(game)
        print(f'Sum of minimum power: {min_power_sum}')
        sys.exit(0)

    # Part 1
    print(f'Checking possible games with max {MAX_RED_CUBES} red, {MAX_GREEN_CUBES} green and {MAX_BLUE_CUBES} blue cubes')

    possible_id_sum = 0
    for game in games:
        if game_is_possible(game):
            possible_id_sum += game['id']
            print(f'Game {game["id"]} is possible')

    print(f'Sum of possible game IDs: {possible_id_sum}')
