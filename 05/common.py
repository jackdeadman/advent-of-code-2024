import functools
from pathlib import Path
from collections import defaultdict
from typing import TypeVar, Optional

T = TypeVar('T')
AdjacencyList = dict[int, list[int]]


def topological_sort(adjacency_list: AdjacencyList) -> list[int]:
    visited = set()
    stack = []

    def __dfs(node: int):
        visited.add(node)
        for neighbor in adjacency_list.get(node, []):
            if neighbor not in visited:
                __dfs(neighbor)
        stack.append(node)

    for n in adjacency_list:
        if n not in visited:
            __dfs(n)

    return stack[::-1]

def get_sub_graph(graph: AdjacencyList, update: list[int]) -> AdjacencyList:
    update = set(update)
    sub_graph = defaultdict(list)

    for key in update:
            for value in graph[key]:
                if value in update:
                    sub_graph[key].append(value)
    return sub_graph

def sort_update(graph: AdjacencyList, update: list[int], follow_transitive_edges: Optional[bool] = True) -> list[int]:
    if follow_transitive_edges:
        sub_graph = get_sub_graph(graph, update)
        return topological_sort(sub_graph)
    else:
        # Slightly faster if we don't need to consider transitive dependencies
        key_fn = functools.cmp_to_key(lambda a, b: -1 if b in graph[a] else 1)
        return sorted(update, key=key_fn)

def read_input(input_file: Path) -> tuple[AdjacencyList, list[list[int]]]:

    adjacency_list: AdjacencyList = defaultdict(list)
    pages: list[list[int]] = []

    with open(input_file) as f:

        for line in f:
            if '|' in line:
                l, r = line.split('|')
                l = int(l.strip())
                r = int(r.strip())

                adjacency_list[l].append(r)
            elif line != '\n':
                num_strs = line.strip().split(',')
                nums = [int(num_str.strip()) for num_str in num_strs]
                pages.append(nums)

    return adjacency_list, pages





