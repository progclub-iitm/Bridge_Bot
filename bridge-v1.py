import random  #module used for shuffle functionality

suit_vals = {'NT':4,'S':3,'H':2,'D':1,'C':0} 
directions = ['North','East','South','West']
rank = {'A':13,'K':12,'Q':11,'J':10,'10':9,'9':8,'8':7,'7':6,'6':5,'5':4,'4':3,'3':2,'2':1}

def arrange(hand):  
    #Arranges a hand first by suit and then by rank
    l = len(hand)
    number_list = [number(j) for j in hand]
    for i in range(l-1):
        for j in range(i+1,l):
            if number_list[i]<number_list[j]:
                hand[j],hand[i] = hand[i],hand[j]
                number_list[j],number_list[i]=number_list[i],number_list[j]
    return hand

def number(card):
    #function that assigns a numeric value for each card to make sorting easier
    return 13*suit_vals[card[-1]] + rank[card[:-1]]

def display_bid(bid_list):
    #Prints the bidding process so far
    print 
    print 'North'.ljust(6),'East'.ljust(6),'South'.ljust(6),'West'.ljust(6)
    print '-'*50

    l = len(bid_list)
    for i in range(0,l):
        print bid_list[i].ljust(6),
        if i%4 ==3:
            print
    print

def valid_bid(current_bid,prev_bid):
    #Determines if a bid is a valid one
    cnum = current_bid[0]
    pnum = prev_bid[0]
    csuit = current_bid[1:]
    psuit = prev_bid[1:]
    if current_bid == 'PASS':
        return True
    if csuit not in ['S','H','D','C','NT']:
        return False
    if cnum not in '1234567':
        return False
    if int(cnum)>7 or int(cnum)<int(pnum):
        return False
    if cnum == pnum:
        if csuit == 'NT':
            return True
        if csuit<=psuit:
            return False
    return True
            
def winner(trick,trump):
    #returns the winner of a trick
    if trump == 'NT':
        winning_suit = trick[0][-1]
    else:
        for card in trick:
            if trump in card:
                winning_suit = trump
                break
        else:
            winning_suit = trick[0][-1]

    winning_turn = 0
    Max = 0
    for i in range(0,4):
        if trick[i][-1] == winning_suit:
            if rank[trick[i][:-1]]>Max:
                Max = rank[trick[i][:-1]]
                winning_turn = i

    return winning_turn

def get_card(direction,player_hand,dummies_hand,cards_so_far,contract,ns_tricks,ew_tricks):  #technically it should be dummy's not dummies. but yolo
    #This function will be replaced by the output from the AI
    print direction, 'turn to play'
    print 'Contract:',contract
    print 'North-South: %d East-West: %d ' % (ns_tricks, ew_tricks) 
    print 'Your hand:',player_hand
    print 'Dummies Hand:',dummies_hand
    card = raw_input('Enter card:')
    while card not in player_hand:
        card = raw_input('Enter valid card:')
    print
    
    return card
    
#Creating and shufling the deck      
deck = [i+j for i in ['A','K','Q','J','10','9','8','7','6','5','4','3','2'] for j in 'SHDC']
random.shuffle(deck)

#Distributing cards to players
north_hand = arrange(deck[0:13])
east_hand = arrange(deck[13:26])
south_hand = arrange(deck[26:39])
west_hand = arrange(deck[39:52])

total_deal = [north_hand,east_hand,south_hand,west_hand]

#Showing hands. The hands will be passed as input to the AI
print 'press Q for next player'
for i in range(4):
    print directions[i]
    for j in total_deal[i]:
        print j,
    print
    c = raw_input()
    while c!='Q':
        c = raw_input()        

#Bidding
print 'Bidding has started'
bid_list = []
prev_bid = '0S'
turn = 0
pass_counter = 0
while True:
    print directions[turn], 'make a valid bid:'
    c = raw_input()       #These raw_input() statements will be replaced by output from the AI
    while valid_bid(c,prev_bid) != True:
        print 'Enter valid bid'
        c = raw_input()
    
    bid_list.append(c)
    display_bid(bid_list)
    if c == 'PASS':
        pass_counter +=1
        if pass_counter == 3 and len(bid_list)>3:
            break
            #After three consecutive passes the bidding is over
        elif pass_counter == 4:
            print 'Game passed out'
            quit()
            #If aall four players pass on the the first round, game is chucked
    else:
        prev_bid = c
        pass_counter = 0
        
    turn += 1
    turn = turn%4
    
contract = bid_list[-4] #Last three elements are PASS. Fourth last is the final contract

trump = contract[1:]

#Finding declarer and dummy
L = len(bid_list)
#Assuming bidding started with north
if L%2 == 0: #north-south won the bidding
    for i in range(0,L,2): #Checking only north-south bids
        if bid_list[i][1:] == trump:
            declarer_turn = i%4
            dummy_turn = (declarer_turn + 2)%4
            break
else: #east_west won the bidding
    for i in range(1,L,2): # checking only east-west bids
        if bid_list[i][1:] == trump:
            declarer_turn = i%4
            dummy_turn = (declarer_turn + 2)%4
            break
        
print 'Declarer:',directions[declarer_turn]
print 'Dummy:',directions[dummy_turn]
print

ns_tricks = 0
ew_tricks = 0
cards_so_far = [['' for j in range(4)]for i in range(13)] #keeps track of cards played so far. (ideal player remembers all the cards played)
turn = (declarer_turn+1)%4

for i in range(13): #loop over 13 tricks
    for j in range(4):
        dummies_hand = total_deal[dummy_turn] 
        players_hand = total_deal[turn]
        card = get_card(directions[turn],players_hand,dummies_hand,cards_so_far,contract,ns_tricks,ew_tricks,)
        total_deal[turn].remove(card)        
        cards_so_far[i][turn] = card
        turn += 1
        turn =turn%4
    trick = cards_so_far[i]
    turn = winner(trick,trump)
    
    if turn%2 == 0: 
        ns_tricks += 1
    else:
        ew_tricks += 1 
        


    
















    


        

