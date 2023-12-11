# Problem: https://adventofcode.com/2023/day/10
import sys
import time
import re

vprint = print if '-v' in sys.argv else lambda *a, **k: None

"""
Each path tuple shows whether it can be passed through from the top, bottom,
left, and right (respectively).
"""
PATHS = {
    '|': (True, True, False, False),
    '-': (False, False, True, True),
    'L': (True, False, False, True),
    'J': (True, False, True, False),
    '7': (False, True, True, False),
    'F': (False, True, False, True),
    '.': (False, False, False, False),
    'S': (True, True, True, True),
}


def parse_input(input: list[str]) -> tuple[int, int, list[str]]:
    """
    Returns the starting position as: (row, col, grid)
    """
    for row, line in enumerate(input):
        if 'S' in line:
            return (row, line.index('S'), input)
    return (-1, -1, input)


def find_valid_paths(r: int, c: int, grid: list[str],
                     visited: set[tuple[int, int]]) \
                             -> tuple[bool, bool, bool, bool]:
    """
    Returns valid paths in the order of up, down, left, right
    """
    up = down = left = right = False
    if r < len(grid) - 1 and (r + 1, c) not in visited:
        down = PATHS[grid[r + 1][c]][0]

    if r > 0 and (r - 1, c) not in visited:
        up = PATHS[grid[r - 1][c]][1]

    if c < len(grid[r]) - 1 and (r, c + 1) not in visited:
        right = PATHS[grid[r][c + 1]][2]

    if c > 0 and (r, c - 1) not in visited:
        left = PATHS[grid[r][c - 1]][3]

    return (up, down, left, right)


def part1(input: tuple[int, int, list[str]]):
    row, col, grid = input
    for line in grid:
        vprint(line)
    vprint()
    vprint(f'Starting from ({row}, {col})')
    print('Processing...')

    # Perform a BFS to find the furthest distance from the starting position
    # TODO: This is a kind-of-slow way to solve this problem. I'm sure there's
    #       a better way to do this.
    furthest_distance = 0
    bfs_queue = [(row, col, 0)]
    visited = set([(row, col)])
    while bfs_queue:
        r, c, dist = bfs_queue.pop(0)
        furthest_distance = max(furthest_distance, dist)
        up, down, left, right = find_valid_paths(r, c, grid, visited)
        vprint(f'Visiting ({r}, {c})\tDistance: {dist}', end='\t')
        vprint(f'Paths: {up} {down} {left} {right}', end='\t')
        vprint(f'Visited: {visited}')
        if up:
            bfs_queue.append((r - 1, c, dist + 1))
        if down:
            bfs_queue.append((r + 1, c, dist + 1))
        if left:
            bfs_queue.append((r, c - 1, dist + 1))
        if right:
            bfs_queue.append((r, c + 1, dist + 1))
        visited.add((r, c))

    print('Furthest distance:', furthest_distance)


def is_vertical_path(r: int, c: int, grid: list[str]) -> bool:
    """
    Returns True if the path at (r, c) is vertical, False otherwise
    """
    symbol = grid[r][c]
    return PATHS[symbol][0] or PATHS[symbol][1]


def find_loop_nodes(start_r: int, start_c: int, grid: list[str]) \
        -> list[tuple[int, int]]:
    def dfs(r: int, c: int, path: list[tuple[int, int]]) \
            -> list[tuple[int, int]]:
        pass

    path = []
    # TODO: Perform a DFS to find the node path that loops back to the start
    return path


def part2(input: tuple[int, int, list[str]]):
    row, col, grid = input
    debug_regex = re.compile(r'\.')
    for line in grid:
        vprint(line, len(debug_regex.sub('', line)))
    vprint()
    vprint(f'Starting from ({row}, {col})')
    print('Processing...')

    # 1. Find the maximum distance path that loops back to the starting
    #    position
    loop_nodes = find_loop_nodes(row, col, row, col, grid)
    print(f'Loop nodes ({len(loop_nodes)}):', loop_nodes)

    # Calculate the area of the loop (using raycasting)
    area = 0
    is_inside_loop = False
    for r, line in enumerate(input):
        for c, symbol in enumerate(line):
            if symbol == '.' and is_inside_loop:
                area += 1
            elif (r, c) in loop_nodes and is_vertical_path(row, col, grid):
                if is_inside_loop and not PATHS[symbol][3]:
                    is_inside_loop = False
                elif not is_inside_loop and PATHS[symbol][2]:
                    is_inside_loop = True

    print('Area:', area)


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
