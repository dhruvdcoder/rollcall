from typing import List, Tuple


def remove_char_range(r: Tuple[int, int], line: str) -> str:

    new_line = line[:r[0]] + line[r[1]:]

    return new_line


def split_on_points(line: str, *args) -> List[str]:
    points = [0] + list(args) + [len(line)]
    prev_point = points[0]
    splits = []

    for point in points[1:]:
        splits.append(line[prev_point:point])
        prev_point = point

    return splits
