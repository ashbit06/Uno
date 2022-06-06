import random,re,UnoVars
global players

testing = __name__ == '__main__'
hands = []

if not testing:
    players = int(input('How many players? '))
    while players < 2 and players > 8:
        print('\nYou can\'t have '+str(players)+' players!')
        players = int(input('Player count must be between 2 and 8.\nTry again: '.format(players)))

class Game:
    class newDeck:
        """Deck subobject"""
        def __init__(self):
            self.cards = []

        def getTopCard(self):
            return self.cards[len(self.cards)-1]

    class rules:
        # Maybe add a subclass for each custom rule here?
        class stackRule:
            def __init__(self, enabled):
                self.enabled = enabled
        
        def __init__(self, customEnabled):
            self.turnOrder = 1
            self.customEnabled = customEnabled
            self.stackRule = Game.rules.stackRule(self.customEnabled)
            
            if self.customEnabled:
                # This would be where the rule config could be?
                pass
            

    def __init__(self, players=0):
        self.cards = UnoVars.cards
        self.types = UnoVars.types
        self.symbols = UnoVars.symbols
        self.colors = UnoVars.colors
        self.draw = Game.newDeck()
        self.discard = Game.newDeck()
        self.rules = Game.rules(False) # Custom rules would be in here
        self.players = int(players)

    def deckCheck(self):
        if len(self.draw.cards) < 1:
            self.draw.cards = self.discard.cards # Removed list comprehension
            self.discard.cards = self.draw.getTopCard()
            self.draw.cards.pop(self.draw.cards.index(self.draw.getTopCard()))

    def shuffle(self):
        hat = list(self.cards) # Removed list comprehension

        for i in hat:
            card = random.randint(0, len(hat)-1)
            self.draw.cards.append(hat[card])
            hat.pop(card)
            
    def reverseTurnOrder(self):
        if self.rules.turnOrder == -1:
            self.rules.turnOrder = 1
        else:
            self.rules.turnOrder = -1

    def matchCard(self, card1, card2):
        card1 = Card(card1)
        card2 = Card(card2)

        # TODO: Debug this. I forget what's wrong at the moment but I can't really
        #       fix it without knowing what's causing that recursion error.
        if card1.type == self.types['n'] or card1.type == self.types['a']:
            return card1.color == card2.color or card1.symbol == card2.symbol

    def _recite(self):
        print('CARD CODES')
        print('cards: {}'.format(self.cards))
        print('types: {}'.format(self.types))
        print('colors: {}'.format(self.colors))
        print('symbols: {}'.format(self.symbols))
        print('\nCARD NAMES (from Card)')
        print(list([Card(card).full for card in self.cards]))
        print('One card from each type: '+str([
                card for card in[
                    Card(random.choice([
                        c for c in self.cards if Card(c).type==self.types[type]
                    ])).full for type in self.types.keys()
                ]
            ]))
        print('Top card: '+self.draw.getTopCard())
game = Game()

class Player():
    """Player object constructor"""
    def __init__(self):
        self.hand = []
        self.cardCount = len(self.hand)
        self.draw(7)

    def getTopCard(self):
        return self.hand[len(self.hand)-1]
        
    def getPlayable(self, card=None, fmt='code'):
        cards_ = []
        for i in self.hand:
            if i in self.hand: # why is this here???
                cards_.extend(Card(i).getMatches(fmt))
        cards = list(set(cards_)) # remove duplicates
        if card != None:
            return [c for c in cards if game.discard.getTopCard() in Card(c).getMatches()]
        else:
            return cards
    
    def draw(self, amt):
        for i in range(amt):
            self.hand.append(game.draw.getTopCard()) # Add top card from deck to player X's hand
            game.draw.cards.pop() # Remove the top card from the deck
            self.cardCount += 1

    def discard(self, c):
        self.hand.pop(self.hand.index(c))
        game.discard.cards.append(c)
        self.cardCount -= 1

