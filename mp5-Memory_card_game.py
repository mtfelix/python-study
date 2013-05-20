# implementation of card game - Memory

import simplegui
import random

card_deck = range(8) + range(8)

paired  = {}
exposed = [False] * 16


state = 0
p1 = -100
p2 = -100

turn_num = 0

# helper function to initialize globals
def init():
    global exposed, card_deck, state, p1, p2, paired, turn_num
    card_deck = range(8) + range(8)
    random.shuffle(card_deck)
    exposed = [False] * 16
    state = 0
    p1 = -100
    p2 = -100
    paired = {}
    turn_num = 0

     
# define event handlers
def mouseclick(pos):
    global state, p1, p2, turn_num
    card_index = pos[0] // 50

    # add game state logic here
    
    if state == 0:
        if False == exposed[card_index]:
            exposed[card_index] = True
        state = 1
        p1 = card_index
        
    elif state == 1:
        if False == exposed[card_index]:
            exposed[card_index] = True
        state = 2
        p2 = p1
        p1 = card_index
        
    else:
        turn_num += 1
        if card_deck[p1] == card_deck[p2] and p1 != p2:
            exposed[p1] = True
            exposed[p2] = True
            paired[p1] = 1
            paired[p2] = 1

        else:
            if p1 not in paired:
                exposed[p1] = False
            if p2 not in paired:
                exposed[p2] = False            
            
        if False == exposed[card_index]:
            exposed[card_index] = True
            
        state = 1
        p2 = -100
        p1 = card_index

                    
# cards are logically 50x100 pixels in size    
def draw(c):
    global turn_num
    i = 0
    for n in card_deck:
        if True == exposed[i]:
            c.draw_text(str(n), [i * 50 + 12.5, 75], 50, "white")
        else:
            c.draw_polygon([[i * 50, 0], [ (i + 1) * 50, 0], [(i + 1) * 50, 100], [ i * 50, 100]], 2, "yellow", "green")
        c.draw_line(( i * 50, 0), (i * 50, 100), 1, "Blue")
        i += 1
        
    label.set_text("Moves = " + str(turn_num))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", init)
label = frame.add_label("Moves = 0")


# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()


# Always remember to review the grading rubric