import itertools as it
from random import randint

import numpy as np
import Card
from Agent import Agent
from Card import Suits
from Deck import Deck
from Hand import Hand
from Pile import Pile
from Player import Player
from Simple_Reflex_Agent import simple_reflex_agent

import random
from copy import deepcopy

class Game:
    def __init__(self, strategies, numberPlayers: int = 3, rounds: int = 2):
        self.numberPlayers = numberPlayers
        self.startPlayer = randint(0, self.numberPlayers - 1)
        self.rounds = rounds
        self.strategies = strategies

        # Initialize the players
        self.players = []
        for i in range(numberPlayers):
            self.players.append(Player(i))

        self.currentPlayer = self.startPlayer
        self.dice = None
        self.deck = None
        self.numberSuits = 5
        self.agents = []
        for i in range(0, self.numberPlayers):
            self.agents.append(Agent(self.players[i], "agent" + str(i + 1)))  # NOTE: added

    def dealCards(self):
        while not self.deck.isEmpty() and self.deck.length() >= self.numberPlayers:
            for player in self.players:
                if self.deck.isEmpty():
                    break
                player.draw(self.deck)

        # Sort player hands by suit and value
        for player in self.players:
            player.hand.cards.sort(key=lambda card: (card.suit.value, card.cardValue))

    # return a list of indices representing the cards in the players hand that can legally be played, based on the suit that was led
    def getValidActions(self, player, suitLed):
        valid_card_indices = []
        counter = 0

        for index, card in enumerate(player.hand.cards):
            counter += 1
            # if the card matches the suit it can be played
            if card.suit == suitLed:
                valid_card_indices.append(index)

        # can't follow suit/no suit to follow yet, all actions are valid
        if valid_card_indices == []:
            valid_card_indices = list(range(0, counter))

        return valid_card_indices

    # Play a card manually
    def manual_action(self, player, actions):
        playableCards = Hand()
        for action in actions:
            playableCards.add(player.hand.getCardAtIndex(action))

        print(f"Hand: {player.hand}")
        print(f"Playable Cards: {playableCards}")
        card = input("Pick a card to play: ")
        newCard = player.hand.cardFromString(card)
        print(f"newCard: {newCard}")
        playerAction = -1
        if playableCards.contains(newCard):
            playerAction = player.hand.getCard(newCard)
            print(f"playerAction: {playerAction}")

        while playerAction == -1:
            card = input("Invalid card. Please play a valid card: ")
            newCard = player.hand.cardFromString(card)
            print(f"newCard: {newCard}")
            if playableCards.contains(newCard):
                playerAction = player.hand.getCard(newCard)
                print(f"playerAction: {playerAction}")
        return playerAction

    # Genetic Algorithm
    def playPapayoo(self, games, training, rlAgents) -> list[list[int]]:
        results = []
        totalPoints = 0
        gameWins = np.zeros(self.numberPlayers)
        curTheta = 0
        
        # play multiple games
        for g in range(games):
            
            # Every other game try the next theta in the population (if training)
            if training and len(rlAgents) > 0 and (g + 1) % 2 == 1:
                learningAgent = rlAgents[0]
                self.agents[learningAgent].theta = self.agents[learningAgent].thetaPop[curTheta]
                curTheta += 1
            
            gamePoints = np.zeros(self.numberPlayers)
            
            for a in rlAgents:
                agent = self.agents[a]
                # ability keeps track of how well the agent played in each round based on their hand
                self.agents[a].ability = [[] for _ in range(self.rounds)]

            for r in range(self.rounds):
                self.deck = Deck()
                self.deck.shuffle()
                self.dealCards()
                totalPoints = [0 for _ in range(self.numberPlayers)]
                self.dice = Suits(randint(0, 3))
                # print(f"Dice value is {self.dice}") # Uncomment if manual player

                # a hand of small numbers is better because it's harder to win tricks
                for a in rlAgents:
                    self.agents[a].sumOfCards()
                    self.agents[a].state = self.agents[a].createInitialState()

                while self.roundNotOver():
                    winner, trick_points = self.turn()  # all player play a card
                    totalPoints[winner] += trick_points
                    gamePoints[winner] += trick_points

                # determine how good the agent played based on how many points it got and how good the hand was
                for a in rlAgents:
                    agent = self.agents[a]
                    agent.ability[r].append(totalPoints[a] / (250 + agent.agentsCardsSum))

            # Player with the fewest points wins the game
            gameWins[np.argmin(gamePoints)] += 1
            # print(f"Player {np.argmin(gamePoints) + 1} won the game")

            # get average ability for the game over all rounds
            for a in rlAgents:
                # self.agents[a].gameAbilities.append(np.mean(self.agents[a].ability))
                self.agents[a].thetaAbilities.append(np.mean(self.agents[a].ability))

            # save results at the end of the game
            results.append(totalPoints)

            # every 12 games try a different theta (if training)
            if training and (g + 1) % 12 == 0 and len(rlAgents) > 0:
                # Only first RL Agent gets to learn and update its Theta
                learningAgent = rlAgents[0]

                # Get the abilities of the current thetas by averaging over the 2 games it played with each theta
                curAbilities = np.reshape(self.agents[learningAgent].thetaAbilities, (6, 2))
                curAbilities = np.mean(curAbilities, axis=1)
                self.agents[learningAgent].thetaAbilities = curAbilities

                # Create new thetas using the genetic operator (curAbilities is the fitness value)
                newThetas = self.agents[learningAgent].createNewThetas(self.agents[learningAgent].thetaPop, curAbilities)

                # Test the new thetas by playing games to get their accuracies (ie. fitness value)
                accuracies = self.testNewThetas(self.agents[learningAgent], learningAgent, newThetas, rlAgents)

                allThetas = np.concatenate([newThetas, self.agents[learningAgent].thetaPop])
                allAccuracies = np.concatenate([accuracies, curAbilities])

                # Shrink population based on thetas with worst (highest) accuracies
                smallerPop = self.deleteBadTheta(allThetas, allAccuracies)

                self.agents[learningAgent].thetaPop = smallerPop

                # saves the best theta for future reference
                self.agents[learningAgent].checkThetas()
                
                # Reset variables
                curTheta = 0
                
                if (g + 1) % 1000 == 0:
                    print(f"Agent: {self.agents[learningAgent].name}")
                    print(f"Best current theta: {self.agents[learningAgent].bestTheta}")
                    print(f"Best current accuracy: {self.agents[learningAgent].bestSkill}")

                # self.agents[learningAgent].checkCurrentTheta()
                # self.agents[learningAgent].mutate1() #CHECK IF NEEDED!


        if training and len(rlAgents) > 0:
            # Only first RL Agent was learning
            learningAgent = rlAgents[0]

            print(f"Agent: {self.agents[learningAgent].name}")
            print(f"Best current theta: {self.agents[learningAgent].bestTheta}")
            print(f"Best current accuracy: {self.agents[learningAgent].bestSkill}")

            print(f"Final Theta population: \n{self.agents[learningAgent].thetaPop}")
        
        return results, gameWins

    def roundNotOver(self):
        # round is over when players no longer have cards in their hand
        return len(self.players[0].hand.cards) > 0

    def testNewThetas(self, agent, id, thetas, rlAgents):
        accuracies = []

        for t in thetas:
            # play 2 games with each theta to calculate ability
            agent.theta = t
            gameAccuracy = []
            for g in range(2):
                agent.ability = [[] for _ in range(self.rounds)]

                for r in range(self.rounds):
                    self.deck = Deck()
                    self.deck.shuffle()
                    self.dealCards()
                    totalPoints = [0 for _ in range(self.numberPlayers)]
                    self.dice = Suits(randint(0, 3))

                    # a hand of small numbers is better because it's harder to win tricks
                    for a in rlAgents:
                        self.agents[a].sumOfCards()
                        self.agents[a].state = self.agents[a].createInitialState()

                    while self.roundNotOver():
                        winner, trick_points = self.turn()  # all player play a card
                        totalPoints[winner] += trick_points

                    # determine how good the agent played based on how many points it got and how good the hand was
                    agent.ability[r].append(totalPoints[id] / agent.agentsCardsSum)
                gameAccuracy.append(np.mean(agent.ability))
            accuracies.append(np.mean(gameAccuracy))

        return accuracies

    # Deletes some thetas
    def deleteBadTheta(self, thetas, accuracies):
        #Normalize accuracies to sum to 1
        accuracies /= np.sum(accuracies)

        accuracies = accuracies.flatten()

        #Pick 3 random thetas and delete them
        deceased = np.random.choice(thetas.shape[0], 3, p=accuracies, replace=False)
        thetas = np.delete(thetas, deceased, axis=0)

        return thetas

    # all players play a card, based on their strategy
    def turn(self):
        points = 0
        suitLed = None
        maxVal = -1
        cardsPlayed = Pile()
        printResults = False

        # Iterate over players
        player_order = it.chain(range(self.startPlayer, self.numberPlayers), range(self.startPlayer))

        for i in player_order:
            agent = self.agents[i]
            player = agent.player

            actions = self.getValidActions(agent.player, suitLed)

            if self.strategies[i] == 'random':
                card = agent.player.play(random.choice(actions))
            elif self.strategies[i] == 'gene':
                card = agent.playSmart(suitLed, actions)
            elif self.strategies[i] == 'manual':
                printResults = True
                print(f"Player {i+1} turn\t{cardsPlayed}")
                card = agent.player.play(self.manual_action(player, actions))
                print(f"You played {card}")
            elif self.strategies[i] == 'reflex':
                card = agent.player.play(simple_reflex_agent(player, cardsPlayed))
            else:
                print(f"Unknown strategy {self.strategies[i]}, playing randomly")
                card = agent.player.play(random.choice(actions))


            if suitLed is None:
                suitLed = card.suit
                maxVal = card.cardValue

            # update state, chosen card is now active
            if self.strategies[i] == 'gene':
                x = card.cardToCode()
                suit = int(x[0])
                val = int(x[1:])
                agent.state[suit][val - 1] = 3

            cardsPlayed.add(card)

            # Update winning player and points
            if card.suit == suitLed and card.cardValue > maxVal:
                maxVal = card.cardValue
                self.startPlayer = i

            if card.suit == Suits.PAYOO:
                points += card.cardValue
            if card.suit is self.dice and card.cardValue == 7:
                points += 40

        # if there's someone playing manually, print the results for them
        if printResults:
            print(f"Player {self.startPlayer} won the trick: {cardsPlayed} with value {points}\n")

        # RL agents update state so active cards are now seen cards
        for i in range(self.numberPlayers):
            if self.strategies[i] == 'gene':
                self.agents[i].updateState()

        return self.startPlayer, points

