# Problem: https://adventofcode.com/2023/day/8
import sys
import time

VERBOSE = True


def vprint(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)


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


def part2(input: (str, dict[str, list[str]])):
    starting_nodes = [node for node in input[1].keys() if node.endswith('A')]
    print(input[1])
    print(starting_nodes)


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
