from pathlib import Path

from common import read_input, sort_update


def solve(graph: dict[int, list[int]], updates: list[list[int]]) -> int:

    return sum(
        sort[len(sort) // 2]
        for update in updates
        if (sort := sort_update(graph, update)) == update
    )

def main():
    graph, updates = read_input(Path('input.txt'))
    solution = solve(graph, updates)
    print(solution)



if __name__ == '__main__':
    main()