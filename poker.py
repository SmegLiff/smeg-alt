# draw poker, probably works
import random

ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
suits = ("♧", "♢", "♡", "♤")
values = ("High card", "One pair", "Two pairs", "Three of a kind", "Straight", "Flush", "Full House", "Four of a kind", "Straight Flush", "Royal Flush")
deck = []
p1 = []
p1Discarded = False
p1Value = (None, None)
p2 = []
p2Discarded = False
p2Value = (None, None)
gamechannel = ""
prioindices = []

def reset():
    global deck
    global p1, p1Discarded, p1Value
    global p2, p2Discarded, p2Value
    deck = []
    p1 = []
    p1Discarded = False
    p1Value = (None, None)
    p2 = []
    p2Discarded = False
    p2Value = (None, None)

    for value in ranks:
        for suit in suits:
            deck.append(value + suit)


def getValue(hand):
    global ranks, suits
    rank = []
    suit = []
    value = ""
    highest = ""
    indices = []
    for card in hand:
        rank.append(card[:-1])
        suit.append(card[-1:])
    for card in rank:
        indices.append(ranks.index(card))
    indices.sort()

    def isStraight():
        global prioindices
        sublist = indices[:]
        last = sublist.pop(0)
        prioindices.append(last)
        for i in sublist:
            if i - last == 1:
                last = i
                prioindices.append(last)
            else:
                prioindices = []
                return False
        prioindices = prioindices[::-1]
        return True

    def isFlush():
        global prioindices
        first = suit[0]
        for card in suit:
            if card != first:
                return False
        prioindices = indices[::-1]
        return True

    rankset = set()
    for char in rank:
        char = char.replace("J", "11")
        char = char.replace("Q", "12")
        char = char.replace("K", "13")
        char = char.replace("A", "14")
        num = int(char)
        rankset.add(num - 2)
    ranknodupe = sorted(rankset)[::-1]  # big brain moment
    if isStraight() and isFlush():
        ranksort = rank[:].sort()
        if ["10", "A", "J", "Q", "K"] == ranksort:
            value = "Royal Flush" # bruh
        else:
            value = "Straight Flush"
    elif isFlush():
        value = "Flush"
    elif isStraight():
        value = "Straight"
    else:
        if len(ranknodupe) == 2: # four of a kind or FH
            for ele in ranknodupe:
                if rank.count(ranks[ele]) == 4:
                    value = "Four of a kind"
                    prioindices.append(ele)
                elif rank.count(ranks[ele]) == 3:
                    value = "Full House"
                    prioindices.append(ele)

        elif len(ranknodupe) == 3: # two pairs, three of a kind
            for ele in ranknodupe:
                if rank.count(ranks[ele]) == 3: # 3
                    value = "Three of a kind"
                    prioindices.append(ele)
                elif rank.count(ranks[ele]) == 2:
                    value = "Two pairs"
                    prioindices.append(ele)
        elif len(ranknodupe) == 4: # one pair
            for ele in ranknodupe:
                if rank.count(ranks[ele]) == 2:
                    value = "One pair"
                    prioindices.append(ele)
        else:
            value = "High card"
        prioindices.append(sorted(rankset - set(prioindices)))

    valueindex = values.index(value)
    return (valueindex, prioindices, value)

def compareValues():
    global p1Value, p2Value
    if p1Value[0] > p2Value[0]:
        return (gamechannel, p1, p2, 1, p1Value)
    elif p1Value[0] < p2Value[0]:
        return (gamechannel, p1, p2, 2, p2Value)
    else: # same type
        for i in range(0, len(p1Value[1])):
            if p1Value[1][i] > p2Value[1][i]:
                return (gamechannel, p1, p2, 1, p1Value)
            elif p1Value[1][i] < p2Value[1][i]:
                return (gamechannel, p1, p2, 2, p2Value)
        return (gamechannel, p1, p2, 0, p1Value)


def draw(player, amount=1):
    for i in range(0, amount):
        player.append(deck.pop(random.randint(0, len(deck) - 1)))

def discard(player, cards):
    global p1Value, p1Discarded
    global p2Value, p2Discarded
    global p1, p2
    if player == "p1":
        hand = p1
        p1Discarded = True
    elif player == "p2":
        hand = p2
        p2Discarded = True
    temphand = hand[:]
    if cards != "0":
        for i in cards:
            i = int(i)
            i = i - 1 # because arrays start at zero
            temphand[i] = ""
            draw(temphand)
        newhand = [card for card in temphand if len(card) != 0]
        if player == "p1":
            p1 = newhand
        elif player == "p2":
            p2 = newhand


    if p1Discarded and p2Discarded:
        p1Value = getValue(p1)
        p2Value = getValue(p2)
        return compareValues()
    else:
        return "no"


def play(channel):
    global gamechannel
    gamechannel = channel
    reset()
    draw(p1, 5)
    draw(p2, 5)
    return (p1, p2)