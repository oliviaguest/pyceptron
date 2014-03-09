from math import pi
import random as r
import copy as cop
import time

import pygame
from pygame.locals import *

import pyceptron

#preset colours
magenta = [255, 0, 255]
black = [0, 0 , 0]
white = [255, 255 , 255]
blue = [0, 0, 255]
red = [255, 0, 0]
green = [0, 255, 0]
yellow = [255, 255, 0]

height = 200
width = 200
#initialise pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My unit!")
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(magenta)
screen.blit(background, (0, 0))

#varibles for position and size of our unit
radius = int(height/10)
x_spacing = int(radius*2.5)
y_spacing = int(radius*2.5)
x_offset = int(width / 2.0)
y_offset = int(height / 2.0)

#here we are defining our unit
My_unit = pyceptron.Unit(0, 0, x_offset, y_offset, colour = white, radius = 40)

for i in range(10):
  My_unit.colour = white
  My_unit.Draw()    
  pygame.display.update()
  
  #try commenting this out to see what it does
  for event in pygame.event.get():
    if event.type == QUIT:
      quit()
  
  #ditto
  time.sleep(0.5)

  My_unit.colour = black
  My_unit.Draw()    
  pygame.display.update()
  
  #ditto
  for event in pygame.event.get():
    if event.type == QUIT:
      quit()
    
  time.sleep(0.5)


#loop to fall into once the main stuff has been done
while (1):
  for event in pygame.event.get():
    if event.type == QUIT:
      quit()