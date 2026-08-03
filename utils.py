import Cards
from collections import Counter
import move_types

# Rule Functions

# Counts number of cards per ranks

def rank_counts(cards):
    return Counter(card.rank for card in cards)

# finds consecutive cards for straights and staircases

def consecutive(ranks):
    values = sorted(r.value for r in ranks)

    return all(
        values[i] + 1 == values[i + 1]
        for i in range(len(values) - 1)
    )

# determines length of straight/staircase

def straight_ranks(ranks):
    return all(rank.value < Cards.Rank.TWO.value for rank in ranks)


def identify(cards):
    # identify card ranks

    cards = sorted(cards, key=lambda c: c.rank)

    n = len(cards)

    counts = rank_counts(cards)

    freq = sorted(counts.values())

    # Singles

    if n == 1:
        return move_types.Move(
            move_types.MoveType.SINGLE,
            cards,
            cards[0].rank
        )

    # Pair and Rocket

    if n == 2:

        if cards[0].rank == Cards.Rank.BLACK_JOKER and cards[1].rank == Cards.Rank.RED_JOKER:
            return move_types.Move(
                move_types.MoveType.ROCKET,
                cards,
                Cards.Rank.RED_JOKER
            )

        if len(counts) == 1:
            return move_types.Move(
                move_types.MoveType.PAIR,
                cards,
                cards[0].rank
            )

    # Triple

    if n == 3 and freq == [3]:
        return move_types.Move(
            move_types.MoveType.TRIPLE,
            cards,
            cards[0].rank
        )

    # Bomb

    if n == 4 and freq == [4]:
        return move_types.Move(
            move_types.MoveType.BOMB,
            cards,
            cards[0].rank
        )

    # Triple + Single

    if n == 4 and freq == [1, 3]:
        triple = next(
            rank
            for rank, count in counts.items()
            if count == 3
        )

        return move_types.Move(
            move_types.MoveType.TRIPLE_WITH_SINGLE,
            cards,
            triple
        )

    # Triple + Pair

    if n == 5 and freq == [2, 3]:
        triple = next(
            rank
            for rank, count in counts.items()
            if count == 3
        )

        return move_types.Move(
            move_types.MoveType.TRIPLE_WITH_PAIR,
            cards,
            triple
        )

    # Straight

    if (
            n >= 5
            and all(v == 1 for v in counts.values())
            and straight_ranks(counts.keys())
            and consecutive(counts.keys())
    ):
        return move_types.Move(
            move_types.MoveType.STRAIGHT,
            cards,
            min(counts.keys())
        )

    # Staircase

    if (
            n >= 6
            and n % 2 == 0
            and all(v == 2 for v in counts.values())
            and straight_ranks(counts.keys())
            and consecutive(counts.keys())
    ):
        return move_types.Move(
            move_types.MoveType.STAIRCASE,
            cards,
            min(counts.keys())
        )

    # Invalid Move

    return move_types.Move(
        move_types.MoveType.INVALID,
        cards,
        Cards.Rank.THREE
    )

# Compares moves, returns True if move b beats move a, else False

def beats(a: move_types.Move, b: move_types.Move):

    if a.move_type == move_types.MoveType.ROCKET:
        return True

    if a.move_type == move_types.MoveType.BOMB and b.move_type != move_types.MoveType.BOMB:
        return True

    if a.move_type != b.move_type:
        return False

    return a.primary_rank > b.primary_rank

# Generates a list of Card objects given a list of Cards (11 = Jack, 12 = Queen, 13 = King, 14 = ACE, 15 = TWO, 16 = BJ, 17 = RJ)

def card_list_generator(card_list):

    res = []
    for i, card in enumerate(card_list):
        res.append(Cards.Card(i, Cards.Rank(card)))

    return res
