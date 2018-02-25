# __akgarhwal_
# Link : http://www.codeskulptor.org/#user44_WQ2XxBuh4LlGQyE.py

"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1000         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def switch_player(player):
    """ switch player X -> O
    """
    if player == provided.PLAYERX:
        return provided.PLAYERO
    return provided.PLAYERX

def mc_trial(board,player):
    """ compute trials 
    """
    _emptysquare = board.get_empty_squares()
   
    while len(_emptysquare) != 0:
        _randindex = random.randrange(len(_emptysquare))
        _square = _emptysquare[_randindex]
        board.move(_square[0],_square[1],player)
        player = switch_player(player) 
        _emptysquare = board.get_empty_squares()
        if board.check_win() != None :
            break
    
    
def mc_update_scores(scores, board, player):
    """ mc_update score
    """
    _size = board.get_dim()
    if board.check_win() == player:
        for _row in range(_size):
            for _col in range(_size):
                if board.square(_row,_col) == provided.EMPTY:
                    scores[_row][_col] += 0
                elif board.square(_row,_col) == player:
                    scores[_row][_col] += 1
                else:
                    scores[_row][_col] += -1

    elif board.check_win() != provided.DRAW:
        for _row in range(_size):
            for _col in range(_size):
                if board.square(_row,_col) == provided.EMPTY:
                    scores[_row][_col] += 0
                elif board.square(_row,_col) == player:
                    scores[_row][_col] += -1
                else:
                    scores[_row][_col] += 1
                    
def get_best_move(board, scores):
    """ get best move
    """
    _emptysq = board.get_empty_squares()
    score = -1e9
    res = ()
    for _square in _emptysq:
        if scores[_square[0]][_square[1]] > score :
            score = scores[_square[0]][_square[1]]
            res = _square
    return res

def mc_move(board, player, trials):
    """ mc move 
    """
    #print(player)
    
    _size = board.get_dim()
    scores = []
    for _row in range(_size):
        temp = []
        for _col in range(_size):
            temp.append(0)
        scores.append(temp)
        
    for _trail in range(trials):
        _board = board.clone()
        mc_trial(_board, player)
        mc_update_scores(scores, _board, player)
    
    #print(scores)    
    _empty = board.get_empty_squares()
    if len(_empty) > 0:
        return get_best_move(board, scores)
    return None

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)


"""
## class TTTBoard
class TTTBoard:
    """
    Class to represent a Tic-Tac-Toe board.
    """

    def __init__(self, dim, reverse = False, board = None):
        """
        Initialize the TTTBoard object with the given dimension and 
        whether or not the game should be reversed.
        """
            
    def __str__(self):
        """
        Human readable representation of the board.
        """

    def get_dim(self):
        """
        Return the dimension of the board.
        """
    
    def square(self, row, col):
        """
        Returns one of the three constants EMPTY, PLAYERX, or PLAYERO 
        that correspond to the contents of the board at position (row, col).
        """

    def get_empty_squares(self):
        """
        Return a list of (row, col) tuples for all empty squares
        """

    def move(self, row, col, player):
        """
        Place player on the board at position (row, col).
        player should be either the constant PLAYERX or PLAYERO.
        Does nothing if board square is not empty.
        """

    def check_win(self):
        """
        Returns a constant associated with the state of the game
            If PLAYERX wins, returns PLAYERX.
            If PLAYERO wins, returns PLAYERO.
            If game is drawn, returns DRAW.
            If game is in progress, returns None.
        """
            
    def clone(self):
        """
        Return a copy of the board.
        """
        
""" 
