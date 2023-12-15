with open("aoc_2023\\day_13.txt") as f:
    grids = list(map(lambda grid: grid.split("\n"), f.read().split("\n\n")))
ans = 0


def find_vert_lines(grid):
    # rotate 90 clockwise
    new_grid = ["" for _ in range(len(grid[0]))]
    for j, row in enumerate(grid[::-1]):
        for i, char in enumerate(row, 0):
            new_grid[i] += char
    return find_hoz_lines(new_grid)


def find_hoz_lines(grid):
    lines = []
    grid_height = len(grid)
    for i in range(1, grid_height):
        mirror_height = min(i, grid_height - i)

        if grid[i - mirror_height : i] == grid[i + mirror_height - 1 : i - 1 : -1]:
            lines.append(i)
    return lines


for grid in grids:
    cols_above_hoz_ref = find_hoz_lines(grid)
    cols_to_left_vert_ref = find_vert_lines(grid)

    # print(f"{cols_to_left_vert_ref=}")
    # print(f"{cols_above_hoz_ref=}")
    to_add = sum(cols_to_left_vert_ref) + 100 * sum(cols_above_hoz_ref)
    ans += to_add
print(f"Part 1: {ans=}")

# Part 2
# every mirror has one smudge...
import copy


def fix_find_and_return_extra(grid):
    unsmudged_orig_hoz_lines = set(find_hoz_lines(grid))
    unsmudged_orig_vert_lines = set(find_vert_lines(grid))
    for j, row in enumerate(grid):
        # j = len(grid) - 1 - dj
        for i, char in enumerate(row):
            new_grid = copy.deepcopy(grid)
            temp_row_list = list(new_grid[j])
            temp_row_list[i] = "." if char == "#" else "#"
            new_grid[j] = "".join(temp_row_list)

            cols_above_hoz_ref = find_hoz_lines(new_grid)
            if (
                cols_above_hoz_ref
                and len(set(cols_above_hoz_ref) - unsmudged_orig_hoz_lines) > 0
            ):
                print(f"{cols_above_hoz_ref=}")
                new_set = set(cols_above_hoz_ref) - unsmudged_orig_hoz_lines
                if len(new_set) > 1:
                    raise ValueError
                return 100 * list(new_set)[0]

    for j, row in enumerate(grid):
        # j = len(grid) - 1 - dj
        for i, char in enumerate(row):
            new_grid = copy.deepcopy(grid)
            temp_row_list = list(new_grid[j])
            temp_row_list[i] = "." if list(grid[j])[i] == "#" else "#"
            new_grid[j] = "".join(temp_row_list)

            cols_to_left_vert_ref = find_vert_lines(new_grid)
            if cols_to_left_vert_ref and (
                len(set(cols_to_left_vert_ref) - unsmudged_orig_vert_lines) > 0
            ):
                print(f"{cols_to_left_vert_ref=}")
                new_set = set(cols_to_left_vert_ref) - unsmudged_orig_vert_lines
                if len(new_set) > 1:
                    raise ValueError
                return list(new_set)[0]

    raise ValueError


ans = 0

for grid in grids:
    ans += fix_find_and_return_extra(grid)


print(f"Part 2: {ans=}")
# 57729 too high
# 26346 too low
# 26846 too low

# this wording was really nasty and caught me out...!