class Card:
    """Card object constructor for translating ca rd codes
    n1r would translate to 'red 1'
    asb would translate to 'blue skip'
    d2g would translate to 'green draw 2'
    d4w would translate to 'wild draw 4'
    cw would translate to 'wild'
    ... and so on and vice versa."""

    def __init__(self, raw):
        self.raw = raw
        self.isCode = len(self.raw) == 3
        self.fmt = (lambda:'code'if(self.isCode)else'name')()
        self.type = None
        self.symbol = None
        self.color = None
        self.full = None
        #game.types[(lambda x:x[0] if(self.isCode)else self.convert()[0])(self.raw)]
        """
        with self.raw as x:
            if self.isCode:
                game.types[x[0]]
            else:
                game.types[self.convert()[0]]
        """
        
        if not self.isCode:
            pass
        else:
            self.type   = game.types[self.raw[0]]
            self.symbol = game.symbols[self.raw[1]]
            self.color  = game.colors[self.raw[2]]
        
        if self.isCode:
            # if testing:
            #     print(self.color, self.type, self.symbol)

            if self.type == 'normal' or self.type == 'action' or self.type == 'wild':
                # Normal and Action cards
                self.full = '{} {}'.format(self.color, self.symbol)
            else: # Draw cards
                self.full = '{} {} {}'.format(self.color, self.type, self.symbol)

            self.full = self.full.title()
        else:
            code = self.raw.lower().split(' ')
            print(UnoVars.getKeysFromValue(game.types, code))
            self.full = '{}{}{}'.format(
                game.types[code],
                game.symbol[code],
                game.color[code],
            )
    
    def convert(self):
        # DEBUG: Causes a recursion error when called inside the constructor
        return Card(self.raw)

    def getMatches(self, f='code'):
        r = []
        cards = list(game.cards) + [
            'ww'+c for c in list(game.colors.keys())[:len(list(game.colors.keys()))-1]
        ]
        if f == 'code':
            r = [card for card in cards if game.matchCard((
                lambda x:self.raw if(self.isCode)else Card(x).code
            )(self.raw), card)]
        elif f == 'name':
            r = [Card(card).full for card in cards if game.matchCard((
                lambda x:self.raw if(self.isCode)else Card(x).code
            )(self.raw), card)]
        else:
            raise ValueError(
                'Card().getMatches() return value format can only be \'code\' (default) or \'name\'.'
            )
        return list(set(r)) # remove duplicates and return a list

    
    def getInfo(self, fmt=None):
        if fmt == None: fmt = self.fmt
        r = (lambda:self.raw if(self.isCode)else self.convert)()
        return {
            'code':(lambda:r if(self.isCode)else self.convert())(),
            'name':Card((lambda:r if(self.isCode)else self.convert())()).full,
            'type':Card((lambda:r if(self.isCode)else self.convert())()).type,
            'symbol':Card((lambda:r if(self.isCode)else self.convert())()).symbol,
            'color':Card((lambda:r if(self.isCode)else self.convert())()).color,
            'matches (codes)':self.getMatches(),
            'matches (names)':self.getMatches('name'),
            'format':self.fmt
        }

def setup(players=2):
    if players > 8 or players < 2:
        raise ValueError('Player count cannot be less than 2 or greater than 8.')

    game.shuffle()

    for i in range(players):
        hands.append(Player())

    game.discard.cards.append(game.draw.getTopCard()) # Get the starting card
    game.draw.cards.pop(game.draw.cards.index(game.draw.getTopCard()))

    while not game.discard.getTopCard().startswith('n'):
        # Starting card cannot be an action/wild card
        game.discard.cards.append(game.draw.getTopCard())
        game.draw.cards.pop(game.draw.cards.index(game.draw.getTopCard()))

def turn(player):
    card = None
    if player == 0:
        cards = []
        print('These are the cards you can draw on this turn:')
        for c in hands[player].getPlayable(game.draw.getTopCard()):
            if c in hands[player].hand:
                cards.append(c)
                print(Card(c).full)
        # for c in hands[player].getPlayable()
        if len(cards) > 0:
            print('The card you have to match is a '+Card(game.discard.getTopCard()).full+' card')
            card = Card(
                input('Choose a card to place (leave blank to draw a new one): ').title()
            ).code
            hands[player].discard(card)
        else:
            print('The card you had to match was a '+Card(game.discard.getTopCard()).full+' card')
            hands[player].draw(1)
            card = Card(game.draw.getTopCard())
            print('You didn\'t have any cards that you could\'ve drawn,')
            print('so you draw a {} card instead.'.format(card.full))
            card = card.full
    else:
        print('The card Player {} has to match is a {} card'.format(
            player, Card(game.discard.getTopCard()).full)
        )
        cards = []

        for card_ in hands[player].hand:
            if game.matchCard(card_, game.discard.getTopCard()):
                cards.append(card_)
        card = random.choice(cards)
        hands[player].discard(card)
        print('Player {} discarded a {} card!'.format(player+1, Card(card).full))

    card = Card(card)
    if card.type == game.types['w']:
        card.color = random.choice(game.colors)
    return card.convert()

def play(p=2, testing=False):
    setup(p)
    game.players = p

    turns = 0
    player = hands.index(random.choice(hands)) + 100 # Wiggle room for reverse cards and modulos
    while 0 not in [player.cardCount for player in hands]:
        hand = hands[player%p].hand
        
        if Card(game.discard.getTopCard()).symbol == 'skip':
            turns += 1
            player += 1*game.rules.turnOrder
            continue
        elif Card(game.discard.getTopCard()).symbol == 'reverse': # Reverse card beta
            game.reverseTurnOrder()
        # Reverse cards will be added in the future

        turns += 1
        player += 1*game.rules.turnOrder

        print('Player {}\'s turn! (turn #{})'.format((player%p)+1, turns))
        if testing:
            print(hand)
        discarded = turn(player%p)
        print('Player {} discarded a {} card!'.format((player%p)+1, discarded.full))
        
        if 0 in [p_.cardCount for p_ in hands]:
            break
    else:
        print('Player {} wins!'.format(None))

def main(testing=False):
    play(players, testing)

def test(testing=True, _players=3):
    setup(_players)
    game.players = _players
    game._recite()
    print('PLAYERS\' HANDS')
    for p in range(_players):
        print('Player {}\'s hand: {}'.format(p+1, [i for i in hands[p].hand]))
        print('  Cards this player can draw, given the top card'+\
              '/n  of the Discard pile: '+str(hands[p].getPlayable(fmt='name')))
    print('\nRANDOM CARD INFO:')
    x = Card(random.choice(game.cards)).getInfo()
    [print(str(i).title()+': '+str(x[i])) for i in list(x.keys())]

if testing:
    test(3)
else:
    main()
