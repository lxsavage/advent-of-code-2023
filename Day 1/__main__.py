# Problem: https://adventofcode.com/2023/day/1
import sys


DIGIT_NAMES = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'zero': 0,
}


def find_first_digit(line: str) -> str:
    for i in range(len(line)):
        letter = line[i]
        if letter.isdigit():
            return letter
        elif letter.isalpha():
            for digit_name, digit in DIGIT_NAMES.items():
                if line[i:i + len(digit_name)] == digit_name:
                    return str(digit)
    return ''


def find_last_digit(line: str) -> str:
    for i in range(len(line) - 1, -1, -1):
        letter = line[i]
        if letter.isdigit():
            return letter
        elif letter.isalpha():
            for digit_name, digit in DIGIT_NAMES.items():
                if i - len(digit_name) < 0:
                    continue

                test_val = line[i - len(digit_name) + 1:i + 1]
                if test_val == digit_name:
                    return str(digit)
    return ''


def load_data(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


def get_calibration(line: str) -> int:
    left_number: str = find_first_digit(line)
    right_number: str = find_last_digit(line)
    return int(left_number + right_number)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <input_file>')
        sys.exit(1)

    data = load_data(sys.argv[1])

    total_calibration = 0
    for i, line in enumerate(data):
        line_calibration = get_calibration(line)
        total_calibration += line_calibration
        print(f'ln {i}, cal {line_calibration}: {line}')

    print(f'\nTotal calibration: {total_calibration}')
