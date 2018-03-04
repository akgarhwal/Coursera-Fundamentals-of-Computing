## __akgarhwal__
## Link : http://www.codeskulptor.org/#user44_phcxKL906m_32.py


"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided
import random

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(10)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def switch_player(player):
    """
    swtitch player from X to O and O to X
    """
    if player == provided.PLAYERO:
        return provided.PLAYERX
    return provided.PLAYERO

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    _board = board.clone()
    winner = _board.check_win()
    if winner:
        return SCORES[winner],(-1,-1)
    
    if player == provided.PLAYERX:
        score = -2
    else:
        score = 2
    empty_square = _board.get_empty_squares()
    _fin_move = None
    
    for _move in empty_square:
        __board = _board.clone()
        __board.move(_move[0],_move[1], player) 
        result = mm_move(__board,switch_player(player))
        if player == provided.PLAYERX:
            if score < result[0] :
                score = max(score,result[0])
                _fin_move = _move
        else:
            if score > result[0] :
                score = min(score,result[0])
                _fin_move = _move
                
    return score, _fin_move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    
    move = mm_move(board, player)
    #assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
