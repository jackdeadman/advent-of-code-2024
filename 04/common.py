from pathlib import Path
from dataclasses import dataclass

@dataclass
class Position:
    i: int
    j: int

    def __add__(self, other: 'Position') -> 'Position':
        return Position(self.i + other.i, self.j + other.j)

    def on_grid(self, matrix: list[list[str]]) -> bool:
        return 0 <= self.i < len(matrix) and 0 <= self.j < len(matrix[self.i])

def read_input(input_file: Path) -> list[list[str]]:
    with open(input_file) as f:
        return [list(line.strip()) for line in f]
