from functools import total_ordering
from collections import Counter


@total_ordering
class Hand(object):
    card_ranking_dict = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}

    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid

    def get_card_rank(self, card: str):
        return self.card_ranking_dict.get(card, None) or int(card)

    def find_first_diff_card_rank(self, cards_1, cards_2):
        for card_1, card_2 in zip(cards_1, cards_2):
            if card_1 != card_2:
                return (self.get_card_rank(card_1), self.get_card_rank(card_2))
        return (0, 0)  # am not sure what None < None would eval to?

    @property
    def type_rank(self):
        cards = self.cards

        n_unique_cards = len(set(cards))

        if n_unique_cards == 5:  # High card
            rank = 1
        elif n_unique_cards == 4:
            rank = 2  # One pair
        elif n_unique_cards == 3:
            card_counts = Counter(cards)
            if set(card_counts.values()) == {1, 2, 2}:  # Two Pair
                rank = 3
            elif set(card_counts.values()) == {3, 1, 1}:  # Three of a kind
                return 4
            else:
                raise ValueError
        elif n_unique_cards == 2:
            card_counts = Counter(cards)
            if set(card_counts.values()) == {2, 3}:  # Full House
                rank = 5
            elif set(card_counts.values()) == {4, 1}:  # Four of a kind
                rank = 6
            else:
                raise ValueError
        elif n_unique_cards == 1:
            rank = 7
        else:
            raise ValueError

        return rank

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        if self.type_rank < other.type_rank:
            return True
        elif self.type_rank > other.type_rank:
            return False
        else:
            first_different_cards_rank_self_other = self.find_first_diff_card_rank(
                self.cards, other.cards
            )
            return (
                first_different_cards_rank_self_other[0]
                < first_different_cards_rank_self_other[1]
            )


with open("aoc_2023\\day_7_t.txt") as f:
    hands = list(
        map(
            lambda x: Hand(x[0], int(x[1])),
            [line.strip().split(" ") for line in f.readlines()],
        )
    )

sorted_hands = sorted(hands)

ans = 0
for rank, hand in enumerate(sorted_hands, 1):
    ans += rank * hand.bid

print(f"Part 1: {ans}")


# Part 2


@total_ordering
class Hand(object):
    card_ranking_dict = {"A": 14, "K": 13, "Q": 12, "J": 0.5, "T": 10}

    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid

    def get_card_rank(self, card: str):
        return self.card_ranking_dict.get(card, None) or int(card)

    def find_first_diff_card_rank(self, cards_1, cards_2):
        for card_1, card_2 in zip(cards_1, cards_2):
            if card_1 != card_2:
                return (self.get_card_rank(card_1), self.get_card_rank(card_2))
        return (0, 0)  # am not sure what None < None would eval to?

    def improve_counts_using_jokers(self, card_counts: Counter):
        if "J" in card_counts.keys() and card_counts["J"] != 5:
            # print(f"before: {card_counts}")
            j_count = card_counts.pop("J")
            most_common_card_not_j = card_counts.most_common(1)[0][0]
            card_counts.update(most_common_card_not_j * j_count)
            # print(f"after: {card_counts}")
        return card_counts

    @property
    def type_rank(self):
        cards = self.cards

        card_counts = Counter(cards)
        card_counts = self.improve_counts_using_jokers(card_counts)

        if len(card_counts) == 5:  # High card
            rank = 1
        elif len(card_counts) == 4:
            rank = 2  # One pair
        elif len(card_counts) == 3:
            if set(card_counts.values()) == {1, 2, 2}:  # Two Pair
                rank = 3
            elif set(card_counts.values()) == {3, 1, 1}:  # Three of a kind
                return 4
            else:
                raise ValueError
        elif len(card_counts) == 2:
            if set(card_counts.values()) == {2, 3}:  # Full House
                rank = 5
            elif set(card_counts.values()) == {4, 1}:  # Four of a kind
                rank = 6
            else:
                raise ValueError
        elif len(card_counts) == 1:
            rank = 7
        else:
            raise ValueError

        return rank

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        if self.type_rank < other.type_rank:
            return True
        elif self.type_rank > other.type_rank:
            return False
        else:
            first_different_cards_rank_self_other = self.find_first_diff_card_rank(
                self.cards, other.cards
            )
            return (
                first_different_cards_rank_self_other[0]
                < first_different_cards_rank_self_other[1]
            )


with open("aoc_2023\\day_7.txt") as f:
    hands = list(
        map(
            lambda x: Hand(x[0], int(x[1])),
            [line.strip().split(" ") for line in f.readlines()],
        )
    )

sorted_hands = sorted(hands)

ans = 0
for rank, hand in enumerate(sorted_hands, 1):
    ans += rank * hand.bid

print(f"Part 2: {ans}")
# 249106176 too low 1369 new test...
