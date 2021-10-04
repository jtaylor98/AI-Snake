from math import floor, pow, ceil
from random import choice, randint, uniform
import numpy as np
from pygame import Vector2
import pygame as pg
import string

"""pg.init()
win = pg.display.set_mode((800,800))
pg.display.set_caption("scratch")
win.fill((91,90,90))"""

"""run = True
while run:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      run = False
  
  surface = pg.Surface((100, 100), pg.SRCALPHA)
  #surface.fill((243,27,99))
  pg.draw.circle(surface, (30,224,33,2), (50,50), 50)
  win.blit(surface, (250,250))

  pg.display.update()"""


count = 1
for _ in range(10):
  count = (count + 1) % 2
  print(count)