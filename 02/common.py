from pathlib import Path

DELIMITER = ' '

def read_input(input_file: Path) -> list[list[int]]:
    matrix = []

    with open(input_file, 'r') as f:
        for line in f:
            matrix.append(list(map(int, line.split(DELIMITER))))

    return matrix
