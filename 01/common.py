from pathlib import Path

DELIMITER = '   '

def read_input(input_file: Path) -> tuple[list[int], list[int]]:
    nums1, nums2 = [], []

    with open(input_file, 'r') as f:
        for line in f:
            n1, n2 = map(int, line.split(DELIMITER))
            nums1.append(n1)
            nums2.append(n2)
    
    return nums1, nums2
