from math import pi
import random as r
import copy as cop
import time

#import pygame
import pygame
from pygame.locals import *




height = 600
width = 600
#initialise pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pyceptron")
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill([200, 200, 200])
screen.blit(background, (0, 0))



#preset colours
magenta = [255, 0, 255]
black = [0, 0 , 0]
white = [255, 255 , 255]



 
class Unit(object):
  "A neural network unit: represented by a circle"
  def __init__(self, x, y, colour, radius):

    self.colour = colour
    self.radius = radius
    self.x =  x
    self.y =  y
    
  def Draw(self):
    pygame.draw.circle(screen, (self.colour[0], self.colour[1], self.colour[2]), (self.x, self.y), self.radius)

 
   
#below this line are things that will be run - above it are just declarations and definitions of classes, etc.
My_unit = Unit(50, 50, magenta, 40)
My_unit.Draw()      
#refresh the screen
pygame.display.update()

#loop to fall into once the main stuff has been done
while (1):
  for event in pygame.event.get():
    if event.type == QUIT:
      quit()
