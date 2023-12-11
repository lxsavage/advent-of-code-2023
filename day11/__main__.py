# Problem: https://adventofcode.com/2023/day/0
import sys
import time

vprint = print if '-v' in sys.argv else lambda *a, **k: None


def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def blank_space_between(input: list[str],
                        r1: int, c1: int,
                        r2: int, c2: int,
                        expansion_factor: int) -> int:
    def empty_col(c: int) -> bool:
        for row in input:
            if row[c] != '.':
                return False
        return True

    def empty_row(r: int) -> bool:
        return input[r] == '.' * len(input[r])

    row_range = (min(r1, r2), max(r1, r2))
    col_range = (min(c1, c2), max(c1, c2))
    blank_rows_count = sum([1 for r in range(*row_range) if empty_row(r)])
    blank_cols_count = sum([1 for c in range(*col_range) if empty_col(c)])
    vprint(f'Blank rows: {blank_rows_count}, Blank cols: {blank_cols_count}')

    return (expansion_factor - 1) * (blank_rows_count + blank_cols_count)


def find_galaxies(grid: list[str]) -> list[list[tuple[int, int]]]:
    galaxies = []
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == '#':
                galaxies.append((r, c))

    return galaxies


def find_galaxy_distance_sum(galaxies: list[list[tuple[int, int]]],
                             expansion_factor: int = 2) -> int:
    sum_distance = 0
    for i, g1 in enumerate(galaxies):
        vprint(f'\n=== Galaxy {i + 1} ===')
        for j, g2 in enumerate(galaxies[i + 1:]):
            distance = manhattan_distance(g1, g2) + \
                blank_space_between(input, *g1, *g2, expansion_factor)

            sum_distance += distance
            vprint(f'{i + 1} -> {j + i + 2} | '
                   f'{g1} -> {g2} = {distance}')
    return sum_distance


def part1(input: list[str]):
    galaxies = find_galaxies(input)

    if vprint != (lambda *a, **k: None):
        vprint('Input:')
        for line in input:
            vprint(line)
        vprint()

        vprint('Galaxies:')
        for i, galaxy in enumerate(galaxies):
            vprint(f'{i + 1}:', galaxy)

    # Find the Manhattan distances between each pair of galaxies
    sum_distance = find_galaxy_distance_sum(galaxies)
    print(f'Total distance (ef 2): {sum_distance}')


def part2(input: list[str]):
    galaxies = find_galaxies(input)

    if vprint != (lambda *a, **k: None):
        vprint('Input:')
        for line in input:
            vprint(line)
        vprint()

        vprint('Galaxies:')
        for i, galaxy in enumerate(galaxies):
            vprint(f'{i + 1}:', galaxy)

    # Find the Manhattan distances between each pair of galaxies
    sum_distance = find_galaxy_distance_sum(galaxies, 1000000)
    print(f'Total distance (ef 1000000): {sum_distance}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <input_file> [2] [-v]')
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        input = [line.strip() for line in f.readlines()]

    start_time = time.time()
    if len(sys.argv) > 2 and '2' in sys.argv:
        part2(input)
    else:
        part1(input)

    completion_time = round(time.time() - start_time, 4)
    print(f'--- Completed in {completion_time} seconds ---')
