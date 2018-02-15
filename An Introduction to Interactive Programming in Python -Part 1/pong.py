# _author_ = 'akgarhwal'
# to Play this game open below link
# link : http://www.codeskulptor.org/#user44_OIodC3QHbGmVlX5.py


# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [0, 0]
paddle1_vel = paddle2_vel = 0
score_left = score_right = 0
START = False
# increase velo 
def timer_handler():
    global ball_vel
    if ball_vel[0] < 0:
        ball_vel[0] -= 1
    else:
        ball_vel[0] += 1
    if ball_vel[1] < 0:
        ball_vel[1] -= 1
    else:
        ball_vel[1] += 1
    
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_vel = [0, 0]
    vel_h = random.randrange(2,6)
    vel_v = random.randrange(2,6)
    if direction == "RIGHT":
        ball_vel = [vel_h,-vel_v]
    elif direction == "LEFT":
        ball_vel = [-vel_h,-vel_v]
    else:
        ball_vel = [vel_h,vel_v]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global score_left, score_right
    score_left = score_right = 0
    paddle1_pos = HEIGHT // 2
    paddle2_pos = HEIGHT // 2
    ## spawn_ball
    spawn_ball("RIGHT")

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global score_left, score_right
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    
    
    # update ball
    if START :
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
    #if ball_pos[0] <= BALL_RADIUS+8:
    #    ball_vel[0] = - ball_vel[0]
        
    #if ball_pos[0] >= WIDTH-BALL_RADIUS-8:
    #    ball_vel[0] = - ball_vel[0] 
        
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    if ball_pos[1] >= HEIGHT-BALL_RADIUS:
        ball_vel[1] = - ball_vel[1] 
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "Red", "Yellow")

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos+paddle1_vel >= HALF_PAD_HEIGHT and paddle1_pos+paddle1_vel <= HEIGHT-HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos+paddle2_vel >= HALF_PAD_HEIGHT and paddle2_pos+paddle2_vel <= HEIGHT-HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_line((0, paddle1_pos - HALF_PAD_HEIGHT), (0, paddle1_pos + HALF_PAD_HEIGHT), PAD_WIDTH+4, 'White')
    canvas.draw_line((WIDTH, paddle2_pos - HALF_PAD_HEIGHT), (WIDTH, paddle2_pos + HALF_PAD_HEIGHT), PAD_WIDTH+4, 'White')
    
    # determine whether paddle and ball collide    
    if ball_pos[0] <= BALL_RADIUS+8:
        if ball_pos[1]-BALL_RADIUS//2 >= paddle1_pos+HALF_PAD_HEIGHT or ball_pos[1]+BALL_RADIUS//2 <= paddle1_pos-HALF_PAD_HEIGHT:
            spawn_ball("RIGHT")
            score_right += 1
        else:
            ball_vel[0] = - ball_vel[0]
    if ball_pos[0] >= WIDTH-BALL_RADIUS-8:
        if ball_pos[1]-BALL_RADIUS//2 >= paddle2_pos+HALF_PAD_HEIGHT or ball_pos[1]+BALL_RADIUS//2 <= paddle2_pos-HALF_PAD_HEIGHT:
            spawn_ball("LEFT")
            score_left += 1
        else:
            ball_vel[0] = - ball_vel[0]
    
            
    # draw scores
    canvas.draw_text(str(score_left), (WIDTH // 4, 70), 40, 'Green')
    canvas.draw_text(str(score_right), ((WIDTH // 4) * 3, 70), 40, 'Red')
def keydown(key):
    global START
    START = True
    vel = 5
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = vel
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -vel
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = vel
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -vel 
    
   
def keyup(key):
    vel = 0
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = vel
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = vel
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = vel
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = vel

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', new_game)
timer = simplegui.create_timer(5000, timer_handler)
timer.start()
# start frame
new_game()
frame.start()
