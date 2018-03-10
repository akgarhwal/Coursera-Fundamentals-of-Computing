"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    ans = []
    for _word in list1:
        if _word not in ans:
            ans.append(_word)
    return ans

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    new_list = list1 + list2
    ans = []
    for _word in new_list :
        if _word in list1 and _word in list2 and _word not in ans:
            ans.append(_word)
    return ans

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    merge_list = []
    _ind1 = _ind2 = 0
    while _ind1 < len(list1) and _ind2 < len(list2) :
        if list1[_ind1] < list2[_ind2]:
            merge_list.append(list1[_ind1])
            _ind1 += 1
        else:
            merge_list.append(list2[_ind2])
            _ind2 += 1
    
    merge_list.extend(list1[_ind1:])
    merge_list.extend(list2[_ind2:])
    return merge_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    low = 0
    high = len(list1)
    med = (low + high) // 2
    if high-low > 1:
        _left = merge_sort(list1[0:med])
        _right = merge_sort(list1[med:high])
        list1 = merge(_left,_right)
    return list1

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """a
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    return ['',word]

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    words = []
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    for line in netfile.readlines():
        words.append(line)
    return words

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()
#print(merge([1,2,3],[4,5,6]))
#print( merge_sort([6,3,5,4,3,2,1]) )
    
    
