import simplegui

point_pos = [10,20]
vel = [1,1]
acc = [1.1,1.1]

rec_pos = [50,50]
width = 130
height = 90

def tick():
    point_pos[0] += vel[0]
    point_pos[1] += vel[1]
    vel[0] += acc[0]
    vel[1] += acc[1]
    
def draw(canvas):
    canvas.draw_circle(point_pos, 1, 5, "Red")
    canvas.draw_polygon([(50, 50), (180, 50), (180, 140), (50, 140)], 1, "Green")


f = simplegui.create_frame("Demo",300,300)
f.set_draw_handler(draw)

t = simplegui.create_timer(100,tick)
f.start()
t.start()