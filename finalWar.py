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

def deal(deck, player1, player2):

    for i in range(len(deck)):
        if i%2==0:
            player1.append(deck[i])
        else:
            player2.append(deck[i])

def war():
    deck = shuffleDeck()
    player1=[]
    player2=[]

    deal(deck,player1,player2)
    
    count = 0
    battle = 0
    doubleBattle = 0
    playSignal = 1
    p1Win = 0
    p2Win = 0
    stats = [count,battle,doubleBattle,playSignal,p1Win,p2Win]

    
    while stats[3] == 1:
        stats[0]+=1
        print('Turn #',stats[0])
        print('Player 1 deck: {}'.format(len(player1)))
        print('Player 2 deck: {}'.format(len(player2)))
##        final = tally(player1,player2)
##        if final == 0:
##            break
        if (len(player1) or len(player2)) == 0:
            break
        finalStats = playTurn(player1,player2,stats)
        if finalStats[3] == 0:
            break
        check = checkDeck(deck,player1,player2)
        if check > 0:
            print(finalStats)
            break
##    print('Player 1 deck: {}'.format(len(player1)))
##    print('Player 2 deck: {}'.format(len(player2)))
    result = tally(player1, player2, stats)
    if stats[4] == 1:
        print("Player1 wins")
    elif stats[5] == 1:
        print("Player2 wins")
    else:
        print('tie?')
    return (finalStats[0],finalStats[1],finalStats[2])

def tally(player1, player2,stats):
    if len(player1) == 0:
        stats[5]+=1
    if len(player2)==0:
        stats[4]+=1
    return stats
    
def checkDeck(deck,player1,player2):
    if (len(player1)+len(player2))<len(deck):
##        print('Player 1 deck: {}'.format(len(player1)))
##        print('Player 2 deck: {}'.format(len(player2)))
        print('DECK SIZE ERROR - MISSING CARDS')
        print('IN CHECKDECK: player1: {}, player2: {}'.format(len(player1),len(player2)))
        return 1
    elif (len(player1)+len(player2))>len(deck):
##        print('Player 1 deck: {}'.format(len(player1)))
##        print('Player 2 deck: {}'.format(len(player2)))
        print('DECK SIZE ERROR - TOO MANY CARDS')
        return 2
    else:
        return 0

def playTurn(player1,player2,stats):
    import random
    #stats[3] = playSignal; setting to 0 breaks war() loop

    if len(player1) == 0:
        stats[3]=0
        return stats
    if len(player2) == 0:
        stats[3]=0
        return stats

    random.shuffle(player1)
    random.shuffle(player2)

    p1card = player1.pop()
    p2card = player2.pop()

    print('1\n\n2\n\n3\n\nFlip!')
    print('Player 1: {:>7}'.format(p1card))
    print('Player 2: {:>7}'.format(p2card))

    result = checkHand(p1card,p2card)
    if result == 1:
        #if player 1 wins:
        stats[0]+=1
        player1.append(p1card)
        player1.append(p2card)
        return stats        
    elif result == -1:
        #if player 2 wins:
        stats[0]+=1
        player2.append(p1card)
        player2.append(p2card)
        return stats
    else:
        #if there is a tie:
        stats[1]+=1
        #stats[1] = "double war count"
        if (len(player1)>0) and (len(player2)>0):
            #if both player1 and player2 have cards in their hand, play out the
            #battle
            battle(p1card, player1, p2card, player2,stats)
        else:
            #if either has 0 cards at this point,
            print('IN PLAYTURN: player1: {}, player2: {}'.format(len(player1),len(player2)))
            print('Checking size of distributed cards:')
            print(len(player1)+len(player2))
            if len(player1)>len(player2):
                player1.append(player2)
            else:
                player2.append(player1)
##            max([player1,player2]).append(min([player1,player2]))
##            print('Battle, but {} has {} cards'.format(max([player1, player2]), len(max([player1,player2]))))
        return stats

