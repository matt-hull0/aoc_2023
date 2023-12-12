import re


def arrangement_compatible(string1, string2) -> bool:
    # string 1 must be the record
    assert len(string1) == len(string2)
    if string2 in checked:
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


def calc_arrangements(record, seed, num_places_to_add_dots) -> int:
    if len(record) == len(seed):
        return arrangement_compatible(record, seed)
    else:
        extra_arrangements = 0
        for loc in range(num_places_to_add_dots):
            new_seed = add_dot(seed, loc)
            extra_arrangements += calc_arrangements(
                record, new_seed, num_places_to_add_dots
            )

        return extra_arrangements


with open("aoc_2023\\day_12.txt") as f:
    lines = [line.strip().split(" ") for line in f.readlines()]

ans = 0

for record, check in lines:
    seed = ".".join([int(x) * "#" for x in check.split(",")])
    # print(seed)
    checked = set()
    num_places_to_add_dots = len(check.split(",")) + 1

    ans += calc_arrangements(record, seed, num_places_to_add_dots)

print(f"Part 1: {ans=}")


# Part 2

for record, check in lines:
    record = record * 5
    check = check * 5
    seed = ".".join([int(x) * "#" for x in check.split(",")])
    # print(seed)
    checked = set()
    num_places_to_add_dots = len(check.split(",")) + 1

    ans += calc_arrangements(record, seed, num_places_to_add_dots)
