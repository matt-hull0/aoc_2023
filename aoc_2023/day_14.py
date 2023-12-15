with open("aoc_2023\\day_14.txt") as f:
    grid = list(map(lambda line: list(line.strip()), f.readlines()))


def calculate_load(grid):
    total_load = 0
    for dist, row in enumerate(grid[::-1], 1):
        total_load += dist * sum([1 for c in row if c == "O"])
    return total_load


def roll_north(grid):
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == ".":
                # moved = False
                for _y in range(y + 1, len(grid)):
                    if grid[_y][x] == ".":
                        continue
                    elif grid[_y][x] == "#":
                        break
                    elif grid[_y][x] == "O":
                        grid[_y][x] = "."
                        grid[y][x] = "O"
                        break

                    else:
                        raise ValueError

    return grid


rolled_north = roll_north(grid)

ans = calculate_load(rolled_north)

print(f"Part 1: {ans}")

# Part 2
# roll north, then west, then south, then east

# to rotate clockwise..


def rotate_clock(grid):
    new_grid = [[] for _ in range(len(grid[0]))]
    for j, row in enumerate(grid[::-1]):
        for i, char in enumerate(row, 0):
            new_grid[i].append(char)
    return new_grid


cycles = 1_000_000_000
# detect a repeating pattern?
cycle_set = set()
cycle_dict = {}

for i in range(cycles):
    print(f"Part 2 ans = {calculate_load(grid)}")
    if i % 10_000 == 0:
        print(f"done {i}, {100*i/cycles}")
    for j in range(4):
        grid = roll_north(grid)
        grid = rotate_clock(grid)
    if "".join([c for row in grid for c in row]) in cycle_set:
        print(f"found cycle at {i=}")  # don't know length...
        print(f"check = {calculate_load(grid)}")
        cycle_period = i - cycle_dict["".join([c for row in grid for c in row])]
        print(f"{cycle_period=}")
        num_cycles_to_do = (cycles - (i + 1)) % cycle_period
        print(f"{num_cycles_to_do=}")
        for _ in range(num_cycles_to_do):
            for j in range(4):
                grid = roll_north(grid)
                grid = rotate_clock(grid)
        print(f"Part 2 ans = {calculate_load(grid)}")
        break

    else:
        cycle_set.add("".join([c for row in grid for c in row]))
        cycle_dict["".join([c for row in grid for c in row])] = i
print(f"Part 2 ans = {calculate_load(grid)}")
