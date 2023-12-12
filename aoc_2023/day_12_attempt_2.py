import re
import itertools
from collections import Counter

# instead try replacing ? with both a . or a #
# check "as we go" that the resulting record is compatible, if not, stop, if yes,
# iterate for a shorter record


def make_as_many_separate_springs_as_poss(arrange):
    new_list = []
    prev_char = "."
    for char in arrange:
        if char != "?":
            new_list.append(char)
            prev_char = char
        elif prev_char == ".":
            new_list.append("#")
            prev_char = "#"
        elif prev_char == "#":
            new_list.append(".")
            prev_char = "."
    return "".join(new_list)


def arrangement_compatible(record, arrange, check) -> bool:
    # string 1 must be the record
    # up_to_hash_q = re.search(r".+?(?=#+\?)", arrange).group(0)
    # set_so_far_match = re.search(r"^[#.]+?(?=#+\?)", arrange)
    set_so_far_match = re.search(r"^[#.]+?(?=(#+\?|\.\?))", arrange)
    up_to_q = set_so_far_match.group(0) if set_so_far_match else ""
    subset_check = [x.end() - x.start() for x in re.finditer(r"#+", up_to_q)]
    if subset_check != check[: len(subset_check)]:
        return False
    # first of record [?or#] must be >= first of check?
    possible_longest_springs = [
        x.end() - x.start() for x in re.finditer(r"[\?#]+", arrange)
    ]
    # if len(possbile_springs) < len(check): NOT VALID STATEMENT
    #     return False

    if sum(possible_longest_springs) < sum(check):
        return False
    left = Counter(possible_longest_springs) - Counter(check)
    if any([v < 0 for v in left.values()]):
        return False
    as_many_separate_springs_as_possible = make_as_many_separate_springs_as_poss(
        arrange
    )
    if len(re.findall(r"#+", as_many_separate_springs_as_possible)) < len(check):
        return False

    [x.end() - x.start() for x in re.finditer(r"([\?[\.\?*.][\#])+", arrange)]
    return True


assert (
    arrangement_compatible(
        "???.###????.###????.###????.###????.###",
        ".??.###????.###????.###????.###????.###",
        [1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3],
    )
    == False
)
assert (
    arrangement_compatible(
        ".??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.",
        "......?...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.",
        [1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3],
    )
    == True
)


def calculate(record, arrange, check):
    if arrangement_compatible(record, arrange, check):
        if not any([c == "?" for c in arrange]):
            return [x.end() - x.start() for x in re.finditer(r"#+", arrange)] == check
        else:
            first_q_to_dot = arrange.replace("?", ".", 1)
            first_q_to_hash = arrange.replace("?", "#", 1)
            return calculate(record, first_q_to_dot, check) + calculate(
                record, first_q_to_hash, check
            )
    else:
        return False


with open("aoc_2023\\day_12.txt") as f:
    lines = [line.strip().split(" ") for line in f.readlines()]


ans = 0

# for i, (record, check) in enumerate(lines, 1):
#     arrange = record
#     check = list(map(int, check.split(",")))
#     checked = set()
#     ans += calculate(record, arrange, check)

print(f"Part 1: {ans=}")


# Part 2
ans = 0
for i, (record, check) in enumerate(lines, 1):
    print(f"Line {i}")
    record = "?".join([record for _ in range(5)])
    check = ",".join([check for _ in range(5)])

    arrange = record
    check = list(map(int, check.split(",")))
    checked = set()
    ans += calculate(record, arrange, check)

print(f"Part 2: {ans=}")
