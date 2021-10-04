import settings
import pygame as pg
from pygame import Vector2
from random import randint, choice

class Food(pg.sprite.Sprite):
    def __init__(self, width):
        pg.sprite.Sprite.__init__(self) #calling parent function init so we don't override it
        self.width = width
        self.speed = 0.1
        self.image = pg.Surface((self.width, self.width)) #setting dimensions of surface and making transparent
        self.image.fill(settings.YELLOW)        
        self.pos = Vector2(randint(self.width, settings.SCR_WIDTH-self.width), randint(self.width, settings.SCR_HEIGHT-self.width)) #setting at random position
        self.vel = Vector2(self.speed * choice((-1,1)), self.speed * choice((-1,1))) #selecting random velocity
        self.rect = self.image.get_rect() #fetching rectangle object that has dimensions of the image
        self.rect.center = self.pos #setting position of image in middle of window
    
    def update(self, snake):
        settings.WIN.blit(self.image, self.rect)        
        if self.rect.left < 0 or self.rect.right > settings.SCR_WIDTH:
            self.vel.x = self.vel.x * -1
        if self.rect.top < 0 or self.rect.bottom > settings.SCR_HEIGHT:
            self.vel.y = self.vel.y * -1
        self.pos += self.vel
        self.rect.center = self.pos
        snake.check_collisions(self)
    
    def reset(self):
        self.vel *= choice((-1,1))
        self.pos = randint(self.width, settings.SCR_WIDTH-self.width), randint(self.width, settings.SCR_HEIGHT-self.width) #resetting position of food to a random pos
        self.rect.center = self.pos #updating rect position of food