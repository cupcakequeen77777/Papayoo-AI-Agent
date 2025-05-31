from enum import Enum


class Suits(Enum):
    CLUB = 0
    SPADE = 1
    HEART = 2
    DIAMOND = 3
    PAYOO = 4

    def __str__(self):
        if self == Suits.CLUB:
            return 'C'
        if self == Suits.SPADE:
            return 'S'
        if self == Suits.HEART:
            return 'H'
        if self == Suits.DIAMOND:
            return 'D'
        if self == Suits.PAYOO:
            return 'P'


class Card:
    suit = None
    cardValue = None

    def __init__(self, suit, value):
        self.suit = suit
        self.cardValue = value

    def __str__(self):
        return f"{self.suit}{self.cardValue}"

    def __repr__(self):
        return f"{self.suit}{self.cardValue}"

    def __eq__(self, otherCard):
        if otherCard.suit == self.suit and otherCard.cardValue == self.cardValue:
            return True
        return False


    def __ne__(self, other):
        return not self.__eq__(other)

    # convert a card object to a string with the first index being a number representing the suit and the remaining 1-2
    # indices being the rank of the card
    def cardToCode(self):
        return str(self.suit.value) + str(self.cardValue)
