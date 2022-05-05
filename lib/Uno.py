import random,re

def get_keys_from_value(d, val):
	# https://github.com/nkmk/python-snippets/blob/3c58602bfb74f604a9d33ecac5a0ae6a8002fb63/notebook/dict_get_key_from_value.py#L31-L36
    return [k for k, v in d.items() if v == val]

class Game:
	def __init__(self):
		self.allCards = ('n1r', 'n1r', 'n1y', 'n1y', 'n1g', 'n1g', 'n1b', 'n1b',
	    				 'n2r', 'n2r', 'n2y', 'n2y', 'n2g', 'n2g', 'n2b', 'n2b',
	    				 'n3r', 'n3r', 'n3y', 'n3y', 'n3g', 'n3g', 'n3b', 'n3b',
	    				 'n4r', 'n4r', 'n4y', 'n4y', 'n4g', 'n4g', 'n4b', 'n4b',
	    				 'n5r', 'n5r', 'n5y', 'n5y', 'n5g', 'n5g', 'n5b', 'n5b',
	    				 'n6r', 'n6r', 'n6y', 'n6y', 'n6g', 'n6g', 'n6b', 'n6b',
	    				 'n7r', 'n7r', 'n7y', 'n7y', 'n7g', 'n7g', 'n7b', 'n7b',
	    				 'n8r', 'n8r', 'n8y', 'n8y', 'n8g', 'n8g', 'n8b', 'n8b',
	    				 'n9r', 'n9r', 'n9y', 'n9y', 'n9g', 'n9g', 'n9b', 'n9b',
	    				 'n0r', 'n0y', 'n0g', 'n0b',
	    				 'asr', 'asr', 'asy', 'asy', 'asg', 'asg', 'asb', 'asb',
	    				 # 'arr', 'arr', 'ary', 'ary', 'arg', 'arg', 'arb', 'arb',
						 # Reverse cards coming soon!
	    				 'd2r', 'd2r', 'd2y', 'd2y', 'd2g', 'd2g', 'd2b', 'd2b',
	    				 'd4w', 'd4w', 'd4w', 'd4w',
	    				 'cw', 'cw', 'cw', 'cw') # Constant list of cards (tuples can't be changed)
		self.cardTypes = {'n': 'nothing',
				  		  'a': 'action',
				  		  'd': 'draw',
				  		  'cw': 'wild'}
		self.cardColors = {'r': 'red',
						  'b': 'blue',
						  'y': 'yellow',
						  'g': 'green',
						  'w': 'wild'}
		self.actionCodes = {'r': 'reverse',
							's': 'skip'}
		self.deck = []
		self.discard = []

		self.rules = {}

	def getTopCard(self, pile='deck'):
		if pile == 'deck':
			return self.deck[len(self.deck)-1]
		else:
			return self.discard[len(self.discard)-1]

	def deckCheck():
		if len(self.deck) < 1:
			self.deck = [c for c in self.discard]
			self.discard = self.deck.getTopCard()
			self.deck.pop(self.deck.index(self.getTopCard()))

	def shuffle(self):
		hat = [i for i in self.allCards]

		for i in hat:
			card = random.randint(0, len(hat)-1) # Gets the index of a card so it works with duplicates
			self.deck.append(hat[card])
			hat.pop(card)

	def matchCard(self, card1, card2):
		card1 = Card(card1)
		card2 = Card(card2)
		return card1.type == card2.type or \
			   card1.symbol == card2.symbol or \
			   card1.color == card2.color or \
			   'wild' in card1.full or 'wild' in card2.full

game = Game()

class Player():
	"""Player object constructor"""
	def __init__(self, hand=[]):
		self.hand = hand
		self.cardCount = len(self.hand)

	def getTopCard(self):
		return self.hand[len(self.hand)-1]

	def draw(self, amt):
		for i in range(amt):
			self.hand.append(game.getTopCard()) # Add top card from deck to player X's hand
			game.deck.pop() # Remove the top card from the deck
			self.cardCount += 1

	def discard(self, c):
		self.hand.pop(self.hand.index(c))
		game.discard.append(c)
		self.cardCount -= 1

