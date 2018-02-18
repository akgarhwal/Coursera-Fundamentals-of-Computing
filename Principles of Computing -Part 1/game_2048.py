#__author__ = "akgarhwal"
# to play this game go to below link
# Link : http://www.codeskulptor.org/#user44_1DcmASKi8e5Upnu.py

"""
Clone of 2048 game.
"""

import poc_2048_gui
import random
ROWS = 4
COLS = 4


# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # list with all zero
    length = len(line)
    result = [0] * length

    # Shift all number (!=0) to left side of list
    first = last = 0
    while first < length and last < length:
        while last < length and line[last] == 0 :
            last += 1
        if last < length:
            result[first] = line[last]
            last += 1
            first += 1

    #print("Before Merging : ",result)
    # Now merge equal number
    first = last = 0
    while first < length and last < length:
        if last+1 < length and result[last] == result[last+1]:
            result[first] = result[last] + result[last+1]
            if last != first:
                result[last] = 0
            result[last+1] = 0		
            last += 2
        else:
            result[first] = result[last]
            if first != last:
                result[last] = 0	
            last += 1
        first += 1

    return result


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        self._initial_val = {}
        self._initial_val[UP] = []
        self._initial_val[DOWN] = []
        self._initial_val[LEFT] = []
        self._initial_val[RIGHT] = []
        for ind in range(grid_width):
            self._initial_val[UP].append((0,ind))
        for ind in range(grid_width):
            self._initial_val[DOWN].append((grid_height-1,ind))
        for ind in range(grid_height):
            self._initial_val[LEFT].append((ind,0))
        for ind in range(grid_height):
            self._initial_val[RIGHT].append((ind,grid_width-1))
        
        
    def reset(self):
        """
        Reset the game so the _grid is empty except for two
        initial tiles.
        """
        self._grid = [[(0*col*row) for col in range(self._grid_width)] 
                     for row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the _grid for debugging.
        """
        matrix = ''
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                matrix += str(self.get_tile(row,col))
        return matrix

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        prev_state = self.__str__()
        if (direction == UP) :
            self.merge_all(UP)
        elif (direction == LEFT) :
            self.merge_all(LEFT)
        elif (direction == RIGHT) :
            self.merge_all(RIGHT)
        else:
            self.merge_all(DOWN)
        
        cur_state = self.__str__()
        if prev_state != cur_state:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # Distribution of 90% 2 and 10% 4
        dist = [2, 2, 2, 2, 4, 2, 2, 2, 2, 2]
        # Randomly select a zero tile
        new_tile_index = random.choice(self.get_zeros_ind())
        # Replace tile with either a 2 or a 4, selected randomly.
        self._grid[new_tile_index[0]][new_tile_index[1]] = random.choice(dist)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]
    def get_zeros_ind(self):
        """
        Return list of index whoes value is zero in _grid
        """
        zeros = []
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self._grid[row][col] == 0:
                    zeros.append((row,col))
        return zeros
    def merge_all(self,direction):
        """
        Call merge for all gird
        """
        if direction == UP or direction == DOWN:
            step = self.get_grid_height()
        else:
            step = self.get_grid_width()
        #print('step' ,step)
        for val in self._initial_val[direction]:
            temp_lst = []
            #print('val : ',val)
            row,col = OFFSETS[direction]
            for num in range(step):
                #print(val[0]+x,val[1]+x)
                temp_lst.append(self.get_tile(val[0]+(num*row),val[1]+(num*col)))
            #print("BF : ",temp_lst)
            temp_lst = merge(temp_lst)
            #print("AF : ",temp_lst)
            for num in range(step):
                self.set_tile(val[0]+(row*num),val[1]+(col*num),temp_lst[num])
        
        
poc_2048_gui.run_gui(TwentyFortyEight(ROWS, COLS))
