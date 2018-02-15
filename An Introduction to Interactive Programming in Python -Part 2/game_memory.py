# __akgarhwal__
# link : http://www.codeskulptor.org/#user44_aPDpvGAnystO9pT.py

# implementation of card game - Memory

import simplegui
import random

card_deck = [x for x in range(8)] * 2
exposed = [False] * 16
state = 0
last_card = [-1,-1]
turn_counter = 0

# helper function to initialize globals
def new_game():
    global state
    global exposed
    global turn_counter
    turn_counter = 0
    exposed = [False] * 16
    state = 0
    random.shuffle(card_deck)
    
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state
    global last_card
    global turn_counter
    card_index = pos[0] // 50
    
    if exposed[card_index] :
        return
    
    if state == 0:
        state = 1
        last_card[0] = card_index
        exposed[card_index] = True
    elif state == 1:
        turn_counter += 1
        state = 2
        last_card[1] = card_index
        exposed[card_index] = True
    else:
        state = 1
        if card_deck[last_card[0]] != card_deck[last_card[1]]:
            exposed[last_card[0]] = False
            exposed[last_card[1]] = False   
        last_card[0] = card_index
        exposed[card_index] = True
        
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    label.set_text("Turns = "+str(turn_counter))
    card_pos = 0
    SIZE = 50
    #print(card_deck)
    for card_index in range(len(card_deck)):
        card_pos = SIZE * card_index
        canvas.draw_text(str(card_deck[card_index]), (card_pos+10, SIZE+15), SIZE, 'White')
        if not exposed[card_index]:
            canvas.draw_polygon([[SIZE*card_index, 0],[SIZE*card_index+SIZE, 0],[SIZE*card_index+SIZE, 100],[SIZE*card_index, 100]], 5, 'Green', 'Red')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
