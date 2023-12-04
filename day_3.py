import re


def generate_grid(x_dim: int, y_dim: int, puzzle_input: list[str]) -> list[str]:
    larger_grid = ["." * (x_dim + 2)]
    for row in puzzle_input:
        new_row = "." + row + "."
        larger_grid.append(new_row)

    larger_grid.append("." * (x_dim + 2))
    return larger_grid


def is_symbol(char: str) -> bool:
    if re.match(r"[^\d.]", char):
        return True
    else:
        return False


def check_if_surrounded_by_symbol(x: int, y: int, grid: list[str]) -> bool:
    # above
    if is_symbol(grid[y - 1][x]):
        return True
    # below
    if is_symbol(grid[y + 1][x]):
        return True
    # left
    if any([is_symbol(char) for _y in range(y - 1, y + 2) for char in grid[_y][x - 1]]):
        return True
    # right
    if any([is_symbol(char) for _y in range(y - 1, y + 2) for char in grid[_y][x + 1]]):
        return True

    return False


with open("day_3.txt") as f:
    puzzle_input = [row.strip() for row in f.readlines()]

x_dim = len(puzzle_input[0])
y_dim = len(puzzle_input)

grid = generate_grid(x_dim, y_dim, puzzle_input)

total = 0

for y, row in enumerate(grid[1:-1], start=1):
    number_str = ""
    found_new_num = False
    surrounded_by_symbol = False
    for x, char in enumerate(row[1:-1], start=1):
        if char.isnumeric():
            number_str += char
            if not surrounded_by_symbol:
                surrounded_by_symbol = check_if_surrounded_by_symbol(x, y, grid)
            # BUG - deal with end of line...!
            if x == x_dim and surrounded_by_symbol:
                number_found = int(number_str)
                total += number_found

        elif len(number_str) > 0:
            # print(f"found num {number_str}, surrounded - {surrounded_by_symbol}")
            if surrounded_by_symbol:
                number_found = int(number_str)
                total += number_found
            number_str = ""
            surrounded_by_symbol = False


print(f"Part 1: {total}")

# Part 2
from typing import Tuple, Union


def battleship(x, y) -> dict[Tuple[int, int] : Union[None, int]]:
    if not grid[y][x].isnumeric():
        return

    start_x = x
    while grid[y][start_x - 1].isnumeric():
        start_x -= 1
    num_str = ""

    _x = start_x
    while grid[y][_x].isnumeric() and _x < len(grid[0]):
        num_str += grid[y][_x]
        _x += 1

    return (start_x, y, int(num_str))


def find_gear_teeth(x: int, y: int, grid: list[str]) -> list[int]:
    # assume max teeth is 3 digits long
    numbers_found = set()

    # above
    for _x, _y in zip(range(x - 1, x + 2), [y - 1 for _ in range(3)]):
        battleship_result = battleship(_x, _y)
        if battleship_result:
            numbers_found.add(battleship_result)

    # below
    for _x, _y in zip(range(x - 1, x + 2), [y + 1 for _ in range(3)]):
        battleship_result = battleship(_x, _y)
        if battleship_result:
            numbers_found.add(battleship_result)

    # left
    battleship_result = battleship(x - 1, y)
    if battleship_result:
        numbers_found.add(battleship_result)
    # right
    battleship_result = battleship(x + 1, y)
    if battleship_result:
        numbers_found.add(battleship_result)

    return numbers_found


gear_ratios = 0

for y, row in enumerate(grid[1:-1], start=1):
    for x, char in enumerate(row[1:-1], start=1):
        if char == "*":
            gears = find_gear_teeth(x, y, grid)

            if len(gears) == 2:
                ratio = 1
                for gear in gears:
                    ratio *= gear[2]
                gear_ratios += ratio


print(f"Part 2: {gear_ratios}")
