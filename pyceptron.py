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
  def __init__(self, layer, i, x_offset, y_offset, colour = black, activation = 0.0, bias = 0.001, radius = 60, x_spacing = 150, y_spacing = 150):
    self.layer = layer
    self.i = i
    self.colour = colour
    self.radius = radius
    self.x = self.layer * (x_spacing+self.radius) + x_offset
    self.y = self.i * (y_spacing+self.radius)  + y_offset
    self.x_spacing = x_spacing
    self.y_spacing = y_spacing
    self.activation = activation
    self.in_weights = 0.0
    self.in_activations = 0.0
    self.bias = bias     

    
  def Draw(self):
    if self.activation > 0.0:
      width = 2
    else:
      width = 0
    pygame.draw.circle(screen, (self.colour[0], self.colour[1], self.colour[2]), (self.x, self.y), self.radius, width)

  def Colour(self):
    self.colour[1] = 255*self.activation

  def Clamp(self, value):
    self.activation =  value
    #self.Colour()
    self.Draw()

  def Update(self):
    #print self.i
    #print self.j
    #print self.activation
    #print self.in_activations
    self.activation = self.in_activations - self.bias
    if self.activation  > 0:
      self.activation = 1
    else:
      self.activation = 0
    #self.Colour()
    self.Draw()
    self.in_activations = 0
    #print self.activation
    
       

class Weight(object):
  "A neural network connection weight: reprsented by a line"
  def __init__(self, unit_from, unit_to, colour = black, strength = 0.0):
    self.unit_from = unit_from
    self.unit_to =  unit_to
    self.colour = colour
    self.strength = strength

  def Draw(self):
    line_width = int(self.strength * 1000)
    if line_width > 8:
      line_width = 8
    if line_width < 1:
      line_width = 1

    pygame.draw.line(screen, self.colour, (self.unit_from.x, self.unit_from.y), (self.unit_to.x, self.unit_to.y), line_width)

  def Propagate(self):
    "Send activations from self.unit_from to self.unit_to"
    self.unit_to.in_activations += self.unit_from.activation * self.strength

  def Update(self, target, learning_rate):
    error = target - self.unit_to.activation
    self.strength += learning_rate * error
    print"Output error:", error,
    print "Weight:", self.strength
    self.Draw()
    return error
    

class Network(object):
  "The network itself!"
  def __init__(self, patterns, targets,  units = [1, 1], learning_rate = 0.001, height = 600, width = 600, background = 0):
    self.units = units
    self.patterns = patterns
    self.targets = targets

    if len(patterns[0]) != units[0]:
      self.units[0] = len(patterns[0])
    if len(targets[0]) != units[-1]:
      self.units[-1] = len(targets[0])
    self.layers =  len(self.units)
    self.layer = [None] * self.layers
    self.weights = [None] * self.layers
    self.learning_rate = learning_rate
    self.background = background
    for l in range(self.layers):
      self.layer[l] = [None] * self.units[l]
      if l > 0:
	#we want weights to only exist between two layers, so the 0th layer on its own cannot have any connections
	self.weights[l] = [None] * self.units[l-1]
	for unit_on_prev_layer in range(self.units[l-1]):
	  self.weights[l][unit_on_prev_layer] =  [None] * self.units[l]

	  
<<<<<<< HEAD
    radius = int(height/max(units))
    x_spacing = int(radius*2.5)
    y_spacing = int(radius*2.5)
=======
    radius = int(height/(max(units)*3))
    x_spacing = int(radius*1.5)
    y_spacing = int(radius*1.5)
>>>>>>> cd76a75c44ff30ed5690879fd524210d2d76d033
    x_offset = int((width - (self.layers - 1) * (x_spacing + radius)) / 2.0)
	  
    #initialisation of network
    for l in range(self.layers):
      for unit_on_this_layer in range(self.units[l]):
	#cycle through the units to actually create the units for the layer we are on
	y_offset = int((height - ((self.units[l]-1) * (y_spacing + radius))) / 2.0)
	self.layer[l][unit_on_this_layer] = Unit(l, unit_on_this_layer, x_offset, y_offset, black, 0.0, 0.001, radius, x_spacing, y_spacing)
	self.layer[l][unit_on_this_layer].Draw()

	if l > 0:
	  #we want weights to only exist between two layers, so the 0th layer on its own cannot have any connections
	  for unit_on_prev_layer in range(self.units[l-1]):
	    #cycle through the units of the previous layer so we can connect them to their counterparts on this layer
	    self.weights[l][unit_on_prev_layer][unit_on_this_layer] = Weight(self.layer[l-1][unit_on_prev_layer], self.layer[l][unit_on_this_layer])
	    self.weights[l][unit_on_prev_layer][unit_on_this_layer].Draw()


  def Train(self):
    error = 1.0
    #for x in range(1000):
    while error != 0.0:
      error = 0.0
      #clamp the input layer to a pattern p
      for p in range(len(self.patterns)):
        screen.blit(self.background, (0, 0))

	for event in pygame.event.get():
	  if event.type == QUIT:
	    quit()

	for unit_on_this_layer in range(self.units[0]):
	  self.layer[0][unit_on_this_layer].Clamp(self.patterns[p][unit_on_this_layer])

	for unit_on_this_layer in range(self.units[1]):
	  for unit_on_prev_layer in range(self.units[0]):
	    self.weights[1][unit_on_prev_layer][unit_on_this_layer].Propagate()
          self.layer[1][unit_on_this_layer].Update()
	  
	for unit_on_this_layer in range(self.units[1]): 
	  for unit_on_prev_layer in range(self.units[0]):
	    error += self.weights[1][unit_on_prev_layer][unit_on_this_layer].Update(self.targets[p][unit_on_this_layer], self.learning_rate)
       
	pygame.display.update()
	
	

	#time.sleep(0.5)

Patterns = [
	    [1.0, 0.0],
	    [0.0, 1.0],
	    [0.0, 0.0],
	    [1.0, 1.0]
	   ]
Targets = [
	    [1.0],
	    [1.0],
	    [0.0],
	    [1.0]
	  ]
#Patterns = [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 0.0]]
#Targets = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]

def Main():
  #below this line are things that will be run - above it are just declarations and definitions of classes, etc.
  N = Network(Patterns, Targets, background = background)

  N.Train()
	
	
  #refresh the screen
  pygame.display.update()

  #loop to fall into once the main stuff has been done
  while (1):
    for event in pygame.event.get():
      if event.type == QUIT:
	quit()

if __name__ == "__main__":
  Main()