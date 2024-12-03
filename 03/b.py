import re
from pathlib import Path
from typing import Generator, Iterator

from common import read_input

MUL_PATTERN = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)|don\'t\(\)|do\(\)')

def find_matches(input_string: str) -> Iterator[re.Match]:
    return MUL_PATTERN.finditer(input_string)


def find_mul_operands(input_string: str) -> Generator[tuple[int, int], None, None]:
    enabled = True
    for match in find_matches(input_string):
        if match.group() == "don't()":
            enabled = False
        elif match.group() == "do()":
            enabled = True
        elif enabled:
            l, r = int(match.group(1)), int(match.group(2))
            yield l, r

def solve(input_string: str) -> int:
    return sum(l * r for l, r in find_mul_operands(input_string))

def main():
    input_file = 'input.txt'

    input_string = read_input(Path(input_file))
    solution = solve(input_string)
    print(solution)

if __name__ == '__main__':
    main()