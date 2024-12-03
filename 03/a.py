import re
from pathlib import Path
from typing import Generator

from common import read_input

MUL_PATTERN = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)')

def find_mul_operands(input_string: str) -> Generator[tuple[int, int], None, None]:
    for match in MUL_PATTERN.finditer(input_string):
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