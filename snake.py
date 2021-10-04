

import pygame as pg
import settings
from pygame import gfxdraw
from pygame import Vector2
from snake_fov import FOV
from dna import DNA
from neural_network import Network
from math import sin, cos, radians, degrees, floor
from random import randint, random, choice
import colorsys
import time
import string

color =[(205, 97, 85)]

class Head(pg.sprite.Sprite):
    def __init__(self, rad, col, ratios, id=None):
        pg.sprite.Sprite.__init__(self) #calling parent function init so we don't override it
        #radius is the same as the center of the surface coordinates
        self.image = pg.Surface((rad*2+1, rad*2+1), pg.SRCALPHA, 32) #setting dimensions of surface and making transparent
        self.rect = self.image.get_rect() #fetching rectangle object that has dimensions of the image
        self.rect.center = (settings.SCR_WIDTH/2, settings.SCR_WIDTH/2) #setting position of image in middle of settings.WINdow
        self.lline_angle = 90 #starting with lead line pointed up
        self.lline_amp = 55 #length of lead line
        self.fov_boundary = 120 #+- the current line angle; representing field of view for snake
        self.n_rays = 20 #number of rays that will be cast out from the snake head as sensors
        self.rad = rad
        self.col = col
        self.pos = Vector2(randint(rad*2, settings.SCR_WIDTH-rad*2), randint(rad*2, settings.SCR_HEIGHT-rad*2)) #spawning at random position
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.ID = id
        self.new_dir = 3 #default steer sensitivity for snake
        self.max_speed = ratios["speed"][0]
        self.max_force = ratios["force"][0]
        self.fov_data = []
        self.init_fov()
        
    def init_fov(self):
        self.FOV = FOV(self.pos, self.n_rays) #creating fov object for snake (creating eyes for snake)
        self.fov_boundaries = self.lline_angle + self.fov_boundary, self.lline_angle - self.fov_boundary #updating fov for snake head
        self.fov_data = self.FOV.update(settings.WIN, self.pos, self.fov_boundaries, self.ID, False)
        
    def update(self, new_direction, show_fov):
        self.new_dir = new_direction
        self.line_pos = self.lead_line() #getting position of our target line we want to approach
        self.acc = self.seek((self.line_pos)) #steering velocity is our acceleration in for given target in that direction
        
        self.vel += self.acc #adding acc to vel b/c vel is change in acceleration
        if self.vel.length() > self.max_speed: #making sure it's length (magnitude) is not greater than max speed
            self.vel.scale_to_length(self.max_speed)
        
        self.lline_angle = (self.lline_angle + self.new_dir) % 360 #upating lead line direction
        
        self.fov_boundaries = self.lline_angle + self.fov_boundary, self.lline_angle - self.fov_boundary #updating fov boundaries for snake head
        #MUST LOOP AGAIN BEFORE ADDING ANOTHER BATCH TO FOV_DATA ** FIX THIS **
        #for i in range(settings.BATCH_SIZE):
        #    self.fov_data[i] = self.FOV.update(settings.WIN, self.pos, self.fov_boundaries, self.ID, show_fov)
        self.fov_data = self.FOV.update(settings.WIN, self.pos, self.fov_boundaries, self.ID, show_fov)

        self.pos += self.vel #adding vel to position
        if self.pos.x > settings.SCR_WIDTH:
            self.pos.x = settings.SCR_WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y > settings.SCR_HEIGHT:
            self.pos.y = settings.SCR_HEIGHT
        if self.pos.y < 0:
            self.pos.y = 0                
                
        self.rect.center = self.pos #updating the rect object position
        self.draw()
    
    def draw(self):
        pg.gfxdraw.aacircle(self.image, self.rad, self.rad, self.rad, self.col) #drasettings.WINg our circle onto sprite image
        pg.gfxdraw.filled_circle(self.image, self.rad, self.rad, self.rad, self.col)
        #pg.draw.circle(self.image, self.col, (self.rad, self.rad), self.rad)
        settings.WIN.blit(self.image, self.rect)

    def seek(self, target_pos):
        #desired vel = target pos - current pos
        self.line_pos = target_pos
        self.desired_vel = (target_pos - self.pos).normalize() * self.max_speed #getting our desired velocity vector that points to target pos. length will be max speed
        steer_force = (self.desired_vel - self.vel) ##steering force = desired vel - current vel
        #print("Raw Steer Force:", steer_force)
        if steer_force.length() > self.max_force: #making sure speed of steer vector is not greater than max force
            steer_force.scale_to_length(self.max_force) #scales length to max force if greater than max force (length == magnitude of vector == speed)
            #print("!!STEER ABOVE MAX FORCE!!")
            #print("Steer Force Scaled Down:", steer_force)
        return steer_force
    
    def lead_line(self): #calculates the position of the "lead" for the snake to follow
        #print("angle:", self.lline_angle)
        x2 = (cos(radians(self.lline_angle)) * self.lline_amp) #the return value is also multiplied by the value in the AMPLITUDE variable, so that instead of ranging over -1.0 to 1.0, it will range between (-1.0 * AMPLITUDE) to (1.0 * AMPLITUDE)
        y2 = -1 *(sin(radians(self.lline_angle)) * self.lline_amp) #multiplying by -1 b/c y coord increase going down
        x2 = x2 + self.pos.x
        y2 = y2 + self.pos.y
        #position of rear of head
        #rear_x2 = (cos(radians(self.lline_angle)) * self.rad)
        #rear_y2 = -1 *(sin(radians(self.lline_angle)) * self.rad)
        #self.rear_pos = -1*rear_x2 + self.pos.x, -1*rear_y2+self.pos.y #rear position of head
        return  x2, y2

    def draw_vectors(self):
        line_width = 3
        scale = .35 * self.lline_amp
        #desired velocity
        pg.draw.line(settings.WIN, settings.WHITE, self.pos, (self.pos + self.desired_vel * scale), line_width) #line representing velocity
        #current velocity
        pg.draw.line(settings.WIN, settings.GREEN, self.pos, (self.pos + self.vel * scale), line_width)
        self.draw() #overlapping vector lines with snake head    
    
