from pathlib import Path

from common import read_input, Equation, ADD, MULTIPLY, CONCAT, solvable


def solve(equations: list[Equation]) -> int:
    operators = [ADD, MULTIPLY, CONCAT]
    return sum(
        eq.solution for eq in equations if solvable(eq, operators=operators))


def main():
    equations = read_input(Path('input.txt'))
    solution = solve(equations)
    print(solution)


if __name__ == '__main__':
    main()
