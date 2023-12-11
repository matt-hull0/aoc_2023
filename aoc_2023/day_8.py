import re

with open("aoc_2023\\day_8.txt") as f:
    instructions, network_raw = f.read().split("\n\n")

network = {}
for line in network_raw.split("\n"):
    locations = re.findall(r"\w+", line)
    network[locations[0]] = (locations[1], locations[2])

current_location = "AAA"
end = "ZZZ"
steps = 0
directions = instructions[::-1]

while current_location != end:
    if len(directions) == 0:
        directions = instructions[::-1]

    next_direction = directions[-1]
    directions = directions[0:-1]
    next_index = 0 if next_direction == "L" else 1
    current_location = network[current_location][next_index]
    steps += 1

print(f"Part 1: {steps=}")

# Part 2

starting_locations = [node for node in network.keys() if node[-1] == "A"]
steps_to_get_to_z = []

for current_location in starting_locations:
    steps = 0
    directions = instructions[::-1]

    while current_location[-1] != "Z":
        if len(directions) == 0:
            directions = instructions[::-1]

        next_direction = directions[-1]
        directions = directions[0:-1]
        next_index = 0 if next_direction == "L" else 1
        current_location = network[current_location][next_index]
        steps += 1

    steps_to_get_to_z.append(steps)

# get lowest common multiple of all:
import math

lcm = math.lcm(*steps_to_get_to_z)
print(f"Part 2: {lcm=}")
