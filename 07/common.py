from dataclasses import dataclass
from pathlib import Path
import operator
from typing import Callable
import math


@dataclass
class Equation:
    solution: int
    operands: list[int]

@dataclass
class Operator:
    symbol: str
    action: Callable[[int, int], int]

def concat(x, y):
    shift = math.ceil(math.log10(y + 1))
    return int(x*10**shift + y)


ADD = Operator('+', operator.add)
MULTIPLY = Operator('*', operator.mul)
CONCAT = Operator('||', action=concat)

def solvable(equation: Equation, operators: list[Operator]) -> bool:

    if len(equation.operands) == 1:
        return equation.operands[0] == equation.solution

    left, right = equation.operands[0], equation.operands[1]

    # Ops can only increase the value so we can stop early if we exceed the solution
    if left > equation.solution:
        return False

    def _operator_solves(op: Operator) -> bool:
        result = op.action(left, right)
        new_operands = [result, *equation.operands[2:]]
        new_equation = Equation(equation.solution, new_operands)
        return solvable(new_equation, operators=operators)

    return any(_operator_solves(op) for op in operators)


def read_input(input_file: Path) -> list[Equation]:
    equations = []
    with open(input_file, 'r') as f:
        for line in f:
            solution, operands = line.strip().split(': ')
            solution = int(solution)
            operands = [int(i) for i in operands.split(' ')]
            equations.append(Equation(solution, operands))

    return equations
