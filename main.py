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

#create list to hold units in a neural network layer as another to keep the weights
Units = [3, 2]
layers = 2
Layer = [None] * layers
Weights = [None] * layers
for l in range(layers):
  Layer[l] = [None] * Units[l]
  if l > 0:
    #we want weights to only exist between two layers, so the 0th layer on its own cannot have any connections
    Weights[l] = [None] * Units[l-1] * Units[l]

#preset colours
purple = [255, 20, 255]
black = [0, 0 , 0]
offset = int(width/10.0)
x_spacing = 8
y_spacing = 8
radius = 30
  
class Unit(object):
  "A neural network unit: represented by a circle"
  def __init__(self, i, layer, colour = purple, activation = 0.0):
    self.i = i
    self.j = layer
    self.colour = purple
    self.radius = radius
    self.x = self.i * (x_spacing*self.radius) + offset
    self.y = self.j * (y_spacing*self.radius)  + offset
    self.activation = activation;
    
  def Draw(self):
    pygame.draw.circle(screen, (self.colour[0], self.colour[1], self.colour[2]), (self.x, self.y), self.radius)

class Weight(object):
  "A neural network connection weight: reprsented by a line"
  def __init__(self, unit_from, unit_to, strength = 0, colour = black):
    self.unit_from = unit_from
    self.unit_to =  unit_to
    self.colour = colour
    self.strength = strength

  def Draw(self):
    pygame.draw.line(screen, self.colour, (self.unit_from.x, self.unit_from.y), (self.unit_to.x, self.unit_to.y), 1)
    
#initialisation of network
for l in range(layers):
  for unit_on_this_layer in range(Units[l]):
    #cycle through the units to actually create the units for the layer we are on
    Layer[l][unit_on_this_layer] = Unit(l,unit_on_this_layer)
    Layer[l][unit_on_this_layer].Draw()

    if l > 0:
      #we want weights to only exist between two layers, so the 0th layer on its own cannot have any connections
      for unit_on_prev_layer in range(Units[l-1]):
	#cycle through the units of the previous layer so we can connect them to their counterparts on this layer
	Weights[l][unit_on_this_layer] = Weight(Layer[l-1][unit_on_prev_layer], Layer[l][unit_on_this_layer])
	Weights[l][unit_on_this_layer].Draw()
      
#refresh the screen
pygame.display.update()

#loop to fall into once the main stuff has been done
while (1):
  for event in pygame.event.get():
    if event.type == QUIT:
      quit()