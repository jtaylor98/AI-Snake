import pygame as pg
import settings
from math import sin, cos, radians, sqrt, ceil

class Ray:
    def __init__(self, pos, angle):
        self.x = pos[0]
        self.y = pos[1]
        self.dir = cos(radians(angle)), -1 * sin(radians(angle))
        self.closest_point = None
        self.closest_key = None
        self.none = 1000000
        self.barriers_distance = {"Wall": self.none, "Food": self.none, "Segment": self.none} # none means ray has no contact with that barrier at all
    
    def update_barrier_distance(self, key, distance, intersect_pts):    
        self.barriers_distance[key] = distance if distance != None else self.none #updating barriers distance
        self.closest_key = min(self.barriers_distance, key=self.barriers_distance.get) #getting minimum dist in dictionary and updating shortest dist key
        self.closest_point = intersect_pts if intersect_pts is not None else self.closest_point #updating closest intersect point
        #print("closest point:", self.closest_point)
        
    def check_collision(self, wall):
        x1 = wall[0][0]
        y1 = wall[0][1]
        x2 = wall[1][0]
        y2 = wall[1][1]
        
        x3 = self.x
        y3 = self.y
        x4 = self.x + self.dir[0] #ray direction is angle of boundary
        y4 = self.y + self.dir[1]

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4) #denom
        if den == 0: #two lines are parallel and don't touch
            return None #parallel
        else:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
            if (t > 0 and t < 1) and u > 0: #there is an intersection point if true
                x = x1 + t * (x2 - x1) #getting intersection points
                y = y1 + t * (y2-y1)
                col_point = [x,y]
                return col_point        
        
class FOV:
    def __init__(self, pos, n_rays):
        self.rays = []
        self.raw_data = [] #data that will be given to neural network
        self.pos = pos
        self.n_rays = n_rays
            
    def adjust_ray_angles(self, current_pos, boundary): #adjusting the direction of the ray based on where the snake head direction is pointed
        self.rays.clear()
        increment = ceil((boundary[0] - boundary[1]) / self.n_rays) #splitting the left boundary and right boundary by n_rays 
        for angle in range(boundary[0], boundary[1], -increment): #iterating from left bound to right boundary by increment value which gives us "n_rays" iterations
            self.rays.append(Ray(current_pos, angle))
    
    def update(self, surf, current_pos, boundary, snake_id, show):
        self.pos = current_pos
        self.raw_data.clear() #clearing list to update again
        self.adjust_ray_angles(current_pos, boundary) #updating direction 
        for ray in self.rays:
            #closest = float("inf") #keeping track of closest distance per ray
            for key in list(settings.BARRIERS_POS): #key could either be Wall, Food or snake id
                if key != list(settings.BARRIERS_POS.keys())[settings.N_GLOBAL_BARR]: #will break loop when reached global_barr to find own segment pos based on snake id
                    for wall in settings.BARRIERS_POS[key]:
                        if self.update_helper(ray, wall, key): break
                elif snake_id in settings.BARRIERS_POS:
                    for wall in settings.BARRIERS_POS[snake_id]: #iterating through positional values for specific snake id
                        if self.update_helper(ray, wall, "Segment"): break #breaks to next ray if intersection point was found
                    break
                else: 
                    settings.BARRIERS_POS[snake_id] = [] #adding snake id to dictionary if doesnt exist
                    break #breaking out of loop and restarting with newly updated dictionary
                
            for val in ray.barriers_distance.values(): #updating raw_data for neural network
                self.raw_data.append(val)
            if ray.closest_point is not None and show:
                if self.rays[0] is ray or self.rays[-1] is ray: #specifying color of outer rays to show the fov boundaries
                    pg.draw.line(surf, settings.YELLOW, (ray.x, ray.y), ray.closest_point, 3)
                else:            
                    pg.draw.line(surf, settings.WHITE, (ray.x, ray.y), ray.closest_point, 3)                   
                pg.draw.circle(surf, settings.RED, ray.closest_point, 10)  
        return self.raw_data
    
    def update_helper(self, ray, wall, k):
        intersect_points = ray.check_collision(wall)      
        if intersect_points is not None:
            ray_dx = ray.x - intersect_points[0]
            ray_dy = ray.y - intersect_points[1]
            distance = sqrt(ray_dx**2 + ray_dy**2) #getting distance b/w source pos of ray and intersecting point
            ray.update_barrier_distance(k, distance, intersect_points)
            return True
        else: 
            ray.update_barrier_distance(k, None, None)
            return False
            

