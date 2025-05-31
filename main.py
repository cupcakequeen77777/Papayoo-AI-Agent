import random
from copy import deepcopy

from Agent import Agent
from Game import Game
import matplotlib.pyplot as plt
import numpy as np
import time

def graphResults(results, title, showAll, strategies):
    newData = np.transpose(results)  # transpose results so index 0 is all player 0's rewards etc.
    plt.figure()
    plt.suptitle(title)
    plt.xlabel('Game')
    plt.ylabel('Points')
    plt.ylim(0, 250)

    # plot all players:
    if showAll:
        for i in range(len(newData)):
            l = "Player " + str(i + 1) + ", strategy " + strategies[i]
            plt.plot(newData[i], label=l)
    else:
        # plot 1 player (agent)
        plt.plot(newData[0], label="agent")

    plt.legend(loc='upper right')

    # Save plots
    fileName = title + ".png"
    plt.savefig(fileName)

def papayooRL(player_1, player_2, player_3, numGames=1000, numRounds=6, players=3):
    strategies = np.full(players, "random")  # Everyone defaults to random
    strategies[0] = player_1
    strategies[1] = player_2
    strategies[2] = player_3

    papayoo = Game(strategies, players, numRounds)
    training = True

    initialTheta = [0, 0, 0, 0, 0]  # initial theta
    thetaPopulation = np.random.rand(6, 5)
    
    # Assign each agent a Theta (used for RL strategy)
    rlAgents = []
    for i, s in enumerate(strategies):
        if s == "gene":
            rlAgents.append(i)
            papayoo.agents[i].theta = initialTheta
            papayoo.agents[i].thetaPop = thetaPopulation
    
    results, gameWins = papayoo.playPapayoo(numGames, training, rlAgents)

    # Print results
    pointsPerPlayer = np.sum(results, axis=0)
    totalPoints = numGames * 250
    avgPoints = np.divide(pointsPerPlayer, totalPoints)

    for p in range(players):
        print(f"Player {p+1}'s strategy was {strategies[p]} \tGames won: {gameWins[p]} \tPoints: {pointsPerPlayer[p]}\t % of points: {avgPoints[p]}")

    # Graph results
    results = np.array(results)
    mean = np.mean(results.reshape(-1, 1000, 3), axis=1)
    showAllPlayers = True
    graphResults(mean, "test", showAllPlayers, strategies)



if __name__ == "__main__":
    start = time.time()
    # Options: 'random', 'gene', 'manual', 'reflex'
    papayooRL("gene", "reflex", "reflex", 5000, 2, 3)
    end = time.time()
    print(f"Took {end - start:.3f} seconds")