import re
import itertools
from collections import Counter


def arrangement_compatible(string1, string2) -> bool:
    # string 1 must be the record
    assert len(string1) == len(string2)
    if string2 in checked:
        raise ValueError("STILL CHECKING DUPS")
        return False
    for x, y in zip(string1, string2):
        if x == "#" and y != "#":
            return False
        if x == "." and y != ".":
            return False
    checked.add(string2)
    return True


def add_dot(seed, loc) -> str:
    if loc == 0:
        return "." + seed
    else:
        match = list(re.finditer(r"(#+)", seed))[loc - 1]

        return seed[0 : match.end()] + "." + seed[match.end() :]


def find_indices_to_add_dots(seed) -> tuple:
    matches = list(re.finditer(r"(#+)", seed))

    indices = (0, *(match.end() for match in matches))

    return indices


def calc_arrangements(record, seed, num_places_to_add_dots) -> int:
    if len(record) == len(seed):
        return arrangement_compatible(record, seed)
    else:
        num_dots_to_add = len(record) - len(seed)
        extra_arrangements = 0

        ind_to_add_dots = find_indices_to_add_dots(seed)
        for x in itertools.combinations_with_replacement(
            ind_to_add_dots, num_dots_to_add
        ):
            # print(x)
            ind_dot_counts = Counter(x)
            # print(ind_dot_counts)
            new_seed = seed
            for ind, num_dots in sorted(
                list(ind_dot_counts.items()), key=lambda x: x[0], reverse=True
            ):
                new_seed = new_seed[:ind] + "." * num_dots + new_seed[ind:]

            extra_arrangements += calc_arrangements(
                record, new_seed, num_places_to_add_dots
            )

        return extra_arrangements


with open("aoc_2023\\day_12.txt") as f:
    lines = [line.strip().split(" ") for line in f.readlines()]

ans = 0

# for i, (record, check) in enumerate(lines, 1):
#     print(f"Line {i}")
#     seed = ".".join([int(x) * "#" for x in check.split(",")])
#     start_dots = re.findall(r"(^\.+)", record)
#     if start_dots:
#         seed = start_dots[0] + seed
#     end_dots = re.findall(r"(\.+$)", record)
#     if end_dots:
#         seed = seed + end_dots[0]
#     # print(seed)
#     checked = set()
#     num_places_to_add_dots = len(check.split(",")) + 1

#     extra = calc_arrangements(record, seed, num_places_to_add_dots)
#     print(extra)
#     ans += extra

print(f"Part 1: {ans=}")


# Part 2
for i, (record, check) in enumerate(lines, 1):
    print(f"Line {i}")
    record = "?".join([record for _ in range(5)])
    check = ",".join([check for _ in range(5)])
    seed = ".".join([int(x) * "#" for x in check.split(",")])
    start_dots = re.findall(r"(^\.+)", record)
    if start_dots:
        seed = start_dots[0] + seed
    end_dots = re.findall(r"(\.+$)", record)
    if end_dots:
        seed = seed + end_dots[0]
    # print(seed)
    checked = set()
    num_places_to_add_dots = len(check.split(",")) + 1

    extra = calc_arrangements(record, seed, num_places_to_add_dots)
    print(extra)
    ans += extra

print(f"Part 1: {ans=}")

# old
# for record, check in lines:
#     record = record * 5
#     check = check * 5
#     seed = ".".join([int(x) * "#" for x in check.split(",")])
#     # print(seed)
#     checked = set()
#     num_places_to_add_dots = len(check.split(",")) + 1

#     ans += calc_arrangements(record, seed, num_places_to_add_dots)
