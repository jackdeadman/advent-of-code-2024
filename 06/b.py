from pathlib import Path

from common import read_input, Position, Grid, Direction, Player, Obstacle, simulate_movement_trail, MutablePosition
import logging

# Make these optional deps as they are not required for the solution and I want to avoid using deps for the challenges.
# But they are useful for speeding up the solution and displaying the progress.
# Takes around 2s on Apple M1 Pro
try:
    from joblib import Parallel, delayed
    has_parallel = True
except ImportError:
    has_parallel = False
    logging.warning('joblib not installed, running in serial mode. Install optional dependencies for faster execution.')

try:
    from tqdm import tqdm
    has_tqdm = True
except ImportError:
    has_tqdm = False
    logging.warning('tqdm not installed, progress will not be displayed. Install optional dependencies for progress bars.')

def simulation_terminates(player: Player, grid: Grid, retroencabulator_position: Position) -> bool:
    rows, cols = grid.rows, grid.cols

    masks = [1 << d.value for d in Direction]

    # Keep track of visited cells and directions
    configs = [[0 for _ in range(cols)] for _ in range(rows)]
    prev_direction = player.direction
    while player.simulate(grid, additional_position=retroencabulator_position):
        # Only need to check if the direction changes
        # if prev_direction != player.direction:
        mask = masks[player.direction.value]
        if configs[player.position.i][player.position.j] & mask:
            return False
        configs[player.position.i][player.position.j] |= mask
        # prev_direction = player.direction

    return True


def solve(initial_pos: Position, grid: Grid) -> int:

    # Only need to consider positions we looked at in the previous part
    # as all other positions won't impact a solution we already knows terminates.
    positions = simulate_movement_trail(initial_pos, grid)

    def _solve_individual(retroencabulator_position: Position, positions=positions) -> bool:
        prev, direction = positions[retroencabulator_position]

        player = Player(
            prev,
            direction=direction
        )

        terminates = simulation_terminates(player, grid,
                                           retroencabulator_position=retroencabulator_position)

        return not terminates

    if has_tqdm:
        positions = tqdm(positions)

    if has_parallel:
        return sum(
            Parallel(n_jobs=-1)(delayed(_solve_individual)(retroencabulator_position)
                    for retroencabulator_position in positions))
    else:
        return sum(_solve_individual(retroencabulator_position)
                    for retroencabulator_position in positions)


def main():
    player_pos, grid = read_input(Path('input.txt'))
    solution = solve(player_pos, grid)
    print(solution)


if __name__ == '__main__':
    main()
