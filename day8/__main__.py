# Problem: https://adventofcode.com/2023/day/8
import sys
import time
import functools

vprint = print if '-v' in sys.argv else lambda *a, **k: None


def parse_input(input: list[str]) -> (str, dict[str, list[str]]):
    instructions = input[0]
    nodes = {}

    for line in input[2:]:
        split_node_children = line.split(' = ')
        node = split_node_children[0]
        children = split_node_children[1] \
            .replace('(', '') \
            .replace(')', '') \
            .split(', ')

        nodes[node] = children

    return (instructions, nodes)


def part1(input: (str, dict[str, list[str]])):
    instructions, nodes = input
    current_node = 'AAA'
    instruction_ptr = 0
    step_count = 0
    vprint('Instructions:', instructions)
    while current_node != 'ZZZ':
        instruction = instructions[instruction_ptr]
        previous_node = current_node
        current_node = nodes[current_node][1 if instruction == 'R' else 0]
        instruction_ptr = (instruction_ptr + 1) % len(instructions)
        step_count += 1
        vprint(f'{previous_node} -> {current_node}\tStep: {step_count}')
    print(step_count, 'steps')


def lcm(*args):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return a * b // gcd(a, b)

    return functools.reduce(lcm, args)


def find_period(
        node: str,
        instructions: str,
        nodes: dict[str, list[str]]) -> int:
    step_count = 0
    instruction_ptr = 0
    current_node = node
    while not current_node.endswith('Z'):
        vprint('\t', current_node)
        instruction = instructions[instruction_ptr]
        current_node = nodes[current_node][1 if instruction == 'R' else 0]
        step_count += 1
        instruction_ptr = (instruction_ptr + 1) % len(instructions)

    return step_count


def part2(input: (str, dict[str, list[str]])):
    instructions, nodes = input
    starting_nodes = [node for node in input[1].keys() if node.endswith('A')]
    vprint('Starting nodes:', starting_nodes)
    node_periods = [find_period(node, instructions, nodes)
                    for node in starting_nodes]
    vprint('Node periods:', node_periods)
    print(lcm(*node_periods), 'steps')


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
