import random
import unittest
import time
from enum import Enum,auto


class State(Enum):
	ACTIVE = auto()
	INACTIVE = auto()
	BUST = auto()

class Turn(Enum):
	HIT = auto()
	STOP = auto()

class Suit(Enum):
	HEART = auto()
	DIAMOND = auto()
	SPADE = auto()
	CLUB = auto()

class Value(Enum):
	ACE = auto()
	TWO = auto()
	THREE = auto()
	FOUR = auto()
	FIVE = auto()
	SIX = auto()
	SEVEN = auto()
	EIGHT = auto()
	NINE = auto()
	TEN = auto()
	JACK = auto()
	QUEEN = auto()
	KING = auto()

SUIT_TO_TXT = {}
SUIT_TO_TXT[Suit.HEART] = "hearts"
SUIT_TO_TXT[Suit.DIAMOND] = "diamonds"
SUIT_TO_TXT[Suit.SPADE] = "spades"
SUIT_TO_TXT[Suit.CLUB] = "clubs"

VALUE_TO_POINTS = {}
VALUE_TO_POINTS[Value.ACE] = 11
VALUE_TO_POINTS[Value.TWO] = 2
VALUE_TO_POINTS[Value.THREE] = 3
VALUE_TO_POINTS[Value.FOUR] = 4
VALUE_TO_POINTS[Value.FIVE] = 5
VALUE_TO_POINTS[Value.SIX] = 6
VALUE_TO_POINTS[Value.SEVEN] = 7
VALUE_TO_POINTS[Value.EIGHT] = 8
VALUE_TO_POINTS[Value.NINE] = 9
VALUE_TO_POINTS[Value.TEN] = 10
VALUE_TO_POINTS[Value.JACK] = 10
VALUE_TO_POINTS[Value.QUEEN] = 10
VALUE_TO_POINTS[Value.KING] = 10

VALUE_TO_TXT = {}
VALUE_TO_TXT[Value.ACE] = "ace"
VALUE_TO_TXT[Value.TWO] = "two"
VALUE_TO_TXT[Value.THREE] = "three"
VALUE_TO_TXT[Value.FOUR] = "four"
VALUE_TO_TXT[Value.FIVE] = "five"
VALUE_TO_TXT[Value.SIX] = "six"
VALUE_TO_TXT[Value.SEVEN] = "seven"
VALUE_TO_TXT[Value.EIGHT] = "eight"
VALUE_TO_TXT[Value.NINE] = "nine"
VALUE_TO_TXT[Value.TEN] = "ten"
VALUE_TO_TXT[Value.JACK] = "jack"
VALUE_TO_TXT[Value.QUEEN] = "queen"
VALUE_TO_TXT[Value.KING] = "king"

class Card():
	def __init__(self, suit, value):
		self.suit = suit
		self.value = value

class Player():
	#initilise the player
	def __init__(self, user, name):
		self.__user = user #set to 0 if human, otherwise the value is the value that the ai stops at
		self.__point_cap = user #for readability
		self.name = name
		self.deck = []
		self.__points = 0
		self.state = State.ACTIVE
	
	#give the player a card, award points, and if nessisary, set the player to innactive
	def recive_card(self, card):
		self.deck.append(card)
		if card[1] == 11 or card[1] == 12 or card[1] == 13:
			self.__points += 10
		else:
			self.__points += card[1]
		if self.__points > 21:
			self.state = State.BUST
			
	#changes the state of the player to innactive
	def stop(self):
		self.state = State.INACTIVE
		

	#Human and ai turns. Returns 0 if the user is continuing, 1 if the player has stoped.
	def get_turn(self):
		print(self.name + "'s turn.")
		if self.user == 0:
			print("You have the following hand:")
			read_hand(self.hand)
			print("Your hand has a value of " + str(self.__points) + " points.")
			ans = get_menu(["hit", "stop"], "Would you like to HIT, or would you like to STOP?", "Please select a valid option")
			if ans == 0:
				turn = Turn.STOP
			else:
				turn = Turn.HIT
		else:
			if self.__points >= self.__point_cap:
				print(self.name + " has stop.")
				turn = Turn.STOP
			else:
				print(self.name + " has drawn a card.")
				turn = Turn.HIT
		return turn


#creates a deck and shuffles it, then returns the deck. Decks in the number of decks being shuffled
def make_deck(decks):
	deck = []
	for i in decks:
		for s in Suit:
			for v in Value:
				new_card = Card(s, v)
				deck.append(new_card)
	random.shuffle(deck)
	return deck

#creates and returns a string of the card
def read_card(card):
	suit = card[0]
	value = card[1]
	suit_txt = SUIT_TO_TXT.get(suit)
	value_txt = VALUE_TO_TXT.get(value)
	word = value_txt.capitalize() + " of " + suit.capitalize()
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
def do_game(players):
	if len(players) == 0:
		print("There are no players to play!")
		return None
	else:
		game = True
		deck = make_deck(1) #makes the deck
		innactive = [] #when someone stops, they go from the active list into the innactive list. When someone busts, they are removed from the active list and are NOT added to the innactive list 
		active = players
		for p in active:
			for i in range(2):
				card = deck.pop()
				p.recive_card(card)
		while game == True:
			active_2 = active
			#print("ding")
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



#players is a list of players who are able to win. Returns the winers.
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


#cpu = Player(16, "CPU 1")
#you = Player(0, "Kate")
#do_game([cpu, you])

#print(State.ACTIVE)
#print(repr(State.ACTIVE))
#print(type(State.ACTIVE))
#print(isinstance(State.ACTIVE, State))
#print("==============")
#print(State(1))
#print(State(2))
#print(State(3))
