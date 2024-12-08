from pathlib import Path

from common import read_input, Equation, ADD, MULTIPLY, solvable


def solve(equations: list[Equation]) -> int:
    operators = [ADD, MULTIPLY]
    return sum(eq.solution for eq in equations if solvable(eq, operators=operators))


def main():
    equations = read_input(Path('input.txt'))
    solution = solve(equations)
    print(solution)


if __name__ == '__main__':
    main()
