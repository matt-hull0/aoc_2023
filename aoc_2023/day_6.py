import re
import math


def calc_race_margin(t, d):
    # return (
    #     math.floor((t + ((t**2) - (4 * d)) ** (0.5)) / 2)
    #     - math.ceil((t - ((t**2) - (4 * d)) ** (0.5)) / 2)
    #     + 1
    # )
    return (
        math.ceil(((t + ((t**2) - (4 * d)) ** (0.5)) / 2) - 1)
        - math.floor(((t - ((t**2) - (4 * d)) ** (0.5)) / 2) + 1)
        + 1
    )


with open("aoc_2023\\day_6.txt") as f:
    times, record_dists = map(
        lambda x: [int(y) for y in re.split(r"\s+", x.strip())[1:]], f.readlines()
    )
total_margin = 1
for t, d in zip(times, record_dists):
    margin = calc_race_margin(t, d)
    print(margin)
    total_margin *= margin

print(total_margin)
print(calc_race_margin(54817088, 446129210351007))
