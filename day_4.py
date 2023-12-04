with open("day_4.txt") as f:
    cards = [line.strip() for line in f.readlines()]

total_points = 0
for card in cards:
    id_and_winning, card_numbers = card.split(" | ")

    winning_nums = {
        int(value)
        for value in id_and_winning.split(": ")[1].split(" ")
        if len(value) > 0
    }
    card_numbers = {int(value) for value in card_numbers.split(" ") if len(value) > 0}

    num_matches = len(winning_nums & card_numbers)

    if num_matches > 0:
        total_points += 2 ** (num_matches - 1)

print(f"Part 1: {total_points}")

# Part 2

match_dict = {}
cards_in_hand = {i: 1 for i in range(1, len(cards) + 1)}

for card in cards:
    id_and_winning, card_numbers = card.split(" | ")

    winning_nums = {
        int(value)
        for value in id_and_winning.split(": ")[1].split(" ")
        if len(value) > 0
    }
    card_numbers = {int(value) for value in card_numbers.split(" ") if len(value) > 0}

    num_matches = len(winning_nums & card_numbers)

    card_id = int(id_and_winning.split(": ")[0].split(" ")[-1])

    match_dict[card_id] = num_matches

for id in range(1, len(cards) + 1):
    for extra_won_id in range(id + 1, id + 1 + match_dict[id]):
        cards_in_hand[extra_won_id] += cards_in_hand[id]

total_cards = sum(cards_in_hand.values())

print(f"Part 2: {total_cards}")
