from dataclasses import dataclass
from enum import IntEnum, auto
import random


class Rank(IntEnum):
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    TWO = 15
    BLACK_JOKER = 16
    RED_JOKER = 17


@dataclass(frozen=True)
class Card:
    id: int          # Unique identifier (0–53)
    rank: Rank

    def __str__(self):
        names = {
            Rank.THREE: "3",
            Rank.FOUR: "4",
            Rank.FIVE: "5",
            Rank.SIX: "6",
            Rank.SEVEN: "7",
            Rank.EIGHT: "8",
            Rank.NINE: "9",
            Rank.TEN: "10",
            Rank.JACK: "J",
            Rank.QUEEN: "Q",
            Rank.KING: "K",
            Rank.ACE: "A",
            Rank.TWO: "2",
            Rank.BLACK_JOKER: "BJ",
            Rank.RED_JOKER: "RJ",
        }
        return names[self.rank]

class Deck:

    def __init__(self):
        self.cards = []
        uid = 0

        normal_ranks = [
            Rank.THREE,
            Rank.FOUR,
            Rank.FIVE,
            Rank.SIX,
            Rank.SEVEN,
            Rank.EIGHT,
            Rank.NINE,
            Rank.TEN,
            Rank.JACK,
            Rank.QUEEN,
            Rank.KING,
            Rank.ACE,
            Rank.TWO,
        ]

        # Four copies of every normal rank
        for rank in normal_ranks:
            for _ in range(4):
                self.cards.append(Card(uid, rank))
                uid += 1

        # Two jokers
        self.cards.append(Card(uid, Rank.BLACK_JOKER))
        uid += 1

        self.cards.append(Card(uid, Rank.RED_JOKER))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def deal(self, players=3):
        """
        Returns:
            hands: list[list[Card]]
            landlord_cards: list[Card]
        """
        self.shuffle()

        hands = [[] for _ in range(players)]

        # Deal 17 cards to each player
        for _ in range(17):
            for player in hands:
                player.append(self.draw())

        landlord_cards = [self.draw() for _ in range(3)]

        return hands, landlord_cards
