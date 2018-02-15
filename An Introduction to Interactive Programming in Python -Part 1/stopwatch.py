# __akgarhwal__
# Game Stopwatch 
# link : http://www.codeskulptor.org/#user44_ysdS8OPyRJmQheC.py

# template for "Stopwatch: The Game"
import simplegui


# define global variables
watch_time = 0
success_stop = 0
total_stop = 0
running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    M = (t/10)/60
    t = t - M*600
    S = (t/10)
    MS = (t%10)
    if S < 10:
        S = "0"+str(S)
        
    return (str(M)+":"+str(S)+"."+str(MS))
  
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    t.start()
    global running
    running = True
    

def stop():
    t.stop()
    global total_stop
    global success_stop
    global running
    if running:
        running = False
        total_stop += 1
        if watch_time%10 == 0:
            success_stop += 1
    

def reset():
    global watch_time
    global total_stop
    global success_stop
    global running 
    runnign  = False
    total_stop = 0 
    success_stop = 0
    watch_time = 0
    t.stop()
    

# define event handler for timer with 0.1 sec interval

def timer():
    global watch_time
    watch_time += 1

# define draw handler
def draw(canvas):
    global watch_time
    global success_stop
    global total_stop
    canvas.draw_text(format(watch_time), (60, 180), 80, 'White')
    canvas.draw_text(str(success_stop) + " / "+str(total_stop), (200, 50), 30, 'Green')
    
    
    
# create frame
f = simplegui.create_frame("Stopwatch: The Game", 300, 300)

# register event handlers
f.set_draw_handler(draw)
f.add_button("Start", start, 150)
f.add_button("Stop", stop, 150)
f.add_button("Reset", reset, 150)
t = simplegui.create_timer(100, timer)

# start frame
f.start()
# Please remember to review the grading rubric
