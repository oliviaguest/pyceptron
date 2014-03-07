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
white = [255, 255 , 255]

x_spacing = 8
y_spacing = 8
radius = 30

Units = [3, 2]
Patterns = [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 0.0]]
Targets = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]



 
class Unit(object):
  "A neural network unit: represented by a circle"
  def __init__(self, i, layer, x_offset, y_offset, colour = white, activation = 0.0, bias = 0.001, radius = radius, x_spacing = x_spacing, y_spacing = y_spacing):
    self.i = i
    self.j = layer
    self.colour = white
    self.radius = radius
    self.x = self.i * (x_spacing*self.radius) + x_offset
    self.y = self.j * (y_spacing*self.radius)  + y_offset
    self.activation = activation
    self.in_weights = 0.0
    self.in_activations = 0.0
    self.bias = bias     

    
  def Draw(self):
    pygame.draw.circle(screen, (self.colour[0], self.colour[1], self.colour[2]), (self.x, self.y), self.radius)


  def Clamp(self, value):
    self.activation =  value
    if self.activation == 1:
      self.colour = purple
    else:
      self.colour = white
    self.Draw()

  def Update(self):
    #print self.i
    #print self.j
    #print self.activation
    #print self.in_activations
    self.activation = self.in_activations - self.bias
    if self.activation  > 0:
      self.activation = 1
      self.colour = purple
    else:
      self.activation = 0
      self.colour = white
    self.Draw()
    self.in_activations = 0
    #print self.activation
    
       

class Weight(object):
  "A neural network connection weight: reprsented by a line"
  def __init__(self, unit_from, unit_to, colour = black, strength = 0.01):
    self.unit_from = unit_from
    self.unit_to =  unit_to
    self.colour = colour
    self.strength = strength

  def Draw(self):
    pygame.draw.line(screen, self.colour, (self.unit_from.x, self.unit_from.y), (self.unit_to.x, self.unit_to.y), int(self.strength * 100))

  def Propagate(self):
    "Send activations from self.unit_from to self.unit_to"
    self.unit_to.in_activations += self.unit_from.activation * self.strength
    #print self.unit_to.i
    #print self.unit_to.j
    #print self.unit_to.in_activations

  def Update(self, target, learning_rate):
    self.strength += learning_rate * (target - self.unit_to.activation)
    print"Output error:", target - self.unit_to.activation
    self.Draw()
    

class Network(object):
  "The network itself!"
  def __init__(self, units = Units, patterns = Patterns, targets = Targets):
    #create list to hold units in a neural network layer as another to keep the weights
    self.units = units
    self.layers =  len(self.units)
    self.layer = [None] * self.layers
    self.weights = [None] * self.layers
    self.patterns = patterns
    self.targets = targets
    self.learning_rate = 0.001
    for l in range(self.layers):
      self.layer[l] = [None] * self.units[l]
      if l > 0:
	#we want weights to only exist between two layers, so the 0th layer on its own cannot have any connections
	self.weights[l] = [None] * self.units[l-1]
	for unit_on_prev_layer in range(self.units[l-1]):
	  self.weights[l][unit_on_prev_layer] =  [None] * self.units[l]

    x_offset = int((width - (self.layers - 1) * x_spacing * radius) / 2.0)
	  
    #initialisation of network
    for l in range(self.layers):
      for unit_on_this_layer in range(self.units[l]):
	#cycle through the units to actually create the units for the layer we are on
	y_offset = int((height - ((self.units[l]-1) * y_spacing * radius)) / 2.0)
	self.layer[l][unit_on_this_layer] = Unit(l,unit_on_this_layer, x_offset, y_offset)
	self.layer[l][unit_on_this_layer].Draw()

	if l > 0:
	  #we want weights to only exist between two layers, so the 0th layer on its own cannot have any connections
	  for unit_on_prev_layer in range(self.units[l-1]):
	    #cycle through the units of the previous layer so we can connect them to their counterparts on this layer
	    self.weights[l][unit_on_prev_layer][unit_on_this_layer] = Weight(self.layer[l-1][unit_on_prev_layer], self.layer[l][unit_on_this_layer])
	    self.weights[l][unit_on_prev_layer][unit_on_this_layer].Draw()

  #def Draw(self, layers = -1):
    #if layers == -1:
     #layers = range(self.layers)
    #elif type(layers) == int:
      #layers = [layers]
      
    #for l in layers:
      #for unit_on_this_layer in range(self.units[l]):
	#self.layer[l][unit_on_this_layer].Draw()
      

  def Train(self):
    for x in range(1000):
      #clamp the input layer to a pattern p
      for p in range(len(self.patterns)):

	
	pygame.display.update()
	for event in pygame.event.get():
	  if event.type == QUIT:
	    quit()


	for unit_on_this_layer in range(self.units[0]):
	  self.layer[0][unit_on_this_layer].Clamp(self.patterns[p][unit_on_this_layer])


	for unit_on_this_layer in range(self.units[1]):
	  for unit_on_prev_layer in range(self.units[0]):
	    self.weights[1][unit_on_prev_layer][unit_on_this_layer].Propagate()
	    #self.weights[1][unit_on_prev_layer][unit_on_this_layer].strength += 1
	    #print self.weights[1][unit_on_prev_layer][unit_on_this_layer].strength
	    #self.weights[1][unit_on_prev_layer][unit_on_this_layer].Update(self.target[p][unit_on_this_layer])
          self.layer[1][unit_on_this_layer].Update()

	#for unit_on_this_layer in range(self.units[1]):
	  
	for unit_on_this_layer in range(self.units[1]): 
	  for unit_on_prev_layer in range(self.units[0]):
	    #self.weights[1][unit_on_prev_layer][unit_on_this_layer].Propagate()
	    #self.weights[1][unit_on_prev_layer][unit_on_this_layer].strength += 1
	    #print self.weights[1][unit_on_prev_layer][unit_on_this_layer].strength
	    self.weights[1][unit_on_prev_layer][unit_on_this_layer].Update(self.targets[p][unit_on_this_layer], self.learning_rate)


	pygame.display.update()

	time.sleep(0.5)



	
#below this line are things that will be run - above it are just declarations and definitions of classes, etc.
N = Network()

N.Train()
      
      
#refresh the screen
pygame.display.update()

#loop to fall into once the main stuff has been done
while (1):
  for event in pygame.event.get():
    if event.type == QUIT:
      quit()