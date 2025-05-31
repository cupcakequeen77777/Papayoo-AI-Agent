from copy import deepcopy

import numpy as np
import random
from Card import Suits


class Agent:
    state = None
    player = None
    name = None
    bestTheta = []
    gameAbilities = []
    ability = None  # keep track of how well the agent played in each round
    bestSkill = float('inf')  # want small skill
    theta = None
    agentsCardsSum = 0
    thetaPop = []
    thetaAbilities = []

    def __init__(self, player, name):
        self.player = player
        self.name = name

    # create the array representation of the state given the hand of the agent
    # all cards are 0 because they haven't been seen yet, except for cards in the agents hand which are 2
    # and invalid cards (ex. 12 of clubs) are -1
    def createInitialState(self):
        playersCards = self.player.hand.get()
        playerCardsIndexed = []

        # convert all cards in hand to ints for ease of comparison when setting up the state
        for x in playersCards:
            val = x.cardToCode()
            playerCardsIndexed.append(val)

        state = np.zeros((5, 20))  # FIXME: magic numbers (number of suits x rank)

        # loop through all cards
        for i, suit in enumerate(Suits):
            for j in range(1, 21):
                curCard = str(i) + str(j)
                # invalid card
                if j > 10 and suit != Suits.PAYOO:
                    state[i][j - 1] = -1
                # card in players hand
                if curCard in playerCardsIndexed:
                    state[i][j - 1] = 2

        return state

    def updateState(self):
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] == 3:
                    self.state[i][j] = 1

    # return a list of indices representing the cards in the players hand that can legally be played, based on the suit that was led
    def getValidActions(self, suitLed):
        valid_card_indices = []
        counter = 0

        for index, card in enumerate(self.player.hand.cards):
            counter += 1
            # if the card matches the suit it can be played
            if card.suit == suitLed:
                valid_card_indices.append(index)

        # can't follow suit/no suit to follow yet, all actions are valid
        if valid_card_indices == []:
            valid_card_indices = list(range(0, counter))

        return valid_card_indices

    # chose best action based on state, available actions and theta
    def playSmart(self, suitLed, actions):
        maxStateVal = - float('inf')
        bestAction = -1
        known = None

        for i in range(len(actions)):
            action = self.player.hand.getCardAtIndex(i)

            throwing = True  # player throwing a card and can't win trick
            if suitLed is None or suitLed == action.suit:
                throwing = False  # player leading or following suit and could win the trick

            # get the values of the features for the given state action pair
            featureVals = np.array(self.calcFeatureValues(action, throwing, known))
            known = featureVals[1:]

            # calculate the value of the state based on the feature values and theta
            stateVal = np.sum(featureVals * self.theta)

            # if state value is better than previously calculated state values then update the best action
            if stateVal > maxStateVal:
                maxStateVal = stateVal
                bestAction = i

        card = self.player.play(bestAction)

        return card

    # calculate the values of all features given the state action pair
    def calcFeatureValues(self, action, throwing, known):
        curAction = action.cardToCode()
        actionSuit = int(curAction[0])
        actionValue = int(curAction[1:]) - 1

        sumOfCardsInHand = 0
        biggestCard = 0
        smallestCard = 0
        remainingOfVoid = 0
        activeCards = []

        # state feature values are unknown
        if known is None:
            # loop through all cards
            for i in range(len(self.state)):
                void = True
                for j in range(len(self.state[i])):

                    # card is in hand
                    if self.state[i][j] == 2:
                        void = False  # not void of this suit

                        # update sum of the ranks of cards in hand
                        sumOfCardsInHand += j + 1

                        # check if this is the largest remaining card of the suit
                        largest = True
                        for k in range(j + 1, len(self.state[i])):
                            if self.state[i][k] == 0:
                                largest = False
                                break
                        if largest:
                            biggestCard += 1

                        # check if this is the smallest remaining card of the suit
                        smallest = True
                        for k in range(j):
                            if self.state[i][k] == 0:
                                smallest = False
                                break
                        if smallest:
                            smallestCard += 1

                    # card is active
                    if self.state[i][j] == 3:
                        activeCards.append((i, j))

                # agent has no cards of the current suit
                if void:
                    for k in range(len(self.state[i])):
                        # other players still have cards of that suit, giving the agent an advantage because it can easily throw cards
                        if self.state[i][k] == 0:
                            remainingOfVoid += 1
        else:
            sumOfCardsInHand = known[0]
            biggestCard = known[1]
            smallestCard = known[2]
            remainingOfVoid = known[3]

        # calculate probability of winning the trick
        if throwing:  # can't win trick
            probWinning = 0
        else:
            largerCards = 0
            totalCards = 0
            cantWin = False
            for k in range(len(self.state[actionSuit])):
                # card of the action suit that hasn't been seen yet
                if self.state[actionSuit][k] == 0:
                    totalCards += 1
                    if k > actionValue:
                        largerCards += 1

                # a higher card is active, player won't win
                if self.state[actionSuit][k] == 3 and k > actionValue:
                    cantWin = True
                    break

            # higher card is currently active, player won't win
            if cantWin:
                probWinning = 0
            # no other cards of this suit, player will win
            elif totalCards == 0:
                probWinning = 1
            # calculate probability based on total cards still remaining of the suit, and larger cards of the suit still remaining
            else:
                probWinning = 1 - (largerCards / totalCards)

        f1 = probWinning
        f2 = sumOfCardsInHand
        f3 = biggestCard
        f4 = smallestCard
        f5 = remainingOfVoid

        # return the feature values
        return [f1, f2, f3, f4, f5]

    # calculate the sum of the ranks of all cards in the agents hand to decide how good its hand is
    # a hand of small numbers is better because it's harder to win tricks
    def sumOfCards(self):
        agentsCardsSum = 0
        for c in self.player.hand.cards:
            agentsCardsSum += c.cardValue
        self.agentsCardsSum = agentsCardsSum

    # # mutate the given theta by adding/subtracting a random value between 0 and 0.5 from a random index of the given theta
    # def mutate1(self):
    #     newTheta = deepcopy(self.bestTheta)
    #     index = random.randint(0, len(self.bestTheta) - 1)
    #     amount = random.uniform(0, 0.5)
    #     addOrSub = random.randint(0, 1)
    #     if addOrSub == 0:
    #         newTheta[index] += amount
    #     else:
    #         newTheta[index] -= amount
    #     self.theta = newTheta

    # mutate the given theta by adding/subtracting a random value between 0 and 0.5 from a random index of the given theta
    def mutate(self, theta):
        newTheta = deepcopy(theta)
        index = random.randint(0, len(theta) - 1)
        amount = random.uniform(0, 0.5)
        addOrSub = random.randint(0, 1)
        if addOrSub == 0:
            newTheta[index] += amount
        else:
            newTheta[index] -= amount
        return newTheta

    # def checkCurrentTheta(self):
    #     # get average skill over the past 5 games and reset it
    #     avgSkill = np.mean(self.gameAbilities)
    #     self.gameAbilities = []

    #     # if skill was better than current best then save the current theta
    #     if avgSkill < self.bestSkill:
    #         self.bestTheta = deepcopy(self.theta)
    #         self.bestSkill = avgSkill

    def checkThetas(self):
        abilities = self.thetaAbilities
        thetas = self.thetaPop

        bestAbility = np.argmin(abilities)

        if abilities[bestAbility] < self.bestSkill:
            self.bestTheta = thetas[bestAbility]
            self.bestSkill = abilities[bestAbility]

        self.thetaAbilities = []

    # Create new thetas by combining thetas with the smallest abilities
    def createNewThetas(self, thetas, abilities):  # Genetic Operator
        # Reverse probability and mormalize it so that it sums to one
        reverse_ability = -(abilities - 1)
        sum_ability = np.sum(reverse_ability)
        normalize_ability = reverse_ability / sum_ability

        # Picks parent 1 and parent 2
        parent_1, parent_2 = np.random.choice(6, 2, p=normalize_ability, replace=False)
        i = random.randint(1, 4)
        offspring1 = np.concatenate([thetas[parent_1][:i], thetas[parent_2][i:]])

        parent_1, parent_2 = np.random.choice(6, 2, p=normalize_ability, replace=False)
        i = random.randint(1, 4)
        offspring2 = np.concatenate([thetas[parent_1][:i], thetas[parent_2][i:]])

        parent_1, parent_2 = np.random.choice(6, 2, p=normalize_ability, replace=False)
        i = random.randint(1, 4)
        offspring3 = np.concatenate([thetas[parent_1][:i], thetas[parent_2][i:]])

        # mutate new theta
        offspring1 = self.mutate(offspring1)
        offspring2 = self.mutate(offspring2)
        offspring3 = self.mutate(offspring3)

        return offspring1, offspring2, offspring3

    def __str__(self):
        return f"{self.name}"