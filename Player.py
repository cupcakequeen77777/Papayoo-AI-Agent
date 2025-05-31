from Hand import Hand


class Player:
    hand = None
    name = None

    def __init__(self, name):
        self.hand = Hand()
        self.name = name

    def draw(self, deck):
        self.hand.add(deck.pop_card())

    def play(self, index):
        return self.hand.cards.pop(index)

    def numberCards(self):
        return self.hand.length()

    def __str__(self):
        return f"Player {self.name + 1} Hand: {self.hand}"
        # return f"Player {self.name + 1}\n     Hand: {self.hand}"
