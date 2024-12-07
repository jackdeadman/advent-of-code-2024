import functools
from functools import cached_property
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Iterable


class Obstacle(Enum):
    OBJECT = '#'
    OPEN = '.'
    OOB = 'O'

@dataclass(frozen=True)
class Position:
    i: int
    j: int

    @property
    def pair(self) -> tuple[int, int]:
        return self.i, self.j

    def __add__(self, other):
        return Position(self.i + other.i, self.j + other.j)

@dataclass
class MutablePosition:

    i: int
    j: int

    def __add__(self, other):
        return MutablePosition(self.i + other.i, self.j + other.j)

    def __iadd__(self, other):
        self.i += other.i
        self.j += other.j
        return self

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def frozen(self):
        return Position(self.i, self.j)


@dataclass(frozen=True)
class Grid:
    grid: list[list[str]]

    @property
    def rows(self) -> int:
        return len(self.grid)

    @property
    def cols(self) -> int:
        return len(self.grid[0])

    @property
    def size(self) -> int:
        return self.rows * self.cols

    def __getitem__(self, pos: Position) -> str:
        return self.grid[pos.i][pos.j]

    def __setitem__(self, pos: Position, value: str) -> None:
        self.grid[pos.i][pos.j] = value

    def in_bounds(self, pos: Position) -> bool:
        return self[pos] != Obstacle.OOB.value
        # return 0 <= pos.i < self.rows and 0 <= pos.j < self.cols

    def display(self, player_pos: Optional[Position] = None, include_trail: bool = False) -> None:
        trail = None

        if include_trail:
            trail = simulate_movement_trail(player_pos, self)

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if player_pos is not None and Position(i, j) == player_pos:
                    print('X', end='')
                elif trail is not None and Position(i, j) in trail:
                    print('o', end='')
                else:
                    print(cell, end='')
            print()


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @property
    def vector(self) -> Position:
        if self == Direction.NORTH:
            return Position(-1, 0)
        elif self == Direction.EAST:
            return Position(0, 1)
        elif self == Direction.SOUTH:
            return Position(1, 0)
        elif self == Direction.WEST:
            return Position(0, -1)

    @classmethod
    def cycle(cls, start_pos: Optional['Direction'] = None) -> Iterable['Direction']:

        if start_pos is None:
            start_pos = cls.NORTH

        while True:
            yield start_pos
            start_pos = cls((start_pos.value + 1) % 4)

@dataclass
class Player:
    position: MutablePosition
    direction: Direction

    _direction_cycle: Iterable[Direction] = field(init=False, repr=False)

    def __post_init__(self):
        self._direction_cycle = iter(Direction.cycle(self.direction))
        next(self._direction_cycle)


    @property
    def next_position(self) -> Position:
        return self.position + self.direction.vector

    def move(self) -> None:
        self.position += self.direction.vector

    def simulate(self, grid: Grid, additional_position: Optional[Position] = None) -> bool:
        next_position = self.next_position

        if grid.in_bounds(next_position):

            if grid[next_position] == Obstacle.OBJECT.value or next_position == additional_position:
                self.direction = next(self._direction_cycle)
            else:
                self.move()
            return True
        return False


def simulate_movement_trail(player_pos: Position, grid: Grid) -> dict[Position, tuple[Position, Direction]]:
    direction_cycle = iter(Direction.cycle(Direction.NORTH))
    player = Player(player_pos, direction=next(direction_cycle))

    prev_position = player.position
    prev_direction = player.direction
    visited_positions = {player.position: (prev_position, prev_direction)}

    while player.simulate(grid):
        if player.position not in visited_positions:
            visited_positions[player.position] = (prev_position, prev_direction)
        prev_position = player.position
        prev_direction = player.direction

    return visited_positions

def pad_grid(grid: Grid) -> Grid:
    rows, cols = grid.rows, grid.cols

    new_grid = [[Obstacle.OOB.value for _ in range(cols + 2)] for _ in range(rows + 2)]

    for i in range(rows):
        for j in range(cols):
            new_grid[i + 1][j + 1] = grid[Position(i, j)]

    return Grid(new_grid)


def read_input(input_file: Path) -> tuple[Position, Grid]:
    grid = []
    player_pos = None

    with open(input_file, 'r') as f:
        for i, line in enumerate(f):
            row = []
            for j, c in enumerate(line.strip()):
                if c == '^':
                    if player_pos is not None:
                        raise ValueError('Multiple player positions found')
                    player_pos = Position(i, j)
                    row.append(Obstacle.OPEN.value)
                elif c in [Obstacle.OBJECT.value, Obstacle.OPEN.value]:
                    row.append(Obstacle(c).value)
                else:
                    raise ValueError(f'Invalid character {c} in input file')
            grid.append(row)

    if player_pos is None:
        raise ValueError('No player position found')

    grid = pad_grid(Grid(grid))

    # Adjust player position to account for padding
    player_pos = Position(player_pos.i + 1, player_pos.j + 1)

    return player_pos, grid





