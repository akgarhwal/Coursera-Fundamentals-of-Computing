# __akgarhwal__
# Link : http://www.codeskulptor.org/#user44_fuDg2lVhVrwVARb.py

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
result = ""

deck = None
player = None
dealer = None

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        hand_str = "Hand contains "
        for card in self.hand:
            hand_str += str(card) + " "
        return hand_str

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        total_value = 0
        Ace = 0
        for card in self.hand:
            total_value += VALUES[card.rank]
            if card.rank == 'A':
                Ace = 10
        if total_value+Ace <= 21 :
            total_value += Ace
        return total_value
    
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0;
        for card in self.hand:
            card.draw(canvas,[pos[0]+80*i, pos[1]])
            i += 1
         
        
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()	
        
    def __str__(self):
        # return a string representing the deck
        deck_str = "Deck contains"
        for card in self.deck:
            deck_str += " " + str(card)
        return deck_str

#define event handlers for buttons
def deal():
    global outcome, in_play, result, score
    global deck,player,dealer
    
    if in_play :
        score -= 1
        result = "You lost :("
        in_play = False
    else:    
    
        deck = Deck()
        deck.shuffle()

        dealer = Hand()
        dealer.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())

        player = Hand()
        player.add_card(deck.deal_card())
        player.add_card(deck.deal_card())

        outcome = "Hit or stand?"
        result = ""
        in_play = True

def hit():
    global player, outcome, in_play, score, result
    # if busted, assign a message to outcome, update in_play and score
    # if the hand is in play, hit the player
    if in_play :
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
    
        if player.get_value() > 21:
            result = "You went bust and lose."   
            outcome = "New deal?"
            score -= 1
            in_play = False
     
     
def stand():
    global outcome, result, score, in_play
    global dealer,player
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score
    if in_play:
    
        outcome = "New deal?"
        in_play = False
    
        player_point = player.get_value()
        if player_point > 21 :
            result = "You already busted"
            return 
        
        while (dealer.get_value() < 17):
            dealer.add_card(deck.deal_card())
        
        dealer_point = dealer.get_value()
        if dealer_point > 21:
            score += 1
            result = "Dealer busted and you Won"
            return 
        
        if player_point <= dealer_point:
            result = ("Dealer Won")
            score -= 1
        else:
            result = ("You won :)")
            score += 1    
      
    
# draw handler    
def draw(canvas):
    global player,dealer, score, outcome, result
    
    canvas.draw_text('BlackJack v0.1', (60, 40), 30, 'White')
    canvas.draw_text('Dealer', (80, 85), 25, 'White')
    canvas.draw_text('You', (80, 305), 25, 'White')
    canvas.draw_text('Score '+str(score), (380, 40), 30, 'White')
    canvas.draw_text(outcome, (250, 305), 30, 'White')
    canvas.draw_text(result, (80, 520), 30, 'White')
    #print(result)
    dealer.draw(canvas, [80, 100])
    player.draw(canvas, [80, 320])

    if in_play :
        card_loc = (CARD_CENTER[0], CARD_CENTER[1] )
        canvas.draw_image(card_back, card_loc, CARD_SIZE, [80 + CARD_CENTER[0], 100 + CARD_CENTER[1]], CARD_SIZE)
        
        
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()



