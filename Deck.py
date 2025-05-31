import random

from Card import Suits, Card


class Deck:
    cards = None
    
    def __init__(self):
        self.cards = []
        for suit in Suits:
            for value in range(1, 21):
                if value <= 10 or (suit == Suits.PAYOO and value > 10):
                    self.cards.append(Card(suit, value))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def add_card(self, card):
        self.cards.append(card)
    
    def removeLast(self):
        return self.cards.pop()
    
    def remove(self, index):
        return self.cards.remove(index)
    
    def length(self):
        return len(self.cards)
    
    def isEmpty(self):
        return len(self.cards) == 0
    
    def pop_card(self):
        return self.cards.pop()
    
    def __str__(self):
        x = ""
        if len(self.cards) == 0:
            return ""
        for card in self.cards:
            # print(card, end=" ")
            x += card.__repr__() + " "
        
        return x
