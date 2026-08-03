from enum import Enum, auto
import Cards
import utils
from collections import Counter

class MoveType(Enum):
    PASS = auto()

    SINGLE = auto()
    PAIR = auto()
    TRIPLE = auto()

    TRIPLE_WITH_SINGLE = auto()
    TRIPLE_WITH_PAIR = auto()

    STRAIGHT = auto()
    STAIRCASE = auto()

    AIRPLANE = auto()
    AIRPLANE_WITH_SINGLES = auto()
    AIRPLANE_WITH_PAIRS = auto()

    FOUR_WITH_TWO_SINGLES = auto()
    FOUR_WITH_TWO_PAIRS = auto()

    BOMB = auto()
    ROCKET = auto()

    INVALID = auto()


from dataclasses import dataclass

@dataclass(frozen=True)
class Move:
    move_type: MoveType
    cards: list[Cards.Card]
    primary_rank: Cards.Rank


