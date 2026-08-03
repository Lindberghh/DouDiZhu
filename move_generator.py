from collections import defaultdict
import Cards
import move_types
import utils

# groups a hand of cards by rank

def group_by_rank(hand: list[Cards.Card]) -> dict[Cards.Rank, list[Cards.Card]]:
    groups = defaultdict(list)

    for card in hand:
        groups[card.rank].append(card)

    return dict(groups)

# Generates list of available Single moves given a hand

def generate_singles(hand):
    moves = []

    for card in hand:
        moves.append(
            move_types.Move(
                move_types.MoveType.SINGLE,
                [card],
                card.rank
            )
        )

    return moves

# Generates list of available Pair moves given a hand

def generate_pairs(hand):
    moves = []

    groups = group_by_rank(hand)

    for rank, cards in groups.items():
        if len(cards) >= 2:
            moves.append(
                Move(
                    MoveType.PAIR,
                    cards[:2],
                    rank
                )
            )

    return moves

# Generates list of available Triple moves given a hand

def generate_triples(hand):
    moves = []

    groups = group_by_rank(hand)

    for rank, cards in groups.items():
        if len(cards) >= 3:
            moves.append(
                move_types.Move(
                    move_types.MoveType.TRIPLE,
                    cards[:3],
                    rank
                )
            )

    return moves

# Generates list of available Bombs moves given a hand

def generate_bombs(hand):
    moves = []

    groups = group_by_rank(hand)

    for rank, cards in groups.items():
        if len(cards) == 4:
            moves.append(
                move_types.Move(
                    move_types.MoveType.BOMB,
                    cards,
                    rank
                )
            )

    return moves

# Generates list of available Rocket moves given a hand

def generate_rocket(hand):
    groups = group_by_rank(hand)

    if (
        Cards.Rank.BLACK_JOKER in groups and
        Cards.Rank.RED_JOKER in groups
    ):
        return [
            move_types.Move(
                move_types.MoveType.ROCKET,
                [
                    groups[Cards.Rank.BLACK_JOKER][0],
                    groups[Cards.Rank.RED_JOKER][0]
                ],
                Cards.Rank.RED_JOKER
            )
        ]

    return []

# Generates list of available Triple with Singles moves given a hand

def generate_triple_with_single(hand):
    moves = []

    groups = group_by_rank(hand)

    triples = [
        (rank, cards)
        for rank, cards in groups.items()
        if len(cards) >= 3
    ]

    for triple_rank, triple_cards in triples:

        for card in hand:

            if card.rank == triple_rank:
                continue

            moves.append(
                move_types.Move(
                    move_types.MoveType.TRIPLE_WITH_SINGLE,
                    triple_cards[:3] + [card],
                    triple_rank
                )
            )

    return moves

# Generates list of available Triple with Pair moves given a hand

def generate_triple_with_pair(hand):
    moves = []

    groups = group_by_rank(hand)

    triples = [
        (rank, cards)
        for rank, cards in groups.items()
        if len(cards) >= 3
    ]

    pairs = [
        (rank, cards)
        for rank, cards in groups.items()
        if len(cards) >= 2
    ]

    for triple_rank, triple_cards in triples:

        for pair_rank, pair_cards in pairs:

            if pair_rank == triple_rank:
                continue

            moves.append(
                move_types.Move(
                    move_types.MoveType.TRIPLE_WITH_PAIR,
                    triple_cards[:3] + pair_cards[:2],
                    triple_rank
                )
            )

    return moves

# Generates list of available Straights moves given a hand

def generate_straights(hand):
    moves = []

    groups = group_by_rank(hand)

    ranks = sorted(
        r for r in groups
        if r.value < Cards.Rank.TWO.value
    )

    start = 0

    while start < len(ranks):

        end = start

        while (
            end + 1 < len(ranks)
            and ranks[end + 1] == ranks[end] + 1
        ):
            end += 1

        run = ranks[start:end+1]

        if len(run) >= 5:

            for length in range(5, len(run)+1):

                for i in range(len(run)-length+1):

                    subset = run[i:i+length]

                    cards = [
                        groups[r][0]
                        for r in subset
                    ]

                    moves.append(
                        move_types.Move(
                            move_types.MoveType.STRAIGHT,
                            cards,
                            subset[0]
                        )
                    )

        start = end + 1

    return moves
