import math

from Card import Card
from Game import Game
from bigtree import Node, hprint_tree
import matplotlib.pyplot as plt
import numpy as np
import time


def playPapayoo():
    papayoo = Game()
    results = papayoo.play()
    print(f"Results of each round: {results}")


def treeTest1():

    root1 = Node("-")
    a1 = Node("P5", parent=root1, score=[])
    a2 = Node("P3", parent=root1, score=[])
    b1 = Node("P7", parent=a1, score=[])
    b2 = Node("P4", parent=a1, score=[])
    b3 = Node("P7", parent=a2, score=[])
    b4 = Node("P4", parent=a2, score=[])
    c1 = Node("P2", parent=b1, score=[])
    c2 = Node("P1", parent=b1, score=[])
    c5 = Node("P2", parent=b3, score=[])
    c6 = Node("P1", parent=b3, score=[])
    c7 = Node("P2", parent=b4, score=[])
    c8 = Node("P1", parent=b4, score=[])

    hprint_tree(root1)
    a1.score = [0, 0, 2]
    root1.show(attr_list=["score"])
    print(a1.describe()[4])

    # # find path from c6 to root2
    # print(list(c6.ancestors))

def treeTest2():
    root2 = Node("-")
    a1 = Node("3C", parent=root2, score=0)
    a2 = Node("5H", parent=root2)
    b1 = Node("7C", parent=a1)
    b3 = Node("7C", parent=a2)
    b4 = Node("3P", parent=a2)
    c1 = Node("2S", parent=b1)
    c2 = Node("1D", parent=b1)
    c5 = Node("2S", parent=b3)
    c6 = Node("1D", parent=b3)
    c7 = Node("2S", parent=b4)
    c8 = Node("1D", parent=b4)

    root2.append(Node("j"))
    root2.show(attr_list=["score"])

    # print(list(c6.ancestors))

def createTree():
    # possibleCards = {"P1": [Card("P", )]}
    # possibleCards = {"P1": [3, 5], "P2": [7, 4], "P3": [2, 1]}
    possibleCards = [["3C", "5H"], ["7C", "3P"],["2S", "1D"]]
    cardsLeft = 2
    tree = []

    root = Node("-")
    currentNode = root
    level = 0
    for playerCards in possibleCards:
        for card in playerCards:
            for c in range(0, int(math.pow(cardsLeft, level))):
                print(card)
                # newNode = Node("P" + str(card))
                # currentNode.append(newNode)

        level += 1
        # currentNode = newNode

    n_level = 1
    for playerCards in possibleCards:
        for i in range(cardsLeft ** n_level):
            for cards in playerCards:
                print(cards)
                currentNode.extend([Node(cards), Node(cards)])

    root.show()

def alphaBetaTesting():
    root1 = Node("-")
    a1 = Node("P5", value = 5, suit = "P", parent=root1, score=[])
    a2 = Node("P3", value = 3, suit = "P", parent=root1, score=[])
    b1 = Node("P7", value = 7, suit = "P", parent=a1, score=[])
    b2 = Node("P4", value = 4, suit = "P", parent=a1, score=[])
    b3 = Node("P7", value = 7, suit = "P", parent=a2, score=[])
    b4 = Node("P4", value = 4, suit = "P", parent=a2, score=[])
    c1 = Node("P2", value = 2, suit = "P", parent=b1, score=[])
    c2 = Node("P1", value = 1, suit = "P", parent=b1, score=[])
    c3 = Node("P2", value = 2, suit = "P", parent=b2, score=[])
    c4 = Node("P1", value = 1, suit = "P", parent=b2, score=[])
    c5 = Node("P2", value = 2, suit = "P", parent=b3, score=[])
    c6 = Node("P1", value = 1, suit = "P", parent=b3, score=[])
    c7 = Node("P2", value = 2, suit = "P", parent=b4, score=[])
    c8 = Node("P1", value = 1, suit = "P", parent=b4, score=[])

    print("Here")
    print(a1.describe()[4])
    for leaf in root1.leaves:
        leaf.score = [0, 0, 0]
        points = 0
        # print(list(leaf.ancestors))
        print((str(points) + "+"), end="")

        highestValue = 0
        playerTakingTrick = 0
        count = 0

        for ancestor in leaf.ancestors:
            ancestor.score = [0, 0, 0]

            if ancestor.node_name != "-":
                v = ancestor.get_attr("value")
                print(f"v: {v}")
                if highestValue < v:
                    playerTakingTrick = count
                    highestValue = v
                points += v

                print((str(v) + "+"), end="")
            count += 1
        points += leaf.get_attr("value")
        if highestValue < leaf.get_attr("value"):
            print(f"player taking trick: {playerTakingTrick}")
            playerTakingTrick = 2
            highestValue = leaf.get_attr("value")

        print("=" + (str(points)))
        print(f"highest value: {highestValue}")
        print(f"player taking trick: {playerTakingTrick}")
        leaf.score[playerTakingTrick]= points
    root1.show(attr_list=["score"])

    print("Here")


# def min_value_alphabeta(state, alpha, beta):
#     if state is terminal:
#         return score(state)
#
#     values = []
#     for a in get_actions(state):
#         v = max_value_alphabeta(state.get_child(a), alpha, beta)
#         values.append(v)
#
#         if (v <= beta):
#             return v
#         beta = min(beta, v)
#
#     value = min(values)
#     action = argmin(values)
#
#     return value, action





def graphResults(results, title):
    newData = np.transpose(results)  # transpose results so index 0 is all player 0's rewards etc.
    plt.figure()
    plt.suptitle(title)
    plt.xlabel('Round #')
    plt.ylabel('Points')

    # plot 1 player (agent)
    plt.plot(newData[0], label="agent")

    # plot all players:
    # for i in range(len(newData)):
    #     l = "Player " + str(i+1)
    #     plt.plot(newData[i], label=l)

    plt.legend(loc='lower right')

    # Save plots
    fileName = title + ".png"
    plt.savefig(fileName)


if __name__ == "__main__":
    # playPapayoo()
    # treeTest1()
    # createTree()
    alphaBetaTesting()

    # start = time.time()
    #
    # end = time.time()
    # print(f"Took {end - start:3f} seconds")