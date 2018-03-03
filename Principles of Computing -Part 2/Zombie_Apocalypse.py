## __akgarhwal__
# link : http://www.codeskulptor.org/#user44_FH24svvxYERnJ3i.py

"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Queue:
    """
    A simple implementation of a FIFO queue.
    """

    def __init__(self):
        """ 
        Initialize the queue.
        """
        self._items = []

    def __len__(self):
        """
        Return the number of items in the queue.
        """
        return len(self._items)
    
    def __iter__(self):
        """
        Create an iterator for the queue.
        """
        for item in self._items:
            yield item

    def __str__(self):
        """
        Return a string representation of the queue.
        """
        return str(self._items)

    def enqueue(self, item):
        """
        Add item to the queue.
        """        
        self._items.append(item)

    def dequeue(self):
        """
        Remove and return the least recently inserted item.
        """
        return self._items.pop(0)

    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items = []
        


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._human_list = []
        self._zombie_list = []
        poc_grid.Grid.clear(self)
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)    
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for _zombie in self._zombie_list:
            yield _zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for _human in self._human_list:
            yield _human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        _height = poc_grid.Grid.get_grid_height(self)
        _width = poc_grid.Grid.get_grid_width(self)
        visited = poc_grid.Grid(_height, _width)
        for _row in range(visited.get_grid_height()):
            for _col in range(visited.get_grid_width()):
                visited.set_empty(_row,_col)

        distance_field = [[(_width * _height) for _row in range(_width)] for _col in range(_height)]
        boundary = Queue()
        if HUMAN == entity_type:
            for _human in self._human_list:
                boundary.enqueue(_human)
                visited.set_full(_human[0],_human[1])
                distance_field[_human[0]][_human[1]] = 0
        else:
            for _zombie in self._zombie_list:
                boundary.enqueue(_zombie)
                visited.set_full(_zombie[0],_zombie[1])
                distance_field[_zombie[0]][_zombie[1]] = 0

        while len(boundary) :
            current_cell = boundary.dequeue()
            for _cell in visited.four_neighbors(current_cell[0],current_cell[1]):
                if poc_grid.Grid.is_empty(self,_cell[0],_cell[1]) and visited.is_empty(_cell[0],_cell[1]):
                    boundary.enqueue(_cell)
                    visited.set_full(_cell[0],_cell[1])
                    distance_field[_cell[0]][_cell[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
        
        
        
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for _index in range(len(self._human_list)):
            _human = self._human_list[_index]
            _max_d = zombie_distance_field[_human[0]][_human[1]]
            _human_next = _human
            for _cell in poc_grid.Grid.eight_neighbors(self, _human[0], _human[1]):
                if _max_d < zombie_distance_field[_cell[0]][_cell[1]] and poc_grid.Grid.is_empty(self,_cell[0],_cell[1]):
                    _max_d = zombie_distance_field[_cell[0]][_cell[1]]
                    _human_next = _cell
            self._human_list[_index] = _human_next
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for _index in range(len(self._zombie_list)):
            _zombie = self._zombie_list[_index]
            _min_d = human_distance_field[_zombie[0]][_zombie[1]]
            _zombie_next = _zombie
            for _cell in poc_grid.Grid.four_neighbors(self, _zombie[0], _zombie[1]):
                if _min_d > human_distance_field[_cell[0]][_cell[1]] and poc_grid.Grid.is_empty(self,_cell[0],_cell[1]):
                    _min_d = human_distance_field[_cell[0]][_cell[1]]
                    _zombie_next = _cell
            self._zombie_list[_index] = _zombie_next

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30,40))
