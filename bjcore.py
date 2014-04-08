#
# This is the core for the blackjack game.
# It has a host of objects for the flow of gameplay
#

from random import randrange

class Deck(object):
    def __init__(self):
        self.deck=[]
        suites = ['D', 'H', 'S', 'C']
        cards = range(2,15)
        i=0
        for s in suites:
            for r in cards:
                self.deck.append((s,r))
                i+=1

    def cards(self):
        return self.deck
#
# Many decks object
#
class MultiDeck(object):
    def __init__(self, numdecks):
        self.numdecks = numdecks 
        self.deck = []
        self.discard_pile = []      
        self.shuffle() 
                
    def cardsRemaining(self):
        return len(self.deck)
    
    def percentCardsLeft(self):
        return float(self.cardsRemaining())/float((self.numdecks*52))
    
    def drawCard(self, count=1):
        drawn_card = []
        for i in range(0,count):            
            rand_index = randrange(0,len(self.deck))
            drawn_card.append(self.deck[rand_index])
            self.discard_pile.append(self.deck[rand_index])
            del self.deck[rand_index]
        return drawn_card

    def shuffle(self):
        self.deck = []
        for i in range(0,self.numdecks):
            self.deck+=Deck().cards()
            
    def deckCount(self):
        hc = lambda x: x>9*1
        lc = lambda x: x<7*1
        highcards = sum([hc(c[1]) for c in self.discard_pile])
        lowcards = sum([lc(c[1]) for c in self.discard_pile])
        return lowcards-highcards

class Hand(object):
    def __init__(self):
        self.cards_in_hand = []
        self.soft = 0
        self.hand_active = True
        self.busted = False
        self.wager = 5
    
    def addCardToHand(self, card):
        if card[0][1] == 14:
            self.soft += 1
        self.cards_in_hand += card
        
    def hit(self, deck):
        card = deck.drawCard()
        self.addCardToHand(card)
        return self.formatCard(card[0])

    def handValue(self):        
        self.v = 0        
        if self.cards_in_hand:        
            for c in self.cards_in_hand:
                if 14 > c[1] > 10:
                    self.v+=10
                elif c[1] == 14:
                    self.v += 11
                else:
                    self.v+=c[1]
            
            if self.v > 21:
                i=0
                while (self.v>21 and i< self.soft):
                    self.v-=10
                    i+=1
            
            return self.v            
                
        else:
            return 0
    
    def formatCard(self, card):
        
        cardDict = {11:'J', 12:'Q', 13:'K', 14:'A'}
        if card[1]>10:
            return '(' + str(cardDict[card[1]])+ ' of ' + str(card[0]) + ')'
        else:
            return '('+str(card[1])+' of '+str(card[0])+')'
    
    def showHand(self):
        return ' '.join([self.formatCard(c) for c in self.cards_in_hand])+':'+str(self.handValue())
    
    def clrHand(self):
        self.cards_in_hand = []
        self.soft = 0
        self.hand_active = True
        self.busted = False
    
    def lastCard(self):
        return  self.cards_in_hand[-1]
    
    def lastCardFormatted(self):
        return  self.formatCard(self.cards_in_hand[-1])
    
    def popCard(self):
        try: 
            index = len(self.cards_in_hand) - 1 
            card = self.cards_in_hand[index]
            self.cards_in_hand.remove(card)
            return [card]
        except IndexError:
            return []
    
    def cardCount(self):
        return len(self.cards_in_hand)
    
    def cardValue(self, card):
        if 2 <= card[0][1] <= 9:
            return card[0][1]
        elif 10<=card[0][1]<=13:
            return 10
        elif card[0][1] == 14:
            return 11
    
    def canSplit(self):
        if self.cardCount() == 2:
            return self.cardValue([self.cards_in_hand[0]]) ==  self.cardValue([self.cards_in_hand[1]])
        else:
            return False
        
class DealerHand(Hand):
    def __init__(self):
        Hand.__init__(self)
        
    def handValue(self):
        v = int(self.lastCard()[1])
        if (14>v>10):
            return 10
        elif (v==14):
            return 11
        else:
            return v     
     
    def showHand(self):
        return '(*, *) '+' '.join([self.formatCard(c) for c in self.cards_in_hand[1:]])+':'+str(self.handValue())
    
    def revealHand(self):
        return ' '.join([self.formatCard(c) for c in self.cards_in_hand])+':'+str(Hand.handValue(self))
    
    def revealValue(self):
        return Hand.handValue(self)

class BankRoll(object):
    def __init__(self):
        self.balance = 500
    
    def inc(self, amount):
        self.balance+=amount
    
    def dec(self, amount):
        self.balance-=amount
        
    def printBankRoll(self):
        print 'You currently have: ' + str(self.balance)
        
    def hasEnough(self, bet):
        if bet>self.balance:
            return False
        else:
            return True
