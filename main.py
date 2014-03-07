#! /usr/bin/env python
from math import pi
import random as r
import copy as cop
import time

#import pygame
import pygame
from pygame.locals import *

height = 600
width = height
#initialise pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pyceptron")
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((200, 200, 200))
screen.blit(background, (0, 0))

#create list to hold units in a neural network layer
Units = [3, 2]
layers = 2
Layer = [None] * layers
for i in range(layers):
  Layer[i] = [None] * Units[i]

#preset colours
purple = [255, 20, 255]
offset = int(width/10.0)
x_spacing = 8
y_spacing = 8
radius = 30
  
class Unit(object):
  "A neural network unit: represented as a circle graphically, and as an object in Python"
  def __init__(self, i, j):
    self.i = i
    self.j = j
    self.colour = purple
    self.radius = radius
    self.x = self.i * (x_spacing*self.radius) + offset
    self.y = self.j * (y_spacing*self.radius)  + offset
    
  def Draw(self):
    pygame.draw.circle(screen, (self.colour[0], self.colour[1], self.colour[2]), (self.x, self.y), self.radius)

#initialisation of network
for i in range(layers):
  for j in range(Units[i]):
    Layer[i][j] = Unit(i,j)
    Layer[i][j].Draw()

#refresh the screen
pygame.display.update()

#loop to fall into once the main stuff has been done
while (1):
  for event in pygame.event.get():
    if event.type == QUIT:
      quit()