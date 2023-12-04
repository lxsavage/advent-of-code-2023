# Problem: https://adventofcode.com/2023/day/3
import sys

DEFAULT_MATCH = {
    'bounds': {
        'r': -1,
        'c_start': -1,
        'c_end': -1
    },
    'value': -1
}


def get_number_end(line: str, start_index: int) -> int:
    """
    Returns the index of the last digit of the number starting at start_index.
    """
    result = start_index + 1
    while result < len(line) and line[result].isdigit():
        result += 1

    return result


def seek_next_number(line: str, start: int) -> (int, int):
    """
    Returns the start and end index of the next number in the line after
    `start`. If no number is found, (-1, len(line)) is returned.
    """
    next_start = start
    while next_start < len(line) and not line[next_start].isdigit():
        next_start += 1

    if next_start >= len(line):
        return (-1, len(line))

    next_end = get_number_end(line, next_start)
    return (next_start, next_end)


def seek_next_match(line: str, previous_match: dict) -> dict:
    """
    Returns the start and end index of the next number in the line after
    `start`. If no number is found, (-1, len(line)) is returned.
    """
    next_match = DEFAULT_MATCH.copy()
    next_match['bounds']['r'] = previous_match['bounds']['r']
    next_match['bounds']['c_start'] = -1
    next_match['bounds']['c_end'] = previous_match['bounds']['c_end']

    next_start = previous_match['bounds']['c_end']
    while next_start < len(line) and not line[next_start].isdigit():
        next_start += 1

    if next_start >= len(line):
        return next_match

    next_match['bounds']['c_start'] = next_start
    next_match['bounds']['c_end'] = get_number_end(line, next_start)

    next_match['value'] = int(
        line[next_match['bounds']['c_start']:next_match['bounds']['c_end']]
    )
    return next_match


def number_has_adjacent_symbol(grid: list[str], number_details: dict) -> bool:
    """
    Returns True if the number has an adjacent symbol, False otherwise.
    Obtain number_details from seek_next_match

    Number Details spec:
    { 'bounds': { 'r': int, 'c_start': int, 'c_end': int }, 'value': int }
    """

    def is_symbol(char: chr) -> bool:
        return not char.isdigit() and char != '.'

    #
    # AABCDEE
    # A0123XE
    # AABCDEE
    #
    # Check outer edges for 0 and 3
    # Check top and bottom for every column
    #

    # Simplify checks
    is_on_top_row = number_details['bounds']['r'] == 0
    is_on_bottom_row = number_details['bounds']['r'] == len(grid) - 1
    is_on_left_edge = number_details['bounds']['c_start'] == 0
    is_on_right_edge = number_details['bounds']['c_end'] == len(grid[0])
    number_bounds = number_details['bounds']

    # Check left edge
    # # Check corners

    # # # Top left
    if not is_on_top_row and not is_on_left_edge and \
            is_symbol(grid[number_bounds['r'] - 1][number_bounds['c_start'] - 1]):
        return True

    # # # Bottom left
    if not is_on_bottom_row and not is_on_left_edge and \
            is_symbol(grid[number_bounds['r'] + 1][number_bounds['c_start'] - 1]):
        return True

    # # Check outside
    # # # Left
    if not is_on_left_edge and \
            is_symbol(grid[number_bounds['r']][number_bounds['c_start'] - 1]):
        return True

    # # # Right
    if not is_on_right_edge and \
            is_symbol(grid[number_bounds['r']][number_bounds['c_end']]):
        return True

    # Check inner numbers
    for col in range(number_bounds['c_start'], number_bounds['c_end']):
        # Top
        if not is_on_top_row and \
                is_symbol(grid[number_bounds['r'] - 1][col]):
            return True

        # Bottom
        if not is_on_bottom_row and \
                is_symbol(grid[number_bounds['r'] + 1][col]):
            return True

    # Check right edge
    # # Check corners
    # # # Top right
    if not is_on_top_row and not is_on_right_edge and \
            is_symbol(grid[number_bounds['r'] - 1][number_bounds['c_end']]):
        return True

    # # # Bottom right
    if not is_on_bottom_row and not is_on_right_edge and \
            is_symbol(grid[number_bounds['r'] + 1][number_bounds['c_end']]):
        return True

    # Catchall: No adjacent symbols found
    return False