class Segment(Head):
    def __init__(self, x, y, rad, col, ratios):
        Head.__init__(self, rad, col, ratios)#,None)
        self.pos = Vector2(x,y)
        self.approach_radius = 55
        self.max_speed = ratios["speed"][1]
        self.max_force = ratios["force"][1]
    
    def init_fov(self, *kwargs): pass #overriding init_fov for segment class 
        
    def seek_w_approach(self, target_pos):
        #steering force = desired vel - current vel
        self.line_pos = target_pos
        #self.line_pos = self.line_pos.x + self.rad, self.line_pos.y + self.rad
        self.desired_vel = (target_pos - self.pos)#getting our desired velocity vector that points to target pos. length will be max speed
        distance = self.desired_vel.length() #getting distance from current pos to desired
        
        #print("Distance:", distance)
        try:
            self.desired_vel.normalize_ip()
        except:
            print("Cannot normalize vector length of 0") 
        #print("Normalized Distance:", norm)
        
        if distance < self.approach_radius: #if we have traveled passed the approach radius limit
            self.desired_vel *= distance / self.approach_radius * self.max_speed #distance / approach_radius = distance to center of circle (a fraction; slowly shortening desired velocity
        else:
            self.desired_vel *= self.max_speed 
            
        steer_force = (self.desired_vel - self.vel) #getting steer force
        if steer_force.length() > self.max_force: #making sure speed of steer vector is not greater than max force
            steer_force.scale_to_length(self.max_force) #scales length to max force if greater than max force
        return steer_force
    
    def update(self, target):
        self.acc = self.seek_w_approach((target)) #steering velocity is our acceleration in for given target in that direction
        self.vel += self.acc #adding acc to vel b/c vel is change in acceleration
        if self.vel.length() > self.max_speed: #making sure it's length (magnitude) is not greater than max speed
             self.vel.scale_to_length(self.max_speed)
        
        self.pos += self.vel #adding vel to position
        if self.pos.x > settings.SCR_WIDTH:
            self.pos.x = settings.SCR_WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y > settings.SCR_HEIGHT:
            self.pos.y = settings.SCR_HEIGHT
        if self.pos.y < 0:
            self.pos.y = 0                
                    
        self.rect.center = self.pos #updating the rect object position
        self.draw()        

    def draw(self):
        pg.gfxdraw.aacircle(self.image, self.rad, self.rad, self.rad, self.col) #drasettings.WINg our circle onto sprite image
        pg.gfxdraw.filled_circle(self.image, self.rad, self.rad, self.rad, self.col)
        settings.WIN.blit(self.image, self.rect)
    
    def draw_vectors(self):
        line_width = 3
        try:
            amp = 15
            pg.draw.line(settings.WIN, settings.WHITE, self.pos, (self.line_pos), line_width) #desired velocity
            pg.draw.line(settings.WIN, settings.GREEN, self.pos, (self.pos + self.vel * amp), line_width) #current velocity
            #pg.draw.circle(settings.WIN, settings.YELLOW, self.line_pos, self.approach_radius, 1) #approach radius
            #pg.draw.line(settings.WIN, BLUE, self.pos, self.rear_pos, self.line_width)
        except:
            pass
    
