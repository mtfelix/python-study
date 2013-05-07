# template for "Stopwatch: The Game"

import simplegui
import time

# define global variables
tenth_second = 0
second = 0
minute = 0
count = 0
running_status = False
stop_win_num = 0
stop_tot_num = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global tenth_second, second, minute
    minute = t // 600
    second = (t // 10) % 60
    tenth_second = t % 10
    return '%d:%02d.%d'%(minute,second,tenth_second)

# define event handlers for buttons; "Start", "Stop", "Reset"
def Start():
    global runining_status
    t.start()
    runining_status = True

def Stop():
    global runining_status, stop_tot_num, stop_win_num
    
    t.stop()
    if True == runining_status:
        stop_tot_num += 1
        if 0 == count % 10:
            stop_win_num += 1
    runining_status = False
    
def Reset():
    global runining_status, tenth_second, second, minute, count, stop_win_num, stop_tot_num
    status = 0 # stand for reset
    tenth_second = 0
    second = 0
    minute = 0
    count = 0
    stop_win_num = 0
    stop_tot_num = 0
    t.stop()
    runining_status = False

    
    
# define event handler for timer with 0.1 sec interval
def update():
    global count
    count += 1


# define draw handler
def draw(canvas):
    time = format(count)
    canvas.draw_text(time, [80,150], 40, "white")
    win_rate = str(stop_win_num) + "/" + str(stop_tot_num)
    col_pos = 300-len(win_rate)*10
    canvas.draw_text(win_rate, [col_pos,20], 20, "green")

# create frame
f = simplegui.create_frame("Stopwatch Game",300,300)
start_btn = f.add_button("Start", Start)
stop_btn = f.add_button("Stop", Stop)
reset_btn = f.add_button("Reset", Reset)

t = simplegui.create_timer(100, update)


# register event handlers
f.set_draw_handler(draw)

# start frame
f.start()


# Please remember to review the grading rubric
