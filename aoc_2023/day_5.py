with open("aoc_2023\\day_5.txt") as f:
    paragraphs = f.read().split("\n\n")

# print(paragraphs)

key, seeds_string = paragraphs[0].split(": ")
assert key == "seeds"

seeds_list = [{"seed": int(seed)} for seed in seeds_string.split(" ")]

maps = {}
for para in paragraphs[1:]:
    key_row, *number_rows = para.split("\n")
    source_key, _, destination_key = key_row.replace(" map:", "").split("-")

    mappings = []
    for row in number_rows:
        d, s, r = row.split(" ")
        mappings.append(
            {
                "dest_range_start": int(d),
                "source_range_start": int(s),
                "range_length": int(r),
            }
        )

    maps[source_key] = {"destination_key": destination_key, "mappings": mappings}


# print(seeds_list)
print(maps)


def parse_map(source: int, map: list[dict[str, int]]) -> int:
    for map_row in map:
        if source in range(
            map_row["source_range_start"],
            map_row["source_range_start"] + map_row["range_length"],
        ):
            return map_row["dest_range_start"] + (
                source - map_row["source_range_start"]
            )
    return source


key = "seed"

while key in maps.keys():
    next_key = maps[key]["destination_key"]

    for seed_dict in seeds_list:
        seed_dict[next_key] = parse_map(seed_dict[key], maps[key]["mappings"])

    key = next_key

print(seeds_list)

# find closest:

print(sorted(seeds_list, key=lambda x: x["location"])[0]["location"])


# --------------------------------------------------------------#
# Part 2
# --------------------------------------------------------------#

key, seeds_string = paragraphs[0].split(": ")
assert key == "seeds"

maps = {}
for para in paragraphs[1:]:
    key_row, *number_rows = para.split("\n")
    source_key, _, destination_key = key_row.replace(" map:", "").split("-")

    mappings = []
    for row in number_rows:
        d, s, r = row.split(" ")
        mappings.append(
            {
                "dest_range_start": int(d),
                "source_range_start": int(s),
                "range_length": int(r),
            }
        )

    maps[source_key] = {"destination_key": destination_key, "mappings": mappings}


def parse_map(source: int, map: list[dict[str, int]]) -> int:
    for map_row in map:
        if source in range(
            map_row["source_range_start"],
            map_row["source_range_start"] + map_row["range_length"],
        ):
            return map_row["dest_range_start"] + (
                source - map_row["source_range_start"]
            )
    return source


def parse_seed(seed_num):
    key = "seed"
    seed_dict = {key: seed_num}

    while key in maps.keys():
        next_key = maps[key]["destination_key"]

        seed_dict[next_key] = parse_map(seed_dict[key], maps[key]["mappings"])

        key = next_key

    return seed_dict["location"]


# find closest:

# print(sorted(seeds_list, key=lambda x: x["location"])[0]["location"])
# 462648396 too high

seeds_int_list = [int(num) for num in seeds_string.split(" ")]
seeds_list = []
nearest_location = None
i = 0
num_to_process = sum(seeds_int_list[1::2])

# for seed_start_num, seed_range in zip(seeds_int_list[::2], seeds_int_list[1::2]):
#     for seed_num in range(seed_start_num, seed_start_num + seed_range):
#         i += 1
#         if i % 1_000_000 == 0:
#             print(f"Got to i= {i:_}, % complete = {i *100 /num_to_process}")

#         seed_location = parse_seed(seed_num)
#         nearest_location = (
#             min(nearest_location, seed_location) if nearest_location else seed_location
#         )

# print(seed_location)


# Part 2 Attempt 2: Parse a range instead of individual seeds, splitting the range when req through the map:
# def parse_range_through_single_map()
from typing import Tuple


def parse_range_through_map(
    input_range: Tuple[int, int], map: dict[str, int]
) -> list[Tuple[int, int]]:
    map_start = map["source_range_start"]
    map_end = map["source_range_start"] + map["range_length"] - 1

    map_diff = map["dest_range_start"] - map["source_range_start"]

    if input_range[0] > map_end:
        assert input_range[0] > map_start
        assert input_range[0] > map_end
        assert input_range[1] > map_start
        assert input_range[1] > map_end
        return [input_range]
    elif input_range[1] < map_start:
        assert input_range[0] < map_start
        assert input_range[0] < map_end
        assert input_range[1] < map_start
        assert input_range[1] < map_end
        return [input_range]

    elif input_range[0] >= map_start:
        if input_range[1] <= map_end:
            assert input_range[0] >= map_start
            assert input_range[0] < map_end
            assert input_range[1] > map_start
            assert input_range[1] <= map_end
            return [(input_range[0] + map_diff, input_range[1] + map_diff)]

        else:
            assert input_range[0] >= map_start
            assert input_range[0] < map_end
            assert input_range[1] > map_start
            assert input_range[1] > map_end
            return [
                (input_range[0] + map_diff, map_end + map_diff),
                (map_end + 1, input_range[1]),
            ]

    elif map_end >= input_range[1]:
        assert input_range[0] < map_start
        assert input_range[0] < map_end
        assert input_range[1] >= map_start
        assert input_range[1] <= map_end
        return [
            (input_range[0], map_start - 1),
            (map_start + map_diff, input_range[1] + map_diff),
        ]

    else:
        assert input_range[0] < map_start
        assert input_range[0] < map_end
        assert input_range[1] > map_start
        assert input_range[1] > map_end
        return [
            (input_range[0], map_start - 1),
            (map_start + map_diff, map_end + map_diff),
            (map_end + 1, input_range[1]),
        ]


def parse_ranges_through_map(ranges_list, map_list):
    ranges_list = ranges_list.copy()
    new_ranges_list = []
    for range_row in ranges_list:
        new_range_row = [range_row]

        for map_row in sorted(map_list, key=lambda x: x["source_range_start"]):
            range_to_parse = new_range_row.pop()

            parsed_range = parse_range_through_map(range_to_parse, map_row)

            assert (range_to_parse[1] - range_to_parse[0] + 1) == sum(
                [r[1] - r[0] + 1 for r in parsed_range]
            )

            new_range_row += parsed_range
        new_ranges_list += new_range_row
    return new_ranges_list


def parse_seed_range(seed_start_num: int, seed_range: int):
    key = "seed"
    ranges_list = [(seed_start_num, seed_start_num + seed_range - 1)]
    print(f"{key=}")
    print(f"{ranges_list=}")
    while key in maps.keys():
        next_key = maps[key]["destination_key"]
        ranges_list = parse_ranges_through_map(ranges_list, maps[key]["mappings"])
        key = next_key
        print(f"{key=}")
        print(f"{ranges_list=}")
    return ranges_list


for seed_start_num, seed_range in zip(seeds_int_list[::2], seeds_int_list[1::2]):
    nearest_seed_range_locations = parse_seed_range(seed_start_num, seed_range)

    nearest_seed_range_location = sorted(
        nearest_seed_range_locations, key=lambda x: x[0]
    )[0][0]
    nearest_location = (
        min(nearest_location, nearest_seed_range_location)
        if nearest_location
        else nearest_seed_range_location
    )

print(nearest_location)
# 276959229 too high
