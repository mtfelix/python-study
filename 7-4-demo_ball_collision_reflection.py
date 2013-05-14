# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor runs in Chrome 18+, Firefox 11+, and Safari 6+.
# Some features may work in other browsers, but do not expect
# full functionality.  It does NOT run in Internet Explorer.

import simplegui

WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20

ball_pos = [WIDTH / 2, HEIGHT / 2]
vel = [-40 / 10, 5 / 10]

def draw(canvas):
    ball_pos[0] += vel[0]
    ball_pos[1] += vel[1]
    
    if ball_pos[0] <= BALL_RADIUS:
        vel[0] = -vel[0]
    
    if ball_pos[0] >= WIDTH - BALL_RADIUS -1:
        vel[0] = -vel[0]
        
    if ball_pos[1] <= BALL_RADIUS:
        vel[1] = -vel[1]
        
    if ball_pos[1] >= HEIGHT - BALL_RADIUS - 1:
        vel[1] = -vel[1]
    
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

frame = simplegui.create_frame("Demo",WIDTH,HEIGHT)
frame.set_draw_handler(draw)
frame.start()