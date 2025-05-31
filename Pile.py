class Pile:
    cards = None
    
    def __init__(self):
        self.cards = []
    
    def sort(self):
        self.cards.sort()
    
    def add(self, card):
        self.cards.append(card)
    
    def length(self):
        return len(self.cards)
    
    def isEmpty(self):
        return len(self.cards) == 0
    
    def getCardFromIndex(self, index):
        return self.cards[index]
    
    def __str__(self):
        x = "Pile: "
        for card in self.cards:
            x += f"{card} "
        return x