# simple state example for Memory

import simplegui
     
# define event handlers
def init():
    global state
    state = 0
    
def buttonclick():
    global state
    if state == 0:
        state = 1
    elif state == 1:
        state = 2
    else:
        state = 1    
                         
def draw(canvas):
    if state == 0:
        canvas.draw_text("Game beginning", [30, 62], 24, "White")
    elif state == 1:
        canvas.draw_text("One card exposed", [30, 62], 24, "White")
    else:
        canvas.draw_text("Two cards exposed", [30, 62], 24, "White")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory states", 300, 100)
frame.add_button("Restart", init, 200)
frame.add_button("Simulate mouse click", buttonclick, 200)

# initialize global variables
init()

# register event handlers
frame.set_draw_handler(draw)

# get things rolling
frame.start()
