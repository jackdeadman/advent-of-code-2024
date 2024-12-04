from pathlib import Path

from common import read_input, Position

SENTINEL = ' '

def reflect(matrix: list[list[str]]) -> list[list[str]]:
    n = len(matrix)
    new_matrix = [[' ' for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            new_matrix[i][j] = matrix[j][i]

    return new_matrix


def make_templates(x: str) -> list[list[list[str]]]:

    def __make_template(x: str) -> list[list[str]]:
        n = len(x)
        kernel = [[SENTINEL for _ in range(n)] for _ in range(n)]

        for i in range(n):
            kernel[i][i] = x[i]
            kernel[i][-i - 1] = x[i]

        return kernel

    base = __make_template(x)
    base_reversed = __make_template(x[::-1])

    templates = [
        base,
        base_reversed,
        reflect(base),
        reflect(base_reversed),
    ]

    return templates

def get_kernel(matrix: list[list[str]], centre: Position, size: int) -> list[list[str]]:
    kernel = [[SENTINEL for _ in range(size)] for _ in range(size)]

    amount = size // 2

    for di in range(-amount, amount + 1):
        for dj in range(-amount, amount + 1):
            position = centre + Position(di, dj)
            if position.on_grid(matrix):
                kernel[di + amount][dj + amount] = matrix[position.i][position.j]

    return kernel


def kernel_matches_template(kernel: list[list[str]], template: list[list[str]]) -> bool:
    for i in range(len(template)):
        for j in range(len(template[i])):
            if template[i][j] == SENTINEL:
                continue

            if template[i][j] != kernel[i][j]:
                return False
    return True


def solve(matrix: list[list[str]]) -> int:
    word = 'MAS'
    templates = make_templates(x=word)

    count = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            middle_position = Position(i, j)
            kernel = get_kernel(matrix, middle_position, size=len(word))

            for ti, template in enumerate(templates):
                if kernel_matches_template(kernel, template):
                    count += 1

    return count



def main():
    input_file = 'input.txt'
    matrix = read_input(Path(input_file))
    solution = solve(matrix)
    print(solution)

if __name__ == '__main__':
    main()