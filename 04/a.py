from pathlib import Path

from common import read_input, Position

DIRECTIONS = list(map(
    lambda x: Position(*x),
    [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
))


def has_word(matrix: list[list[str]], position: Position, movement: Position, word: str) -> bool:
    if not position.on_grid(matrix):
        return False

    current_letter = matrix[position.i][position.j]

    if current_letter != word[0]:
        return False

    if word == current_letter:
        return True

    return has_word(matrix,
                       position=position + movement,
                       movement=movement,
                       word=word[1:])


def count_words_from_start(matrix: list[list[str]], start: Position, word: str) -> int:
    return sum(has_word(matrix, position=start, movement=d, word=word) for d in DIRECTIONS)


def solve(matrix: list[list[str]]) -> int:
    word = 'XMAS'
    total = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            start_position = Position(i, j)
            total += count_words_from_start(matrix, start=start_position, word=word)

    return total


def main():
    input_file = 'input.txt'

    matrix = read_input(Path(input_file))
    solution = solve(matrix)
    print(solution)

if __name__ == '__main__':
    main()