def asterisk_is_gear(grid: list[str], row: int,
                     col: int) -> (bool, bool, bool, bool, bool, bool, bool,
                                   bool, bool):
    """
    Returns a tuple of booleans representing where numbers are adjacent to the
    specified symbol.
    The tuple is in the following order:
    (is_gear, top_left, top, top_right, left, right, bottom_left, bottom,
     bottom_right)
    """
    # Booleans for each adjacent number position possibility
    top_left = top = top_right = False
    left = right = False
    bottom_left = bottom = bottom_right = False

    neighbors_count = 0

    is_on_top_row = row == 0
    is_on_bottom_row = row == len(grid) - 1
    is_on_left_edge = col == 0
    is_on_right_edge = col == len(grid[row]) - 1

    # Check top row
    if not (is_on_top_row or is_on_left_edge) and \
            grid[row - 1][col - 1].isdigit():
        top_left = True
        neighbors_count += 1

    if not is_on_top_row and grid[row - 1][col].isdigit():
        top = True
        neighbors_count += 1

    if not (is_on_top_row or is_on_right_edge) and \
            grid[row - 1][col + 1].isdigit():
        top_right = True
        neighbors_count += 1

    # TODO: Subtract to account for the number being in multiple spots along
    #       the top row
    # e.g.: the following number is in 3 spots:
    # .1234.
    # ...*..

    # Check middle row
    if not is_on_left_edge and grid[row][col - 1].isdigit():
        left = True
        neighbors_count += 1

    if not is_on_right_edge and grid[row][col + 1].isdigit():
        right = True
        neighbors_count += 1

    # Check bottom row
    if not (is_on_bottom_row or is_on_left_edge) and \
            grid[row + 1][col - 1].isdigit():
        bottom_left = True
        neighbors_count += 1

    if not is_on_bottom_row and grid[row + 1][col].isdigit():
        bottom = True
        neighbors_count += 1

    if not (is_on_bottom_row or is_on_right_edge) and \
            grid[row + 1][col + 1].isdigit():
        bottom_right = True
        neighbors_count += 1

    # TODO: Subtract to account for the number being in multiple spots along
    #       the bottom row

    return (neighbors_count == 2, top_left, top, top_right,
            left, right, bottom_left, bottom, bottom_right)


def get_gear_ratio(grid: list[str], row: int, col: int,
                   adjacent_numbers: (bool, bool, bool, bool, bool, bool, bool,
                                      bool, bool)) -> int:
    """
    Returns the gear ratio of the gear at the specified position. Takes in the
    output of asterisk_is_gear so it doesn't need to recalculate adjacencies.
    """
    is_gear, top_left, top, top_right, left, right, bottom_left, bottom, \
        bottom_right = adjacent_numbers

    if not is_gear:
        return 0

    ratio = 1
    # TODO: Calculate
    return ratio


def part1(grid: list[str]) -> int:
    valid_numbers = []
    for row_i, line in enumerate(grid):
        seed_match = DEFAULT_MATCH.copy()
        seed_match['bounds']['c_end'] = 0
        seed_match['bounds']['r'] = row_i
        match = seek_next_match(line, seed_match)

        print(line + ':')
        while match['bounds']['c_start'] != -1:
            if number_has_adjacent_symbol(grid, match):
                valid_numbers.append(match.copy())
                print(f'Found match: {match}')

            match = seek_next_match(line, match.copy())

    valid_numbers_sum = sum([match['value'] for match in valid_numbers])
    print(f'Found {len(valid_numbers)} valid numbers')
    print(f'The sum of these numbers is: {valid_numbers_sum}')


def part2(grid: list[str]) -> int:
    gear_ratio_sum = 0
    gears = []
    for row_i, line in enumerate(grid):
        for col_i, char in enumerate(line):
            print(line)
            gear = asterisk_is_gear(grid, row_i, col_i)
            if char == '*' and gear[0]:
                print(f'Found gear at ({row_i}, {col_i})')
                gear_ratio_sum += get_gear_ratio(grid, row_i, col_i, gear)
                gears.append(gear)

    print(f'Found {len(gears)} gears')
    print(f'The sum of the gear ratios is: {gear_ratio_sum}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <input_file>')
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        grid = [line.strip() for line in f.readlines()]

    for line in grid:
        print(line)
    print()

    # Part 2
    if len(sys.argv) > 2 and sys.argv[2] == '2':
        part2(grid)
    else:
        part1(grid)
