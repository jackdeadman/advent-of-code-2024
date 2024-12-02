from pathlib import Path
from common import read_input

def is_safe(row: list[int]) -> bool:
    dy = [b - a for a, b in zip(row, row[1:])]

    too_much = any(abs(d) > 3 for d in dy)
    all_increasing = all(d > 0 for d in dy)
    all_decreasing = all(d < 0 for d in dy)

    return (all_increasing or all_decreasing) and not too_much


def pluck_value(row: list[int], index: int) -> list[int]:
    return [x for i, x in enumerate(row) if i != index]

def is_safe_off_by_one(row: list[int]) -> bool:
    remove_index = 0
    row_to_test = row

    while (invalid := not is_safe(row_to_test)) and remove_index < len(row):
        row_to_test = pluck_value(row, index=remove_index)
        remove_index += 1

    return not invalid


def solve(matrix: list[list[int]]) -> int:
    return sum(map(is_safe_off_by_one, matrix))


def main():
    input_file = 'input.txt'

    matrix = read_input(Path(input_file))
    solution = solve(matrix)
    print(solution)

if __name__ == '__main__':
    main()