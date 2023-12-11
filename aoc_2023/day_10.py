import numpy as np
from collections import defaultdict

with open("aoc_2023\\day_10.txt") as f:
    lines = [line.strip() for line in f.readlines()]

grid = defaultdict(lambda: ".")

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        grid[(x, y)] = char
        if char == "S":
            start_position = np.array([x, y])

print(f"{start_position=}")

possible_directions = np.array(
    [
        [0, 1],
        [0, -1],
        [1, 0],
        [-1, 0],
    ]
)

from typing import Tuple


def next_loc_next_dir(
    curr_loc: np.ndarray, curr_dir: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    next_loc = curr_loc + curr_dir

    if grid[tuple(next_loc)] == "|":
        next_dir = curr_dir
    elif grid[tuple(next_loc)] == "-":
        next_dir = curr_dir
    elif grid[tuple(next_loc)] == "L":
        if tuple(curr_dir) == (0, 1):
            next_dir = np.array([1, 0])
        elif tuple(curr_dir) == (-1, 0):
            next_dir = np.array([0, -1])
        else:
            raise ValueError(f"Unexpected Direction")
    elif grid[tuple(next_loc)] == "J":
        if tuple(curr_dir) == (0, 1):
            next_dir = np.array([-1, 0])
        elif tuple(curr_dir) == (1, 0):
            next_dir = np.array([0, -1])
        else:
            raise ValueError(f"Unexpected Direction")
    elif grid[tuple(next_loc)] == "7":
        if tuple(curr_dir) == (0, -1):
            next_dir = np.array([-1, 0])
        elif tuple(curr_dir) == (1, 0):
            next_dir = np.array([0, 1])
        else:
            raise ValueError(f"Unexpected Direction")
    elif grid[tuple(next_loc)] == "F":
        if tuple(curr_dir) == (0, -1):
            next_dir = np.array([1, 0])
        elif tuple(curr_dir) == (-1, 0):
            next_dir = np.array([0, 1])
        else:
            raise ValueError(f"Unexpected Direction")
    elif grid[tuple(next_loc)] == "S":
        next_dir = curr_dir
    else:
        raise ValueError(f"unexpected pipe char {grid[tuple(next_loc)]}")

    return next_loc, next_dir


# find a valid start direction:

for start_direction in possible_directions:
    try:
        _, _ = next_loc_next_dir(*next_loc_next_dir(start_position, start_direction))
        break
    except ValueError:
        continue

steps = 0
curr_pos, curr_dir = start_position, start_direction

points_on_path = set([tuple(start_position)])

while (steps == 0) or (grid[tuple(curr_pos)]) != "S":
    curr_pos, curr_dir = next_loc_next_dir(curr_pos, curr_dir)
    points_on_path.add(tuple(curr_pos))
    steps += 1
    # print(f"{curr_pos} at step {steps=}")

print(steps)
print(steps // 2)

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

# part 2

# keep track of all points on path - done above

# fix S

curr_dir_tuple = tuple(curr_dir)
start_direction_tuple = tuple(start_direction)
if curr_dir_tuple == (0, 1):
    if start_direction_tuple == (0, 1):
        fix_for_S = "|"
    elif start_direction_tuple == (-1, 0):
        fix_for_S = "J"
    elif start_direction_tuple == (1, 0):
        fix_for_S = "L"
    else:
        raise ValueError
elif curr_dir_tuple == (0, -1):
    if start_direction_tuple == (0, -1):
        fix_for_S = "|"
    elif start_direction_tuple == (-1, 0):
        fix_for_S = "7"
    elif start_direction_tuple == (1, 0):
        fix_for_S = "F"
    else:
        raise ValueError
elif curr_dir_tuple == (1, 0):
    if start_direction_tuple == (1, 0):
        fix_for_S = "-"
    elif start_direction_tuple == (0, 1):
        fix_for_S = "J"
    elif start_direction_tuple == (0, -1):
        fix_for_S = "7"
    else:
        raise ValueError
elif curr_dir_tuple == (-1, 0):
    if start_direction_tuple == (-1, 0):
        fix_for_S = "-"
    elif start_direction_tuple == (0, 1):
        fix_for_S = "F"
    elif start_direction_tuple == (0, -1):
        fix_for_S = "L"
    else:
        raise ValueError
else:
    raise ValueError

grid[(tuple(start_position))] = fix_for_S

# loop through every point on grid, check if enclosed


def is_enclosed(x, y) -> bool:
    # need odd nuimber of "crossings" on all sides and not on path itself
    # remove - and | and collapse any "inline" "F7", "7J" etc pairs

    if (x, y) in points_on_path:
        return False

    # collect parts of path to the left...
    path_points_to_left = [
        (_x, _y) for (_x, _y) in points_on_path if _y == y and _x < x
    ]
    path_points_to_left = sorted(path_points_to_left, key=lambda x: x[0])
    path_symbols = "".join([grid[_x, _y] for (_x, _y) in path_points_to_left])
    path_symbols = path_symbols.replace("-", "")
    path_symbols = path_symbols.replace("F7", "")
    path_symbols = path_symbols.replace("LJ", "")
    crossings = len(path_symbols.replace("|", "++")) / 2
    if crossings % 2 == 0:
        return False

    # check right
    path_points_to_right = [
        (_x, _y) for (_x, _y) in points_on_path if _y == y and _x > x
    ]
    path_points_to_right = sorted(path_points_to_right, key=lambda x: x[0])
    path_symbols = "".join([grid[_x, _y] for (_x, _y) in path_points_to_right])
    path_symbols = path_symbols.replace("-", "")
    path_symbols = path_symbols.replace("F7", "")
    path_symbols = path_symbols.replace("LJ", "")
    crossings = len(path_symbols.replace("|", "++")) / 2
    if crossings % 2 == 0:
        return False

    # check above
    path_points_above = [(_x, _y) for (_x, _y) in points_on_path if _y < y and _x == x]
    path_points_above = sorted(path_points_above, key=lambda x: x[1])
    path_symbols = "".join([grid[_x, _y] for (_x, _y) in path_points_above])
    path_symbols = path_symbols.replace("|", "")
    path_symbols = path_symbols.replace("7J", "")
    path_symbols = path_symbols.replace("FL", "")
    crossings = len(path_symbols.replace("-", "++")) / 2
    if crossings % 2 == 0:
        return False

    # check below
    path_points_below = [(_x, _y) for (_x, _y) in points_on_path if _y > y and _x == x]
    path_points_below = sorted(path_points_below, key=lambda x: x[1])
    path_symbols = "".join([grid[_x, _y] for (_x, _y) in path_points_below])
    path_symbols = path_symbols.replace("|", "")
    path_symbols = path_symbols.replace("7J", "")
    path_symbols = path_symbols.replace("FL", "")
    crossings = len(path_symbols.replace("-", "++")) / 2
    if crossings % 2 == 0:
        return False

    # all checks passed so must be
    return True


is_enclosed(14, 6)
num_enclosed = 0

for x, y in grid.keys():
    num_enclosed += is_enclosed(x, y)

print(f"{num_enclosed=}")

# 41 is wrong!
