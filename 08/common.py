from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict

Position = complex

@dataclass
class Satellite:
    frequency: str
    position: Position

@dataclass
class GridShape:
    width: int
    height: int

    def __contains__(self, item: Position) -> bool:
        return 0 <= item.real < self.width and 0 <= item.imag < self.height



def group_by_frequency(satellites: list[Satellite]) -> dict[str, list[Satellite]]:
    sat_map = defaultdict(list)
    for sat in satellites:
        sat_map[sat.frequency].append(sat)
    return sat_map


def read_input(input_file: Path) -> tuple[list[Satellite], GridShape]:
    satalittes = []
    width = 0
    height = 0

    with open(input_file) as f:
        for i, line in enumerate(f):
            height += 1
            line = line.strip()
            for j, ch in enumerate(line):
                width = len(line)
                if ch != '.':
                    satalittes.append(Satellite(ch, complex(j, i)))

    return satalittes, GridShape(width, height)






