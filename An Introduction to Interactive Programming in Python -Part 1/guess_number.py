# __akgarhwal__
# Simple Game : Guess the number
# link : http://py3.codeskulptor.org/#user301_To6e6yMoNhKrCVp.py
# template for "Guess the number" mini-project
import simplegui
import random
# input will come from buttons and an input field
# all output for the game will be printed in the console
secret_number = 0
num_range = 100
remaining_guess = 7

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    global num_range
    global remaining_guess
    if num_range == 100:
        remaining_guess = 7
    else:
        remaining_guess = 10
    secret_number = random.randrange(0,num_range)
    print("\n\nNew game. Range is [0,"+str(num_range)+")")
    print("Number of remaining guesses is "+str(remaining_guess))
    

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global num_range
    global remaining_guess
    remaining_guess = 7
    num_range = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global num_range
    global remaining_guess
    remaining_guess = 10
    num_range = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global remaining_guess
    guess_number = int(guess)
    print ("\nGuess was "+str(guess_number))
    remaining_guess -= 1
    print("Number of remaining guesses is "+str(remaining_guess))
    if secret_number != guess_number and remaining_guess == 0 :
        print("You ran out of guesses.  The number was "+str(secret_number))
        new_game() 
    elif secret_number < guess_number :
        print("Lower")
    elif secret_number > guess_number :
        print("Higher")
    else:
        print("Correct")
        new_game()

def restart():
    # restart game 
    new_game()

# create frame
f = simplegui.create_frame("Guess the number",300,300)


# register event handlers for control elements and start frame
f.add_input("Enter Number", input_guess, 100)
f.add_button("Restart",restart,100)
f.add_button("Range is [0,100)",range100,100)
f.add_button("Range is [0,1000)",range1000,100)
          
          
f.start()
# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