class Card:
	"""Card object constructor for translating card codes
	n1r would translate to 'red 1'
	asb would translate to 'blue skip'
	d2g would translate to 'green draw 2'
	d4w would translate to 'wild draw 4'
	cw would translate to 'wild'
	... and so on and vice versa."""

	def __init__(self, code):
		self.type = None
		self.symbol = None
		self.color = None
		self.full = None
		self.code = None


		if len(code) == 2 or len(code) == 3:
			self.type = game.cardTypes[(lambda c : 'cw' if (c == 'cw') else c[0])(code)]
			self.symbol = (lambda c : c[1] if (str(c[1]) in '1234567890') else (game.actionCodes[c[1]] if (c[1] in 'sr') else None))(code)
			self.color = (lambda c : (game.cardColors[c[2]] if (len(c) == 3) else 'wild'))(code)

			self.full = None

			if self.symbol != None:
				self.full = 'wild'
			elif self.symbol == 'skip' or self.symbol == 'reverse' or str(self.symbol) in '1234567890':
				self.full = '{} {}'.format(self.color, self.symbol)
			elif self.type == 'draw':
				self.full = '{} draw {}'.format(self.color, self.symbol)
		else:
			if code == 'wild':
				self.code = 'cw'
			elif code.count(' ') == 1:
				if re.search(r'[0-9]$', code):
					self.code = 'n{}{}'.format(code.split(' ')[1],
											   get_keys_from_value(game.cardColors, code.split(' ')[0])[0])
				else:
					self.code = 'a{}{}'.format(get_keys_from_value(game.cardColors,  code.split(' ')[1])[0],
											   get_keys_from_value(game.actionCodes, code.split(' ')[0])[0])
			elif code.count(' ') == 2:
				self.code = 'd{}{}'.format(code.split(' ')[2],
										   get_keys_from_value(game.cardColors, code.split(' ')[0])[0])

	# def __call__(self):
	# 	if len(code) == 2 or len(code) == 3:
	# 		return self.full
	# 	else:
	# 		return self.code

hands = []

def setup(players=2):
	if players > 8 or players < 2:
		raise ValueError('Player count cannot be less than 2 or greater than 8.')

	game.shuffle()

	for player in range(players):
		hands.append(Player()) # Make a Player object
		hands[player].draw(7)

	game.discard.append(game.getTopCard()) # Get the starting card
	game.deck.pop(game.deck.index(game.getTopCard()))

	while not game.getTopCard('discard').startswith('n'): # Starting card cannot be an action/wild card
		game.discard.append(game.getTopCard())
		game.deck.pop(game.deck.index(game.getTopCard()))

def turn(player):
	if player == 0:
		print([Card(card).full for card in hands[0].hand if game.matchCard(Card(card), Card(game.getTopCard()))])
		card = input('Choose a card to discard (leave blank to draw a new one): ')
		player.discard(card)
	else:
		cards = [Card(card).full for card in hands[hands.index(player)].hand if game.matchCard(card, game.getTopCard())]
		print(cards)
		player.discard(random.choice(cards))

def play(p=2):
	setup(p)

	turns = 0
	while 0 not in [player.cardCount for player in hands]:
		for player in range(p):
			if Card(game.getTopCard('discard')).symbol == 'skip':
				continue
			# Reverse cards will be added in the future

			turns += 1

			print('Player {}\'s turn! (turn #{})'.format(player+1, turns))
			turn(hands[player])
			print('Player {} discarded a {} card!'.format(player+1, Card(game.getTopCard('discard')).full))

			if 0 in [p_.cardCount for p_ in hands]:
				break

def main(testing=False):
	play(3)

if __name__ == '__main__':
	main()
