from pathlib import Path
from common import read_input


def solve(nums1: list[int], nums2: list[int]) -> int:
    return sum(abs(n1 - n2) for n1, n2 in zip(sorted(nums1), sorted(nums2)))


def main():
    input_file = 'input.txt'

    nums1, nums2 = read_input(Path(input_file))
    solution = solve(nums1, nums2)
    print(solution)

if __name__ == '__main__':
    main()