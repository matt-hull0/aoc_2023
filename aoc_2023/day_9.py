def predict_next(numbers: list[int]) -> int:
    differences = [num2 - num1 for num2, num1 in zip(numbers[1:], numbers[:-1])]

    if all([d == 0 for d in differences]):
        to_add = 0
    else:
        to_add = predict_next(differences)

    return numbers[-1] + to_add


# assert predict_next([3, 3, 3]) == 3
# assert predict_next([1, 2, 3]) == 4
assert predict_next([10, 13, 16, 21, 30, 45]) == 68

with open("aoc_2023\\day_9.txt") as f:
    lines = [line.strip().split(" ") for line in f.readlines()]


extrap = 0
for line in lines:
    line = [int(x) for x in line]

    extrap += predict_next(line)


print(f"Part 1: {extrap}")

# 1743490463 too high
# 931951663 too low

# Part 2

with open("aoc_2023\\day_9.txt") as f:
    lines = [list(map(int, line.strip().split(" "))) for line in f.readlines()]


extrap = 0
for line in lines:
    line = line[::-1]

    extrap += predict_next(line)


print(f"Part 2: {extrap}")
