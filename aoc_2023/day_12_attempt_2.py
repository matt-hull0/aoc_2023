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


def calc_set_so_far(arr_string):
    q_ind = arr_string.find("?")
    arr_string = arr_string[0:q_ind]

    dot_ind = arr_string.rfind(".")
    arr_string = arr_string[0:dot_ind] if dot_ind != -1 else ""
    return arr_string


def arrangement_compatible(record, arrange, check) -> bool:
    # string 1 must be the record
    # up_to_hash_q = re.search(r".+?(?=#+\?)", arrange).group(0)
    # set_so_far_match = re.search(r"^[#.]+?(?=#+\?)", arrange)

    # check what is fixed so far matches the check
    # set_so_far_match = re.search(r"^[^#][#.]*?(?=(#+\?|\.\?))", arrange)
    # up_to_q = set_so_far_match.group(0) if set_so_far_match else ""
    up_to_q = calc_set_so_far(arrange)
    subset_check = [x.end() - x.start() for x in re.finditer(r"#+", up_to_q)]
    if subset_check != check[: len(subset_check)]:
        return False

    # check not too many # in next block of "undecided" ###??
    springs_up_to_undetermined = re.search(r"^[\.#]+[^\?]", arrange)
    springs_up_to_undetermined = (
        springs_up_to_undetermined.group(0) if springs_up_to_undetermined else ""
    )
    subset_check = [
        x.end() - x.start() for x in re.finditer(r"#+", springs_up_to_undetermined)
    ]

    if len(subset_check) > len(check):
        return False
    if subset_check and subset_check[-1] > check[len(subset_check) - 1]:
        return False

    # check possible to generate enough #
    # first of record [?or#] must be >= first of check?
    possible_longest_springs = [
        x.end() - x.start() for x in re.finditer(r"[\?#]+", arrange)
    ]

    if sum(possible_longest_springs) < sum(check):
        return False

    #
    left = Counter(possible_longest_springs) - Counter(check)
    if any([v < 0 for v in left.values()]):
        return False

    # check possible to make the number of distinct group of springs required
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


record = "?".join(["???.###" for _ in range(5)])
check = "1,1,3"
check = ",".join([check for _ in range(5)])
check = list(map(int, check.split(",")))
arrange = record
# assert calculate(record, arrange, check) == 1

record = "?".join([".??..??...?##." for _ in range(5)])
check = ",".join(["1,1,3" for _ in range(5)])
check = list(map(int, check.split(",")))
arrange = record
# assert calculate(record, arrange, check) == 16384

record = "?".join(["?#?#?#?#?#?#?#?" for _ in range(5)])
check = ",".join(["1,3,1,6" for _ in range(5)])
check = list(map(int, check.split(",")))
arrange = record
# assert calculate(record, arrange, check) == 1

record = "?".join(["????.#...#..." for _ in range(5)])
check = ",".join(["4,1,1" for _ in range(5)])
check = list(map(int, check.split(",")))
arrange = record
# assert calculate(record, arrange, check) == 16

record = "?".join(["????.######..#####." for _ in range(5)])
check = ",".join(["1,6,5" for _ in range(5)])
check = list(map(int, check.split(",")))
arrange = record
# assert calculate(record, arrange, check) == 2500

record = "?".join(["?###????????" for _ in range(5)])
check = ",".join(["3,2,1" for _ in range(5)])
check = list(map(int, check.split(",")))
arrange = record
# assert calculate(record, arrange, check) == 506250


with open("aoc_2023\\day_12.txt") as f:
    lines = [line.strip().split(" ") for line in f.readlines()]


ans = 0

for i, (record, check) in enumerate(lines, 1):
    arrange = record
    check = list(map(int, check.split(",")))
    checked = set()
    ans += calculate(record, arrange, check)

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
