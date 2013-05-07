# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor runs in Chrome 18+, Firefox 11+, and Safari 6+.
# Some features may work in other browsers, but do not expect
# full functionality.  It does NOT run in Internet Explorer.

import simplegui

def draw(canvas):
    canvas.draw_circle([150,150],80,2,"black","yellow")
    canvas.draw_circle([150,150],70,2,"black","red")
    canvas.draw_circle([150,150],60,2,"black","green")
    canvas.draw_circle([150,150],50,2,"black","blue")
    canvas.draw_circle([150,150],40,2,"black","white")
    canvas.draw_circle([150,150],30,2,"black","purple")
    canvas.draw_circle([150,150],20,2,"black","yellow")
    canvas.draw_circle([150,150],10,2,"black","yellow")
    canvas.draw_circle([150,150],5,2,"black","red")
    
    #canvas.draw_circle([210,200],20,10,"green")
    

f = simplegui.create_frame("Person",300,300)
f.set_draw_handler(draw)
f.start()