def checkHand(p1card,p2card):
    values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8,
              '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

    p1values = p1card.split()
    p2values = p2card.split()

    if values[p1values[0]] > values[p2values[0]]:
##        print("Player 1 wins the hand!")
        return 1
    elif values[p2values[0]] > values[p1values[0]]:
##        print('Player 2 wins the hand!')
        return -1
    else:
        return 0

def battle(p1card,player1,p2card,player2,stats):
    
##    print('THIS MEANS WAR')
    
    if len(player1)>1:
        p1flipcard = player1.pop()
    else:
        #print('Battle',len(player1))
        player2.append(player1.pop())
        return

    if len(player2)>1:
        #print('Battle',len(player2))
        p2flipcard = player2.pop()
    else:
        player1.append(player2.pop())
        return
    
    stash = [p1card,p2card]    
    stash = prepStash(stash,player1)
    stash = prepStash(stash,player1)

    stash.append(p1flipcard)
    stash.append(p2flipcard)

    result = checkHand(p1flipcard,p2flipcard)
##    print("Stash:",stash)
    if result == 1:
##        print('Player 1 wins this battle!')
        for i in range(len(stash)):
            player1.append(stash[i])
        print('IN BATTLE: player1: {}, player2: {}'.format(len(player1),len(player2)))
        return stats
    elif result == -1:
##        print('Player 2 wins this battle!')
        for i in range(len(stash)):
            player2.append(stash[i])
        print('IN BATTLE: player1: {}, player2: {}'.format(len(player1),len(player2)))
        return stats
    else:
        stats[2]+=1
        doubleBattle(stash,player1,player2)
        print('IN BATTLE: player1: {}, player2: {}'.format(len(player1),len(player2)))
        return stats

def prepStash(stash,player):
    if len(player)>3:
        for i in range(3):
            stash.append(player.pop())
    elif len(player)==1:
        pass
    else:
        for i in range(len(player)-1):
            stash.append(player.pop())
    return stash

def doubleBattle(stash,player1,player2):
    #print("THIS MEANS ... DOUBLE WAR ... I GUESS")
    #print(len(player1))
    print('IN DOUBLEBATTLE: player1: {}, player2: {}'.format(len(player1),len(player2)))
    if len(player1)>1:
        stash = prepStash(stash,player1)
    else:
        #print('Player 1 forfeits...')
        #print('Double battle',len(player1))
        player2.append(player1.pop())
        print('IN 2x BATTLE: player1: {}, player2: {}'.format(len(player1),len(player2)))
        return

    if len(player2)>1:
        stash = prepStash(stash,player2)
    else:
        #print('Player 2 forfeits...')
        #print('Double battle',len(player1))
        player1.append(player2.pop())
        return

    p1flipcard = player1.pop()
    p2flipcard = player2.pop()
    stash.append(p1flipcard)
    stash.append(p2flipcard)

##    print('2x Stash:',len(stash),stash) #not conveying full stash?
    
    result = checkHand(p1flipcard,p2flipcard)

    if result == 1:
##        print('Player 1 wins this DOUBLE BATTLE!')
        for i in range(len(stash)):
            player1.append(stash[i])
    elif result == -1:
##        print('Player 2 wins this DOUBLE BATTLE!')
        for i in range(len(stash)):
            player2.append(stash[i])
    if result == 0:
##        print("THIS MEANS ... TRIPLE WAR ... I GUESS")
        for i in range(len(stash)):
            if i%2==0:
                player1.append(stash[i])
            else:
                player2.append(stash[i])
    
def warStats(n):
    battles =[]
    wars = []
    doubleWar = []
    for i in range(n):
        results = war()
        battles.append(results[0])
        wars.append(results[1])
        doubleWar.append(results[2])
    battleAvg = sum(battles)/len(battles)
    warAvg = sum(wars)/len(wars)
    doubleWarAvg = sum(doubleWar)/len(doubleWar)
    print("Average # of Battles: {:3}\nAverage # of Wars: {:3}\nAverage # of 2x Wars: {:3}".format(battleAvg,warAvg,doubleWarAvg))


war()

    
    