class Snake():
    def __init__(self, radius, ratios, network_struct, dna=None):
        self.radius = radius
        self.alpha_val = 245 #transparency value for color
        self.ratios = ratios
        #CREATE RANDOM DNA HERE THEN PASS TO NEURAL NETWORK (BRAIN)
        #APPEND COLOR VAL ONTO END OF DNA TO SHOW INHERITANCE
        
        #self.color_rgb = self.gen_color() #generating random color for snake
        if not dna:
            self.color_rgb = self.gen_color()
            self.DNA = DNA(network_struct)
            self.DNA.data.append(self.color_rgb)
        else:
            self.DNA = dna
            self.color_rgb = self.DNA.data[-1]
            self.color_rgb.append(self.alpha_val)
        
        self.brain = Network(network_struct, self.DNA.data[:-1]) 

        self.tint_val = list(self.color_rgb) #tint color for next snake segment
        #self.tint_multiplier = 0.05
        self.ID = "".join(choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8)) #generating random string with uppercase, lowercase, & digits for id
        self.head = Head(radius, self.color_rgb, ratios, self.ID)
        self.body = [self.head]
        self.hunger_interval = 3000
        self.age_interval = 1000
        self.new_hunger_time = pg.time.get_ticks() + self.hunger_interval
        self.new_age_time = pg.time.get_ticks() + self.age_interval
        self.age_incr = 0.1
        self.age = 0 #represents how long the snake has been not_dying
        self.size = 1
        self.hunger = 0 #will be addded to health 
        self.food_eaten = 0
        self.food_bonus = 15 #added to health everytime a food is eaten
        self.health = 30
        self.dead = False
        self.death_fade = False
        self.collision_ratio = 0.65 #1 is the same size, 2 is twice as big and 0.5 is half the size
        self.raw_fov_data = self.head.fov_data #input data for neural network
        
    def gen_color(self): #https://stackoverflow.com/questions/43437309/get-a-bright-random-colour-python
        h,s,l = random(), 0.5 + random()/2.0, 0.4 + random()/5.0 #randomly chooses light colored rgb values
        r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
        return [r, g, b, self.alpha_val]
    
    def update(self, show_vectors, show_fov):
        if not self.death_fade:
            new_direction = self.brain.think(self.head.fov_data) #running neural network to produce new direction
            self.head.update(new_direction, show_fov) #updating snake head pos on screen
            self.raw_fov_data = self.head.fov_data #giving fov_data to snake class for easier access
            for i in range(1, self.size): #updating snake position
                self.body[i].update((self.body[i-1].pos)) #updating snake body on screen 
            if show_vectors:
                for segment in self.body:
                    segment.draw_vectors()
        else:
            for i in range(0, self.size): #starting death fade
                self.body[i].col[-1] -= 5
                self.body[i].draw()
                if self.body[i].col[-1] == 0:
                    self.dead = True
        
    def check_collisions(self, food):
        current_time = pg.time.get_ticks() #getting current time in game
        if self.size > settings.EXCLUDE_SEGMENTS: #making sure snake is long enough to detect collision
            for i in range(settings.EXCLUDE_SEGMENTS, self.size): #checking for collision with itself (not counting first [EXCLUDE_SEGMENTS] segments)
                if pg.sprite.collide_circle_ratio(self.collision_ratio)(self.head, self.body[i]): #checking for collision b/w head and segments after [EXCLUDE_SEGMENT-1] index
                    self.death_fade = True
        if self.head.rect.left < 0 or self.head.rect.top < 0 or self.head.rect.right > settings.SCR_WIDTH or self.head.rect.bottom > settings.SCR_HEIGHT: #checking collision with wall
            self.death_fade = True
            
        if current_time > self.new_age_time: 
            self.age += self.age_incr #increasing of age every [age_incr]
            self.new_age_time = pg.time.get_ticks() + self.age_interval
        if self.health > 0: #snake dies if current time exceeds starvation time
            if self.head.rect.colliderect(food): #if head collides with food
                self.append() #appending segment to snake
                food.reset() #resetting food position in window
                self.size += 1
                self.food_eaten += 1
                self.health += self.food_bonus + self.food_eaten
            self.health -= 0.01
        else: 
            self.health = 0
            self.death_fade = True
            
    def append(self):
        for i in range(len(self.tint_val)-1):
            self.tint_val[i] = round(self.tint_val[i] + ((255 - self.tint_val[i]) * 0.005)) #creating lighter tint rgb val for segment
        prev_pos = self.body[-1].pos #getting last segment pos
        new_pos = -3 * self.body[-1].vel #getting last segment vel and mult by a negative to get opposite velocity
        new_pos += prev_pos #adding inverted vel to prev position to get new position 
        seg = Segment(new_pos.x, new_pos.y, self.radius, self.tint_val[:], self.ratios) #appending new segment directly behind last segment
        self.body.append(seg)
