import itertools

with open("aoc_2023\\day_11.txt") as f:
    lines = [line.strip() for line in f.readlines()]

galaxies = []
cumulative_count_blank_rows = 0
blank_row_cumulative_dict = {}

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "#":
            galaxies.append((x, y))
    if all([char == "." for char in line]):
        cumulative_count_blank_rows += 1000000 - 1

    blank_row_cumulative_dict[y] = cumulative_count_blank_rows

cumulative_count_blank_cols = 0
blank_col_cumulative_dict = {}
for x in range(0, len(lines[0])):
    if all([row[x] == "." for row in lines]):
        cumulative_count_blank_cols += 1000000 - 1
    blank_col_cumulative_dict[x] = cumulative_count_blank_cols

total_dist = 0
for gal_1, gal_2 in itertools.combinations(galaxies, 2):
    distance = abs(gal_2[1] - gal_1[1]) + abs(gal_2[0] - gal_1[0])
    distance += abs(
        blank_col_cumulative_dict[gal_2[0]] - blank_col_cumulative_dict[gal_1[0]]
    )
    distance += abs(
        blank_row_cumulative_dict[gal_2[1]] - blank_row_cumulative_dict[gal_1[1]]
    )
    # print(f"{gal_1} -> {gal_2}: {distance=}")

    total_dist += distance

print(f"Part 2: {total_dist=}")
