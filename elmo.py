def shuffleDeck():
    import random
    suits = {'\u2660', '\u2661', '\u2662', '\u2663'}
    ranks = {'2','3','4','5','6','7','8','9','T','J','Q','K','A'}
    deck = []

    for suit in suits:
        for rank in ranks:
            card = rank+' '+suit
            deck.append(card)

    random.shuffle(deck)
    return deck

def checkHand(p1card,p2card):
    values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8,
              '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

    p1values = p1card.split()
    p2values = p2card.split()

    if values[p1values[0]] > values[p2values[0]]:
##        print("Player 1 wins the hand!")
        return p1card
    elif values[p2values[0]] > values[p1values[0]]:
##        print('Player 2 wins the hand!')
        return p2card
    else:
        return 1
def elmo():
    me = []
    elmo = []
    deck = shuffleDeck()
    playingField = deck[:10]
    print(playingField)
    for i in range(len(playingField)):
        if i%2==0:
            choice = input("Pick from the left or the right (L/R): ")
            if choice == "L":
                me.append(playingField[0])
                playingField.pop(0)
            else:
                me.append(playingField[-1])
                playingField.pop(-1)
            if len(playingField) != 0:
                print(playingField)
        else:
            print("Elmo's turn...")
            elmoChoice = checkHand(playingField[0],playingField[-1])
            if elmoChoice == 1:
                elmo.append(playingField[0])
                playingField.pop(0)
            else:
                elmo.append(elmoChoice)
                if elmoChoice == playingField[0]:
                    playingField.pop(0)
                else:
                    playingField.pop(-1)
            if len(playingField) != 0:
                print(playingField)
    print(f"Your hand: {me}")
    print("Your score: {}".format(tallyScore(me)))
    print(f"Elmo's hand: {elmo}")
    print("Elmo's score: {}".format(tallyScore(elmo)))

def tallyScore(playerCards):
    values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8,
              '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    score = 0
    for i in range(len(playerCards)):
        value = playerCards[i].split()
        score += values[value[0]]
    return score

elmo()
