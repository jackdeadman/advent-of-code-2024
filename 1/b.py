from pathlib import Path
from common import read_input
from collections import Counter


def solve(nums1: list[int], nums2: list[int]) -> int:
    totals = Counter(nums2)
    return sum(n1 * totals[n1] for n1 in nums1)


def main():
    input_file = 'input.txt'

    nums1, nums2 = read_input(Path(input_file))
    solution = solve(nums1, nums2)
    print(solution)

if __name__ == '__main__':
    main()