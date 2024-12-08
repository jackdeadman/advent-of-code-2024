from typing import Iterable

from itertools import combinations

from pathlib import Path

from common import read_input, Satellite, GridShape, group_by_frequency

def find_antinode(s1: Satellite, s2: Satellite) -> complex:
    delta = s1.position - s2.position
    return s1.position + delta

def find_all_antinodes(satellites: list[Satellite], grid_shape: GridShape) -> Iterable[complex]:
    for s1, s2 in combinations(satellites, 2):

        if (anti1 := find_antinode(s1, s2)) in grid_shape:
            yield anti1

        if (anti2 := find_antinode(s2, s1)) in grid_shape:
            yield anti2

def solve(satellites: list[Satellite], grid_shape: GridShape) -> int:

    sat_map = group_by_frequency(satellites)

    anti_nodes = {
        antinode
        for _, sats in sat_map.items()
        for antinode in find_all_antinodes(sats, grid_shape=grid_shape)
    }

    return len(anti_nodes)


def main():
    satellites, grid_shape = read_input(Path('input.txt'))
    solution = solve(satellites, grid_shape)
    print(solution)


if __name__ == '__main__':
    main()
