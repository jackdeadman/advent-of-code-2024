import functools
import math
from functools import cached_property
from numbers import Complex
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Iterable


DirectionType = complex

class Obstacle(Enum):
    OBJECT = '#'
    OPEN = '.'
    OOB = 'O'

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

    def __getitem__(self, pos: complex) -> str:
        return self.grid[int(pos.imag)][int(pos.real)]

    def __setitem__(self, pos: complex, value: str) -> None:
        self.grid[int(pos.imag)][int(pos.real)] = value

    def in_bounds(self, pos: complex) -> bool:
        return self[pos] != Obstacle.OOB.value

    def display(self, player_pos: Optional[complex] = None, include_trail: bool = False) -> None:
        trail = None

        if include_trail:
            trail = simulate_movement_trail(player_pos, self)

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if player_pos is not None and complex(j, i) == player_pos:
                    print('X', end='')
                elif trail is not None and complex(j, i) in trail:
                    print('o', end='')
                else:
                    print(cell, end='')
            print()


NORTH = -1j
EAST = 1
SOUTH = 1j
WEST = -1

DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

def cycle_directions(start_pos: Optional[complex] = None) -> Iterable[complex]:
    if start_pos is None:
        start_pos = NORTH

    while True:
        yield start_pos
        start_pos *= 1j

@dataclass
class Player:
    position: complex
    direction: DirectionType

    _direction_cycle: Iterable[DirectionType] = field(init=False, repr=False)

    def __post_init__(self):
        self._direction_cycle = iter(cycle_directions(self.direction))
        next(self._direction_cycle)


    @property
    def next_position(self) -> complex:
        return self.position + self.direction

    def move(self) -> None:
        self.position += self.direction

    def simulate(self, grid: Grid, additional_position: Optional[complex] = None) -> bool:
        next_position = self.next_position
        next_item = grid[next_position]

        if next_item != Obstacle.OOB.value:

            if next_item == Obstacle.OBJECT.value or next_position == additional_position:
                self.direction = next(self._direction_cycle)
            else:
                self.move()
            return True
        return False


def simulate_movement_trail(player_pos: complex, grid: Grid) -> dict[complex, tuple[complex, DirectionType]]:
    direction_cycle = iter(cycle_directions())
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
            new_grid[i + 1][j + 1] = grid[complex(j, i)]

    return Grid(new_grid)


def read_input(input_file: Path) -> tuple[complex, Grid]:
    grid = []
    player_pos = None

    with open(input_file, 'r') as f:
        for i, line in enumerate(f):
            row = []
            for j, c in enumerate(line.strip()):
                if c == '^':
                    if player_pos is not None:
                        raise ValueError('Multiple player positions found')
                    player_pos = complex(j, i)
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
    player_pos += 1 + 1j

    return player_pos, grid





