# __akgarhwal__
#Link : http://www.codeskulptor.org/#user44_MLn4jNvEAO7XPWe.py

"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    _score = 0
    _arr = {}
    for _num in hand:
        if _num in _arr:
            _arr[_num] += 1
        else:
            _arr[_num] = 1
    for _num in _arr:
        _score = max(_score,_num*_arr[_num])
    
    return _score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    _sides = [(_num+1) for _num in range(num_die_sides)]
    all_poss_com = gen_all_sequences(tuple(_sides),num_free_dice)
    ans = 0.0
    for _temp in all_poss_com:
        #print(score(_temp+held_dice))
        ans += score(_temp+held_dice)
    ans = ans / len(all_poss_com)
    #print(ans)
    return ans


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    res = [tuple()]
    index = 0
    while index < pow(2,len(hand)):
        temp = []
        for _num in range(len(hand)):
            bit = (index >> _num) & 1
            if bit :
                temp.append(hand[_num])
        index += 1
        res.append(tuple(temp))
    return set(res)



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    print(all_holds)
    expected_val = 0.0
    res_hand = ()
    for _hold in all_holds:
        _temp_e_val = expected_value(_hold, num_die_sides, len(hand)-len(_hold))
        if _temp_e_val  > expected_val :
            expected_val = _temp_e_val
            res_hand = _hold
    return (expected_val, (res_hand))


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
