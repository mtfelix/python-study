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

ball_pos = [50,50]
ball_vel = [0.618,0.5]

direction_right = True

paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2

paddle1_vel = 1
paddle2_vel = 1

pad1_keydown_flag = 0 # 0 -- no keydown in action
pad2_keydown_flag = 0 # 0 -- no keydown in action


score1 = 0
score2 = 0

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    #ball_vel = [2, -2]
    sign = 1
    if right == True :
        sign = 1
    else:
        sign = -1
    ball_vel[0] = sign * random.randrange(120, 240) / 60
    ball_vel[1] = - random.randrange(60, 180) / 60
    


# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    global direction_right
    score1 = 0
    score2 = 0
    ball_init(direction_right)
    
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel, direction_right, pad1_keydown_flag, pad2_keydown_flag
 
    # update paddle's vertical position, keep paddle on the screen
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    pad1_new_pos = paddle1_pos + paddle1_vel * pad1_keydown_flag
    if (HALF_PAD_HEIGHT <= pad1_new_pos) and (HEIGHT - HALF_PAD_HEIGHT >= pad1_new_pos):
            paddle1_pos = pad1_new_pos
    pad2_new_pos = paddle2_pos + paddle2_vel * pad2_keydown_flag
    if (HALF_PAD_HEIGHT <= pad2_new_pos) and (HEIGHT - HALF_PAD_HEIGHT >= pad2_new_pos):
            paddle2_pos = pad2_new_pos
    
#    print "in draw, paddle1_vel is ", paddle1_vel;
#    print "in draw, paddle2_vel is ", paddle2_vel;
#    
#    print "in draw, paddle1_pos is ", paddle1_pos;
#    print "in draw, paddle2_pos is ", paddle2_pos;
#    
    pad1_p1 = [0, paddle1_pos - HALF_PAD_HEIGHT]
    pad1_p2 = [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT]
    pad1_p3 = [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT]
    pad1_p4 = [0, paddle1_pos + HALF_PAD_HEIGHT]
    
    pad2_p1 = [WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT]
    pad2_p2 = [WIDTH, paddle2_pos - HALF_PAD_HEIGHT]
    pad2_p3 = [WIDTH, paddle2_pos + HALF_PAD_HEIGHT]
    pad2_p4 = [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]
    
    c.draw_polygon([pad1_p1,pad1_p2,pad1_p3,pad1_p4], 1, "White","White")
    c.draw_polygon([pad2_p1,pad2_p2,pad2_p3,pad2_p4], 1, "White","White")
    
    # update ball
    
    ## vertical collide
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    ## touch/collide gutter
    
    pad1_head = paddle1_pos - HALF_PAD_HEIGHT
    pad1_foot = paddle1_pos + HALF_PAD_HEIGHT
    
    pad2_head = paddle2_pos - HALF_PAD_HEIGHT
    pad2_foot = paddle2_pos + HALF_PAD_HEIGHT
    
    ball_head = ball_pos[1] - BALL_RADIUS
    ball_foot = ball_pos[1] + BALL_RADIUS
    # touch left gutter
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH: #or ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        if pad1_head <= ball_foot and pad1_foot >= ball_head:
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = - ball_vel[1] * 1.1
        else:
            score2 += 1
            direction_right = - direction_right
            ball_init(direction_right)
    # touch right gutter
    if ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        if pad2_head <= ball_foot and pad2_foot >= ball_head:
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = - ball_vel[1] * 1.1
        else:
            score1 += 1
            direction_right = - direction_right
            ball_init(direction_right)
  
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]  
    
    
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "Green", "White")
    c.draw_text(str(score1), (WIDTH / 4 , HEIGHT / 4 ), 60, "White")
    c.draw_text(str(score2), (WIDTH / 4 * 3 , HEIGHT / 4 ), 60, "White")    
    
def keydown(key):
    global paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos, pad1_keydown_flag, pad2_keydown_flag
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= 5
        pad1_keydown_flag = 1
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 5
        pad2_keydown_flag = 1
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 5
        pad1_keydown_flag = 1
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 5
        pad2_keydown_flag = 1
#    print "paddle1_vel is: ", paddle1_vel
#    print "paddle2_vel is: ", paddle2_vel
#    print "paddle1_pos is: ", paddle1_pos
#    print "paddle2_pos is: ", paddle2_pos
#    

def keyup(key):
    global paddle1_vel, paddle2_vel, pad1_keydown_flag, pad2_keydown_flag
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
        pad1_keydown_flag = 0
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
        pad2_keydown_flag = 0
def reset():
    new_game()
    

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
reset_btn = frame.add_button("Restart", new_game, 100)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
