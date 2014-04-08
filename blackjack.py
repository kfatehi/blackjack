from bjcore import MultiDeck, Hand, DealerHand, BankRoll
import os, sys

class Game(object):
	
	def __init__(self, decks = 6):
		self.game_state = 'Welcome'
		self.game_deck = MultiDeck(decks)
		self.player_hand = Hand()
		self.dealer_hand = DealerHand()
		self.bank_roll = BankRoll()
		self.run_flag = True
		self.play_hand_container = []
		self.runGame()
	
	#show the count of the deck		
	def printCount(self):
		print 'The count is ' + str(self.game_deck.deckCount()) + '....'
	
	#check to see if all hands are busts
	def allHandsBusted(self):
		b = 1
		for h in self.play_hand_container:
			b*=h.busted*1
		return b
	
	#break to keep the game pace
	def gamePause(self):
		print 'Press Enter to continue.'
		player_input = raw_input()
	
	#Show the hands from the perspective of a player
	#if the reveal flag is set to true, it will show the 
	#dealer's down card
	def showState(self , msg='', reveal=False):
		os.system('clear')
		print msg + '\n'
		i=len(self.play_hand_container) - 1
		j = 0
		
		for h in self.play_hand_container:	
			s = h.showHand()
			if not(h.hand_active):
				s = s + '  *'
			if (i):
				s = 'Hand ' + str(j) + ': ' + s
			else:
				s = 'Your Hand: ' + s 
			print s
			print
			j+=1
			
		dh = ''
		if reveal:
			dh = self.dealer_hand.revealHand()
		else:
			dh = self.dealer_hand.showHand()
		
		print 'Dealer Hand: ' + dh
		print
	
	#Main Welcome Screen
	def welcomeScreen(self):
		os.system('clear')
		print "======================="
		print "Welcome to BlackJack!"
		print "======================="
		print 'By John Wasack'
		print "=======================\n"
		self.gamePause()
	
	#Game over screen	
	def gameOverScreen(self):
		self.gamePause()
		self.run_flag = False
		os.system('clear')
		print "=======================\n"
		print "Game Over"
		print "Thank you for playing!\n"
		print "=======================\n"
	
	#Take the input from a bet and do some logic	
	def betInput(self):
		os.system('clear')
		bet_ok = False
		self.bank_roll.printBankRoll()
		while not(bet_ok):	
			print 'What is your bet? (Default is 5): '
			bet_input = raw_input()
			
			try:
				bet_int = int(bet_input)
				
				if bet_int > self.bank_roll.balance:
					print 'You do not have that much cash!\nPlease try again.'
				else:
					self.player_hand.wager = bet_int
					bet_ok = True
				
			except ValueError:
				if bet_input.upper() == 'Q':
					print 'Quitting game...'
					self.game_state = 'GameOver'
					return None
				self.player_hand.wager = 5
				bet_ok = True
			
		
		os.system('clear')
		print 'You have bet ' + str(self.player_hand.wager),
		return self.player_hand.wager
	
	#Deal the hand in the right order
	def startHand(self):	
		
		if (self.game_deck.percentCardsLeft() < 0.35):
			self.game_deck.shuffle()
		
		insurance = False
		
		self.play_hand_container = []
		
		self.player_hand.addCardToHand(self.game_deck.drawCard())
		self.dealer_hand.addCardToHand(self.game_deck.drawCard())
		self.player_hand.addCardToHand(self.game_deck.drawCard())
		self.dealer_hand.addCardToHand(self.game_deck.drawCard())
		
		''' THIS IS FOR DEBUG'' 
		c = self.game_deck.drawCard()
		self.player_hand.addCardToHand(c)
		self.player_hand.addCardToHand(c)
		##############################'''
		
		self.play_hand_container.append(self.player_hand)
		self.showState()
		
		if self.dealer_hand.lastCard()[1]==14:
			print 'Would you like insurance? (Y/n)'
			
			flag = True
			
			while flag:
				player_input = raw_input().upper()
				
				if player_input == 'Y':
					insurance = True
					print 'You have taken insurance.'
					flag = False
				elif player_input == 'N':
					print 'You have declined insurance'
					flag = False
				else:
					print 'You entered something incorrectly. Please type (Y) for yes or (N) for no.'
		
		if self.dealer_hand.revealValue()==21:
			self.showState('Dealer has 21', reveal=True)
			print 'Dealer has 21, you lose :('
			self.bank_roll.dec(self.player_hand.wager)
			if insurance:
				self.bank_roll.inc(2*self.player_hand.wager)
				print 'But you had insurance!'
			self.gamePause()
			return False
		else:
			if self.player_hand.handValue()==21:
				print 'BLACKJACK!'
				print 'You win ' + str(int(self.player_hand.wager*1.5))
				self.bank_roll.inc(int(self.player_hand.wager*1.5))
				if insurance:
					self.bank_roll.dec(self.player_hand.wager)
				self.gamePause()
				return False
			else:
				if insurance:
					self.bank_roll.dec(self.player_hand.wager)
				return True
	
	#This is the dealer logic for after the player makes all decisions
	#Stand on soft 17s
	def dealerLogic(self):
		dealer_go = True
		while(dealer_go):
			if self.dealer_hand.revealValue() < 17:
				print 'Dealer Hits!'
				print 'Dealer Draws: ' + self.dealer_hand.hit(self.game_deck)
				print 'Dealer Hand: ' + self.dealer_hand.revealHand()
				print
			elif self.dealer_hand.revealValue() > 21:
				print 'Dealer Busts!'
				print 'Dealer hand: ' + str(self.dealer_hand.revealHand()) + '\n'
				dealer_go=False
				return self.dealer_hand.revealHand()
			else:
				print 'Dealer Stands!'
				print 'Dealer hand: ' + str(self.dealer_hand.revealHand()) + '\n'
				dealer_go=False
				return self.dealer_hand.revealHand()
			
			self.gamePause()
			
	#Evaluate the hand(s) after the dealer has played
	def evaluateHand(self, plrhand, dealer_done = True, msg = None):
		if msg:
			print msg
		plr = plrhand.handValue()
		dlr = self.dealer_hand.revealValue()
			
		if plr > 21:
			#self.showState('Bust', reveal = True)
			print 'Player Busts!\n'
			plrhand.busted = True
			if dealer_done:	
				print '**** Player loses ' + str(plrhand.wager) + '.\n'
				self.bank_roll.dec(plrhand.wager)
				return False
			return False
			
		if dealer_done:	
			if(dlr>21):
				print 'Dealer Busts!'
				print '**** Player wins ' + str(plrhand.wager) + '. ****\n'
				self.bank_roll.inc(plrhand.wager)
				return False
			elif (dlr==plr):
				print 'Push\n'
				print '**** No Money Exchanged. ****'
				return False
			elif (dlr>plr):
				print 'Dealer Wins :('
				print '**** Player loses ' + str(plrhand.wager) + '. ****\n'
				self.bank_roll.dec(plrhand.wager)
				return False
			elif (plr>dlr):
				print '**** Player wins: ' + str(plrhand.wager) + '. ****\n'
				self.bank_roll.inc(plrhand.wager)
				return False
				
		return True
	
	#Get player input for each hand
	def playerLogic(self, player_go):
		hand_index=0
		for h in self.play_hand_container:
			while h.hand_active:		
				if len(self.play_hand_container)>1:
					print 'Active Hand: ' + str(hand_index)
				
				print 'What would you like to do?'
				print '(H) hit, (S) stand, (D) double down, (I) split, or (Q) quit'
				player_input = raw_input().upper()
				
				if player_input == 'H':
					os.system('clear')
					h.hit(self.game_deck)
					self.showState(msg = 'You Hit!')
					print 'You drew: ' + self.player_hand.lastCardFormatted()
					h.hand_active = self.evaluateHand(h, dealer_done = False)
				
				elif player_input == 'S':
					h.hand_active = False
					os.system('clear')
					self.showState('You Stand!', reveal = False)

				elif player_input == 'D':
					if h.wager*2 <= self.bank_roll.balance:	
						os.system('clear')
						
						h.wager*=2
						h.hit(self.game_deck)
						self.showState('DOUBLE DOWN!', reveal = False)
						print 'You drew: ' + self.player_hand.lastCardFormatted()
						self.evaluateHand(h, dealer_done = False)
						h.hand_active = False
					
					else:
						print 'You do not have that much cash, and so you cannot double down'
						print 'Please try again.'
				
				elif player_input == 'Q':
					print 'Quitting game...'
					self.game_state = 'GameOver'
					h.hand_active = False
					return False
				
				elif player_input == '*':
					self.printCount()
				
				elif player_input == 'I':
					can_split = self.player_hand.canSplit()
					
					if (can_split and self.bank_roll.hasEnough(h.wager*(len(self.play_hand_container)+1))):
						print 'You can split'
						new_hand = Hand()
						new_hand.addCardToHand(h.popCard())
						new_hand.addCardToHand(self.game_deck.drawCard())
						new_hand.wager = h.wager
						h.addCardToHand(self.game_deck.drawCard())
						self.play_hand_container.append(new_hand)
						self.showState('You Split!', reveal = False)

					else:
						print 'You cannot split'
						 
				
				else:
					print 'That input is not recognized. Try again.'

			hand_index+=1
		return True
	
	#This is the main game logic
	#Logical order is:
	#1) set up the hand
	#2) get player decisions
	#3) have the dealer play
	#4) evaluate the hand and change the bankroll
	def mainGameLogic(self):
		
		self.player_hand.clrHand()
		self.dealer_hand.clrHand()
		player_go = True
		
		bet = None
		if self.bank_roll.hasEnough(1):
			bet = self.betInput()
			if (bet == None):
				player_go = False
			else:
				player_go = self.startHand()
		else:
			print 'You are all out of cash!'
			player_go = False
			self.game_state = 'GameOver'
			
		if (player_go):
			player_done = self.playerLogic(player_go)
			if (player_done):
				if not(self.allHandsBusted()):
					self.showState(msg = "Dealer's Turn", reveal=True)
					self.dealerLogic()
				
				self.gamePause()
				os.system('clear')
				
				for h in self.play_hand_container:
					msg=''
					if len(self.play_hand_container) > 1:
						msg = 'Hand ' + str(self.play_hand_container.index(h)) + ' result:'
					self.evaluateHand(h, dealer_done = True, msg=msg)
					self.gamePause()
		
	#Small, rudimentary game "engine"
	def runGame(self):
		while (self.run_flag):
			
			if self.game_state == 'Welcome':
				self.welcomeScreen()
				self.game_state = "MainState"
			
			elif self.game_state == 'MainState':
				self.mainGameLogic()
			
			elif self.game_state == 'GameOver':
				self.gameOverScreen()

def main():
	game = Game()

if __name__ == '__main__':
	status = main()
	sys.exit(status)
