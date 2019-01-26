import random
import unittest
import time

ACTIVE = 1
INACTIVE = 2
BUST = 3

class Player():
	#initilise the player
	def __init__(self, user, name):
		self.user = user #set to 0 if human, otherwise the value is the value that the ai stops at
		self.name = name
		self.deck = []
		self.points = 0
		self.state = ACTIVE
	
	#give the player a card, award points, and if nessisary, set the player to innactive
	def recive_card(self, card):
		self.deck.append(card)
		if card[1] == 11 or card[1] == 12 or card[1] == 13:
			self.points += 10
		else:
			self.points += card[1]
		if self.points > 21:
			self.state = BUST


			
	def stop(self):
		self.state = INACTIVE
		

	#Human and ai turns. Returns 0 if the user is continuing, 1 if the player has stoped.
	def get_turn(self):
		print(self.name + "'s turn.")
		if self.user == 0:
			print("You have the following hand:")
			for i in self.deck:
				print("A " + read_card(i))
			print("Your hand has a value of " + str(self.points) + " points.")
			hit = get_menu(["hit", "stop"], "Would you like to HIT, or would you like to STOP?", "Please select a valid option")
			return hit
		else:
			if self.points >= self.user:
				print(self.name + " has stop.")
				return 1
			else:
				print(self.name + " has drawn a card.")
				return 0
			

#creates a deck and shuffles it, then returns the deck
def make_deck():
	deck = []
	for s in range(4):
		for v in range(13):
			deck.append((s + 1, v + 1))
	random.shuffle(deck)
	return deck

#creates and returns a string of the card	
def read_card(card):
	if card[0] == 1:
		suit = "Hearts"
	elif card[0] == 2:
		suit = "Dimonds"
	elif card[0] == 3:
		suit = "Clubs"
	elif card[0] == 4:
		suit = "Spades"
	else:
		suit = "Jevils"
	
	if card[1] == 1:
		value = "Ace"
	elif card[1] == 11:
		value = "Jack"
	elif card[1] == 12:
		value = "Queen"
	elif card[1] == 13:
		value = "King"
	else:
		value = str(card[1])
	
	word = value + " of " + suit
	return word

def read_hand(hand):
	words = ""
	for i in hand:
		if hand[-1] == i:
			words = words + "and " + read_card(i) + "."
		else:
			words = words + read_card(i) + ", "
	return words

def get_menu(valid, prompt, error):
	ans = input(prompt).lower().strip()
	while not ans in valid:
		print(error)
		ans = input(prompt)
	return valid.index(ans)


#takes in a list of player objects returns the object of the player that won, returns None if nobody wins
def do_game(active):
	if len(active) == 0:
		print("There are no players to play!")
		return None
	else:
		game = True
		deck = make_deck()
		innactive = [] #when someone stops, they go from the active list into the innactive list. When someone busts, they are removed from the active list and are NOT added to the innactive list 
		for p in active:
			for i in range(2):
				card = deck.pop()
				p.recive_card(card)
		while game == True:

			active_2 = active
			print("ding")
			for p in active_2:
				print(p.name)
				print(p.state)
				if p.state == 2:
					innactive.append(p)
					active.remove(p)
				elif p.state == 3:
					active.remove(p)
			
			if len(active) == 0:
				if len(innactive) == 0:
					print("All players have bust. Ending game.")
					winners = None
					game = False
				else:
					print("All players have eather bust or stoped.")
					winners = find_winner(innactive)
					length = len(winners)
					if length == 1:
						print("The winner is " + winners[0].name)
						print("They had a hand of a " + read_hand(winners[0].deck))
					else:
						print("The winners are "),
						for i in range(length - 1):
							print(winners[i].name + ", "),
						print("and " + winners[length - 1] + ".")
					game = False

			print(active)		
			for p in active:
				turn = p.get_turn()
				if turn == 0:
					card = deck.pop()
					p.recive_card(card)
					if p.user == 0:
						print("You drew a " + read_card(card))
					if p.state == 3:
						print(p.name + " has bust.")
				elif turn == 1:
					p.stop()

			
		return winners
							
					
					


#players is a list of players who stoped. Returns the winers
def find_winner(players):
	point = 0
	winners = []
	for i in players:
		if i.points > point:
			winners = [i]
			points = i.points
		elif i.points == point:
			winners.append(i)
	return winners


cpu = Player(16, "CPU 1")
you = Player(0, "Kate")
do_game([cpu, you])







                        
                        
