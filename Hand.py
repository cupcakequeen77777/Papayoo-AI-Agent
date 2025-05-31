from Card import Card, Suits


class Hand:
    cards = None

    def __init__(self):
        self.cards = []

    def sort(self):
        self.cards.sort()

    def add(self, card):
        self.cards.append(card)

    def play(self, index):
        return self.cards.pop(index)

    def length(self):
        return len(self.cards)

    def isEmpty(self):
        return len(self.cards) == 0

    def get(self):
        return self.cards

    def getCardAtIndex(self, index):
        return self.cards[index]

    def getCard(self, otherCard):
        for index, card in enumerate(self.cards):
            if card == otherCard:
                return index
        return -1

    def make_Card(self, suit, value):
        card = Card(suit, value)
        return card

    def cardFromString(self, strCard):
        suit = ""
        if strCard[0].upper() == 'C':
            suit = Suits.CLUB
        elif strCard[0].upper() == 'S':
            suit = Suits.SPADE
        elif strCard[0].upper() == 'H':
            suit = Suits.HEART
        elif strCard[0].upper() == 'D':
            suit = Suits.DIAMOND
        elif strCard[0].upper() == 'P':
            suit = Suits.PAYOO
        cardValue = int(strCard[1:])

        return self.make_Card(suit, cardValue)

    def contains(self, otherCard):
        for card in self.cards:
            if card == otherCard:
                return True

        return False

    def __str__(self):
        x = ""
        for card in self.cards:
            x += f"{card} "
        return x

    def __repr__(self):
        x = "Hand: "
        for card in self.cards:
            x += f"{card} "
        return x
