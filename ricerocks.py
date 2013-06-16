# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# info(self, center, size, radius = 0, lifespan = None, animated = False):
# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 30)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40, 1200)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
# def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
explosion_info = ImageInfo([64, 64], [128, 128], 17, 120, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

good_sound = simplegui.load_sound("https://www.dropbox.com/s/no4xabzohgqdv4l/mgod_clip.mp3")
#good_sound = explosion_sound
# ship angle_vel
SHIP_ANGLE_VEL = 0
ANGLE_DELTA = math.pi/30
NAKE_SHIP_POS = [45, 45]
THRUSTER_SHIP_POS = [45+90, 45]
THRUST_SPEED = 3.618
started = False

rock_group = set([])
missile_group = set([])
explosion_group = set([])


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = math.pi/30
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.fwd_vector = [1,1]
        self.thrust_speed = 0
        
    def draw(self,canvas):
        if False == started:
            return
        global NAKE_SHIP_POS, THRUSTER_SHIP_POS
        
        if False == self.thrust:
            self.image_center = NAKE_SHIP_POS
        else:
            self.image_center = THRUSTER_SHIP_POS
        
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
    
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        self.angle += SHIP_ANGLE_VEL
        
        self.fwd_vector = angle_to_vector(self.angle)
        
        if True == self.thrust:
            self.vel[0] = self.fwd_vector[0] * self.thrust_speed
            self.vel[1] = self.fwd_vector[1] * self.thrust_speed
        
        # friction
        self.vel[0] *= 0.99
        self.vel[1] *= 0.99
    
    def set_angle_vel(self, angle_vel):
        self.angle_vel = angle_vel
        
    def set_thrust(self, thrust_on):
        if False == started:
           return
        self.thrust = thrust_on
        if True == thrust_on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
            self.thrust_speed = THRUST_SPEED
        else:
            ship_thrust_sound.rewind()
            self.thrust_speed = 0

    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def shoot(self):
    
        global missile_group
        missile_pos = [0, 0]
        missile_vel = [0, 0]
        
        # compute the cannon tip based on the pos, size and angle
        missile_pos[0] = self.pos[0] + ((self.image_size[0]/2)* math.cos(-self.angle))
        missile_pos[1] = self.pos[1] - ((self.image_size[0]/2)* math.sin(-self.angle))
        
        
        missile_vel[0] = self.vel[0] + self.fwd_vector[0] * 10
        missile_vel[1] = self.vel[1] + self.fwd_vector[1] * 10
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
        
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        
        self.sound = sound
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        
        if True == self.animated:
            self.image_center[0] = 64 + (self.age) * 128
            self.image_size = [64, 128]
        
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        self.angle += self.angle_vel
        
        self.age += 1
        
        if self.age >= self.lifespan:
            return True
        else:
            return False
         
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def collide(self, object):
        if (dist(self.pos, object.get_position()) <= self.radius + object.get_radius()):
            return True
        else:
            return False

def group_collide(group, sprite_object):
    global explosion_group
    num_of_collisions = 0
    remove_set = set([])
    for item in group:
        if True == item.collide(sprite_object):
            remove_set.add(item)
            num_of_collisions += 1
            explosion = Sprite(item.get_position(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
    group.difference_update(remove_set)
    return num_of_collisions
    
def group_group_collide(group1, group2):
    num_of_collisions = 0
    remove_set = set([])
    for p1 in group1:
        if group_collide(group2, p1) > 0:
            num_of_collisions += 1
            #group1.remove(p1)
            remove_set.add(p1)
    group1.difference_update(remove_set)
    return num_of_collisions

def draw(canvas):
    global time, SHIP_ANGLE_VEL, missile_group, rock_group, my_ship, lives, score, started
    
   
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # draw ship and sprites
    my_ship.draw(canvas)
    #a_missile.draw(canvas)
    # update ship and sprites
    my_ship.update()
    
    #a_rock.update()
    #a_missile.update()
    all_set = rock_group.union(missile_group)
    all_set = all_set.union(explosion_group)
    process_sprite_group(all_set, canvas)
    
    # show the results
    canvas.draw_text("Lives:"+str(lives), (10, 50), 40, "Red")
    canvas.draw_text("Scores:"+str(score), (300, 50), 40, "Green")
    
    score += group_group_collide(missile_group, rock_group)
    
    if group_collide(rock_group, my_ship) >= 1:
        lives -= 1
    
    if lives <= 0 or False == started:
        lives = 0
        score = 0
        started = False
        restart()
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
        
    
def restart():
    global time, SHIP_ANGLE_VEL, missile_group, rock_group, my_ship, lives, score, ship_thrust_sound
    missile_group = set([])
    rock_group = set([])
    SHIP_ANGLE_VEL = 0
    score = 0
    ship_thrust_sound.rewind()
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0.5, 0.5], 0, ship_image, ship_info)
    
# timer handler that spawns rocks
def rock_spawner():
    global rock_group, a_missile, started
    if False == started:
        return
    #print len(rock_group)
    if len(rock_group) < 12:
        x = random.randrange(0, WIDTH)
        y = random.randrange(0, HEIGHT)
        pos = [x, y]
        if dist(pos, my_ship.get_position()) < 10:
            return
        vx = random.randrange(0, 50)/5 - 5
        vy = random.randrange(0, 50)/5 - 5
        ang = 0
        ang_vel = (random.randrange(0, 20)/5 - 2) * math.pi/30
        a_rock = Sprite(pos, [vx, vy], ang, ang_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)

def process_sprite_group(group, canvas):
    
    #global rock_group, missile_group
    for item in group:
        if True == item.update():
            group.remove(item)
        else:
            item.draw(canvas)

def keydown(key):
    
    global SHIP_ANGLE_VEL, THRUSTRE_ON, started, good_sound
    
    if False == started:
        return
    # adjust angle
    if key == simplegui.KEY_MAP["left"]:
        SHIP_ANGLE_VEL = -ANGLE_DELTA
    if key == simplegui.KEY_MAP["right"]:
        SHIP_ANGLE_VEL = ANGLE_DELTA
    my_ship.set_angle_vel(SHIP_ANGLE_VEL)
    
    # turn on thrusters
    if key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(True)
    
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
    if key == simplegui.KEY_MAP["g"]:
        good_sound.rewind()
        good_sound.play()

def keyup(key):
    
    global SHIP_ANGLE_VEL, THRUSTRE_ON, started
    if False == started:
        return
    
    # adjust angle
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
        SHIP_ANGLE_VEL = 0
        my_ship.set_angle_vel(SHIP_ANGLE_VEL)
    
    # turn on thrusters
    if key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(False)

def start_click(pos):
    global started, lives
    started = True
    lives = 3
    restart()
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0.5, 0.5], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(start_click)


timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
