def simple_reflex_agent(player, pile):
    action = None

    if len(pile.cards) == 0:
        # Scenario 1:
        # If leading, play the lowest value card
        lowest_card = None
        action = None

        for i, cards in enumerate(player.hand.cards):
            if lowest_card is None:
                lowest_card = cards
                action = 0
            elif cards.cardValue < lowest_card.cardValue:
                lowest_card = cards
                action = i
    else:
        # Scenario 2:
        # Play the highest value card of the suit
        # that's lower than the current played card(s)

        last_card_pile = pile.cards[len(pile.cards) - 1]

        suit = last_card_pile.suit

        highest_card = None

        for i, card in enumerate(player.hand.cards):
            if card.suit == suit: # Make sure the card follows suit
                if card.cardValue < last_card_pile.cardValue: # Compares the number of the cards.
                    if highest_card is None or card.cardValue > highest_card.cardValue:
                        highest_card = card
                        action = i

        # Scenario 3:
        # If void of the current suit, play the highest value card
        if action is None:
            for i, card in enumerate(player.hand.cards):
                if highest_card is None or card.cardValue > highest_card.cardValue:
                    highest_card = card
                    action = i

    return action