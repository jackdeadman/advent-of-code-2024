from typing import Iterable

from itertools import combinations

from pathlib import Path

from common import read_input, Satellite, GridShape, group_by_frequency

def calc_antinodes_from_positions(s1: Satellite, s2: Satellite, grid_shape: GridShape) -> Iterable[complex]:
    delta = s1.position - s2.position
    node = s1.position

    yield node

    # Forward
    node = s1.position + delta
    while node in grid_shape:
        yield node
        node += delta

    # Backward
    node = s1.position - delta
    while node in grid_shape:
        yield node
        node -= delta

def find_antinodes_in_line(satellites: list[Satellite], grid_shape: GridShape) -> Iterable[complex]:
    for s1, s2 in combinations(satellites, 2):
        antinodes = calc_antinodes_from_positions(s1, s2, grid_shape=grid_shape)
        for a in antinodes:
            yield a

def solve(satellites: list[Satellite], grid_shape: GridShape) -> int:

    sat_map = group_by_frequency(satellites)

    antinodes = {
        antinode
        for _, sats in sat_map.items()
        for antinode in find_antinodes_in_line(sats, grid_shape=grid_shape)
    }

    return len(antinodes)


def main():
    satellites, grid_shape = read_input(Path('input.txt'))
    solution = solve(satellites, grid_shape)
    print(solution)


if __name__ == '__main__':
    main()
