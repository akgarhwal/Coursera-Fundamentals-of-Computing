## __akgarhwal__
#Link : http://www.codeskulptor.org/#user44_OutsuTDbpFg0OGf.py

"""
Cookie Clicker Simulator
"""

import simpleplot
import math
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(40)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 16

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies_produced = 0.0
        self._total_cookies = 0.0
        self._current_time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        _res = "\nTotal cookies Produced = "+str(self._total_cookies_produced)
        _res += "\nTotal Cookies = "+str(self._total_cookies)
        _res += "\nCPS = "+str(self._cps)
        _res += "\nTime = "+str(self._current_time) 
        return _res
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._total_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        _copy_his = list(self._history)
        return _copy_his

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._total_cookies > cookies:
            return 0.0
        _time = (cookies - self._total_cookies) / self._cps
        return math.ceil(_time)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._current_time += time
            self._total_cookies_produced += self._cps * time
            self._total_cookies += self._cps * time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._total_cookies :
            self._total_cookies -= cost
            self._cps += additional_cps
            self._history.append((self._current_time, item_name, cost, self._total_cookies_produced))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    
    _build_info = build_info
    _obj = ClickerState()
    _cur_time = 0
    while True :
        _cur_time = _obj.get_time()
        if _cur_time > duration :
            break
        _cookies = _obj.get_cookies()
        _cps = _obj.get_cps()
        _time_left = duration - _cur_time
        _item = strategy(_cookies, _cps, _obj.get_history(), _time_left, _build_info)
        
        if _item != None:
            _cost = build_info.get_cost(_item)
            _cps = build_info.get_cps(_item)
            _time_req = _obj.time_until(_cost)
            if _time_req + _cur_time > duration :
                break
            _obj.wait(_time_req)
            _obj.buy_item(_item,_cost,_cps)
            _build_info.update_item(_item)
        else:
            break
    #print((_obj.get_history()))
    _obj.wait(duration - _obj.get_time())
    return _obj


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    _total_cookies = cookies + (cps * time_left)
    _item_list = build_info.build_items()
    _cheap_item = None
    _cheap_cost = float("inf")
    for _item in _item_list:
        _cost = build_info.get_cost(_item)
        if _cost <= _total_cookies and _cheap_cost > _cost:
            _cheap_cost = _cost
            _cheap_item = _item
            
    return _cheap_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    _total_cookies = cookies + (cps * time_left)
    _item_list = build_info.build_items()
    _exp_item = None
    _exp_cost = float("-inf")
    for _item in _item_list:
        _cost = build_info.get_cost(_item)
        if _cost <= _total_cookies and _exp_cost < _cost:
            _exp_cost = _cost
            _exp_item = _item
            
    return _exp_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    var = provided.BuildInfo({'Cursor': [15.0, 50.0]}, 1.15)
    state = simulate_clicker(var, time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

