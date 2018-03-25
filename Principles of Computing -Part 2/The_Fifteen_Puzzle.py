# __akgarwal__
# Link to play game : http://www.codeskulptor.org/#user44_mF3gkBhvCL_71.py



"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row]) + ','
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        result = True
        # Tile zero is positioned at (target_row,target_col).
        tile = self.get_number(target_row, target_col)
        if tile != 0:
            result = False
        
        # All tiles in rows target_row+1 or below are positioned at their solved location.
        for row in range(target_row+1,self.get_height()):
            for col in range(self.get_width()):
                row_t,col_t = self.current_position(row,col)
                if row_t != row or col_t != col:
                    result = False
                    break

        # All tiles in row i to the right of position (i,j) are positioned at their solved location.
        for col in range(target_col+1,self.get_width()):
            row_t, col_t = self.current_position(target_row, col)
            if row_t != target_row or col_t != col :
                result = False
                
        return result

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col)
        move_string = ""
        next_row, next_col = self.current_position(target_row, target_col)
        # Same column .
        if target_col == next_col :
            # find number of move in up direction
            diff = target_row - next_row
            move_string += 'u' * diff
            # now start moving tile to its direction
            move_string += 'lddru' * (diff-1)
            # move zero tile to its location for lower_row_invariant
            move_string += 'ld'

        elif target_row == next_row :
            # find number of moce in left direction
            diff = target_col - next_col
            move_string += 'l' * diff
            # move tile to its position one by one
            move_string += 'urrdl' * (diff-1)
        
        else:
            # find direction of next tile
            diff_row = target_row - next_row
            diff_col = abs(target_col - next_col)
            # find direction left or right
            if target_col - next_col > 0:
                # side is left
                side = 'l'
                go_top = 'dru'
                if next_row == 0:
                    move_to_same_col = "drrul"
                else:
                    move_to_same_col = "urrdl"
            else:
                # side is right
                side = 'r'
                go_top = 'dlu'
                if next_row == 0:
                    move_to_same_col = "dllur"
                else:
                    move_to_same_col = "ulldr"

            # move to same row as next_row
            move_string += 'u' * diff_row
            move_string += side * diff_col
            #move to same col
            move_string += (move_to_same_col) * (diff_col - 1)
            move_string += go_top
            # now start moving tile to its direction
            move_string += 'lddru' * (diff_row-1)
            # move zero tile to its location for lower_row_invariant
            move_string += 'ld'
        
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row, target_col-1)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        #assert self.lower_row_invariant(target_row, 0)
        move_string = ""
        next_row, next_col = self.current_position(target_row, 0)

        diff_row = target_row - next_row
        diff_col = next_col  ## :(

        if diff_col == 0 and diff_row == 1 :
            #very easy, just go up and then right
            move_string += 'ur'
            self.update_puzzle('ur')

        else:
            move_string += 'ur'
            self.update_puzzle('ur')
            next_row, next_col = self.current_position(target_row, 0)
            new_target_col = 1
            new_target_row = target_row -1
            # 1.
            if new_target_col == next_col :
                # find number of move in up direction
                diff = new_target_row - next_row
                move_string += 'u' * diff
                # now start moving tile to its direction AND
                # move zero tile to its location for lower_row_invariant
                move_string += 'lddru' * (diff-1) + 'ld'

            elif new_target_row == next_row :

                # find number of move in left direction
                diff = new_target_col - next_col
                if  diff < 0:
                    # new tile is at right side AND
                    # move tile to its position one by one
                    move_string += 'r' * diff + 'ulldr' * (diff-1)
                
                # new tile is at target_row-1, 0
                move_string += 'l'
            
            else:
                # find direction of next tile
                diff_row = new_target_row - next_row
                diff_col = abs(new_target_col - next_col)
                
                # find direction left or right
                if new_target_col - next_col > 0:
                    # side is left
                    side = 'l'
                    go_top = 'dru'
                    if next_row == 0:
                        move_to_same_col = "drrul"
                    else:
                        move_to_same_col = "urrdl"
                else:
                    # side is right
                    side = 'r'
                    go_top = 'dlu'
                    if next_row == 0:
                        move_to_same_col = "dllur"
                    else:
                        move_to_same_col = "ulldr"

                # move to same row as next_row
                move_string += 'u' * diff_row
                move_string += side * diff_col
                #move to same col
                move_string += (move_to_same_col) * (diff_col - 1)
                move_string += go_top
                # now start moving tile to its direction
                move_string += 'lddru' * (diff_row-1)
                # move zero tile to its location for 3X2 move to work
                move_string += 'ld'

            # add 3X2 solve string 
            move_string += "ruldrdlurdluurddlur"
        move_string += 'r' * (self.get_width()-2)
        self.update_puzzle(move_string[2:])
        assert self.lower_row_invariant(target_row-1, self.get_width()-1)
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        result = True
        tile = self.get_number(0, target_col)
        if tile != 0:
            result = False
        # check row 0 right
        for col in range(target_col+1, self.get_width()):
            row_t, col_t = self.current_position(0, col)
            if row_t != 0 or col_t != col :
                result = False
        for col in range(target_col, self.get_width()):
            row_t, col_t = self.current_position(1, col)
            if row_t != 1 or col_t != col :
                result = False
        # below rows
        for row in range(2,self.get_height()):
            for col in range(self.get_width()):
                row_t,col_t = self.current_position(row,col)
                if row_t != row or col_t != col:
                    result = False
                    break
        return result

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        result = True
        tile = self.get_number(1, target_col)
        if tile != 0:
            result = False
        # check row 0 right
        for col in range(target_col+1, self.get_width()):
            row_t, col_t = self.current_position(1, col)
            if row_t != 1 or col_t != col :
                result = False
        # below rows
        for row in range(2,self.get_height()):
            for col in range(self.get_width()):
                row_t,col_t = self.current_position(row,col)
                if row_t != row or col_t != col:
                    result = False
                    break
        return result

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        move_string = "ld"
        target_row = 0
        self.update_puzzle(move_string)
        next_row, next_col = self.current_position(target_row, target_col)

        if next_row != 0 or next_col != target_col :
            diff_row = (target_row+1) - next_row
            diff_col = (target_col-1) - next_col

            if diff_col == 0 and diff_row == 1 :
                #very easy, just go up and then left than down
                move_string += 'uld'

            elif diff_row == 0:
                move_string += 'l' * (diff_col)
                move_string += 'urrdl' * (diff_col - 1)

            else:
                move_string += 'u'
                move_string += 'l' * (diff_col)
                move_string += 'drrul' * (diff_col - 1)
                move_string += 'druld'

            # add 2X3 solve string 
            move_string += "urdlurrdluldrruld"

        self.update_puzzle(move_string[2:])
        assert self.row1_invariant(target_col-1)
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        move_string = ""
        target_row = 1
        next_row, next_col = self.current_position(target_row, target_col)
        # Same column .
        if target_col == next_col :
            # find number of move in up direction
            diff = target_row - next_row
            move_string += 'u' * diff
            # now start moving tile to its direction
            move_string += 'lddru' * (diff-1)

        elif target_row == next_row :
            # find number of moce in left direction
            diff = target_col - next_col
            move_string += 'l' * diff
            # move tile to its position one by one
            move_string += 'urrdl' * (diff-1)
            move_string += 'ur'
        
        else:
            # find direction of next tile
            diff_row = target_row - next_row
            diff_col = target_col - next_col
            # find direction left or right
            if target_col - next_col > 0:
                # side is left
                side = 'l'
                go_top = 'dru'
                if next_row == 0:
                    move_to_same_col = "drrul"
                else:
                    move_to_same_col = "urrdl"
            else:
                # side is right
                side = 'r'
                go_top = 'dlu'
                if next_row == 0:
                    move_to_same_col = "dllur"
                else:
                    move_to_same_col = "ulldr"

            # move to same row as next_row
            move_string += 'u' * diff_row
            move_string += side * diff_col
            #move to same col
            move_string += (move_to_same_col) * (diff_col - 1)
            move_string += go_top
            # now start moving tile to its direction
            move_string += 'lddru' * (diff_row-1)
            # move zero tile to its location for lower_row_invariant
            #move_string += 'ld'
        
        self.update_puzzle(move_string)
        assert self.row0_invariant(target_col)
        return move_string
    
    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        def is_solved():
            """
            Check that upper left 2x2 is solved or not
            """
            row0, col0 = self.current_position(0, 0)
            if row0 != 0 or col0 != 0:
                return False
            row1, col0 = self.current_position(1, 0)
            if row1 != 1 or col0 != 0:
                return False
            row0, col1 = self.current_position(0, 1)
            if row0 != 0 or col1 != 1:
                return False
            row1, col1 = self.current_position(1, 1)
            if row1 != 1 or col1 != 1:
                return False
            return True

        assert self.row1_invariant(1)
        move_string = "ul"
        self.update_puzzle("ul")
        while not is_solved():
            move_string += "drul"
            self.update_puzzle("drul")

        assert self.row0_invariant(0)
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        # move to lower right corner
        cur_row, cur_col = self.current_position(0,0)
        move_string += 'r' * (self.get_width() -1 - cur_col)
        move_string += 'd' * (self.get_height() -1 - cur_row)
        self.update_puzzle(move_string)
        # now start one by one
        for row in range(self.get_height()-1,1,-1):
            for col in range(self.get_width()-1,0,-1):
                result_str = self.solve_interior_tile(row, col)
                move_string += result_str

            result_str = self.solve_col0_tile(row)
            move_string += result_str
     
        # now solve upper row
        for col in range(self.get_width()-1,1,-1):
            # row 1
            result_str = self.solve_row1_tile(col)
            move_string += result_str
            # row 0
            result_str = self.solve_row0_tile(col)
            move_string += result_str

        result_str = self.solve_2x2()
        move_string += result_str
        return move_string
        
