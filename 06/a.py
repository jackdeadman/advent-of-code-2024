from pathlib import Path

from common import read_input, Position, Grid, simulate_movement_trail

def solve(player_pos: Position, grid: Grid) -> int:
    return len(simulate_movement_trail(player_pos, grid))


def main():
    player_pos, grid = read_input(Path('input.txt'))
    solution = solve(player_pos, grid)
    print(solution)



if __name__ == '__main__':
    main()
