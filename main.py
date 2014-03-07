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



#preset colours
purple = [255, 20, 255]
black = [0, 0 , 0]

x_spacing = 8
y_spacing = 8
radius = 30

Units = [3, 2]
x_offset = int((width - ((len(Units)-1) * x_spacing * radius)) / 2.0)
y_offset = int((height - ((max(Units)-1) * y_spacing * radius)) / 2.0)
  
class Unit(object):
  "A neural network unit: represented by a circle"
  def __init__(self, i, layer, colour = purple, activation = 0.0):
    self.i = i
    self.j = layer
    self.colour = purple
    self.radius = radius
    self.x = self.i * (x_spacing*self.radius) + x_offset
    self.y = self.j * (y_spacing*self.radius)  + y_offset
    self.activation = activation
    
  def Draw(self):
    pygame.draw.circle(screen, (self.colour[0], self.colour[1], self.colour[2]), (self.x, self.y), self.radius)

class Weight(object):
  "A neural network connection weight: reprsented by a line"
  def __init__(self, unit_from, unit_to, colour = black, strength = 0.0):
    self.unit_from = unit_from
    self.unit_to =  unit_to
    self.colour = colour
    self.strength = strength

  def Draw(self):
    pygame.draw.line(screen, self.colour, (self.unit_from.x, self.unit_from.y), (self.unit_to.x, self.unit_to.y), 1)

class Network(object):
  "The network itself!"
  def __init__(self, units = Units):
    #create list to hold units in a neural network layer as another to keep the weights
    self.units = units
    self.layers =  len(self.units)
    self.layer = [None] * self.layers
    self.weights = [None] * self.layers
    for l in range(self.layers):
      self.layer[l] = [None] * self.units[l]
      if l > 0:
	#we want weights to only exist between two layers, so the 0th layer on its own cannot have any connections
	self.weights[l] = [None] * self.units[l-1] * self.units[l]

    #initialisation of network
    for l in range(self.layers):
      for unit_on_this_layer in range(self.units[l]):
	#cycle through the units to actually create the units for the layer we are on
	self.layer[l][unit_on_this_layer] = Unit(l,unit_on_this_layer)
	self.layer[l][unit_on_this_layer].Draw()

	if l > 0:
	  #we want weights to only exist between two layers, so the 0th layer on its own cannot have any connections
	  for unit_on_prev_layer in range(self.units[l-1]):
	    #cycle through the units of the previous layer so we can connect them to their counterparts on this layer
	    self.weights[l][unit_on_this_layer] = Weight(self.layer[l-1][unit_on_prev_layer], self.layer[l][unit_on_this_layer])
	    self.weights[l][unit_on_this_layer].Draw()

  def Learn(self):
    #self.blah blah
    None
    

N = Network()
#N.Draw();
      
      
#refresh the screen
pygame.display.update()

#loop to fall into once the main stuff has been done
while (1):
  for event in pygame.event.get():
    if event.type == QUIT:
      quit()