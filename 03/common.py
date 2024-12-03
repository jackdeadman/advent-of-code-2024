from pathlib import Path

def read_input(input_file: Path) -> str:
    with open(input_file, 'r') as f:
        return f.read().strip()
