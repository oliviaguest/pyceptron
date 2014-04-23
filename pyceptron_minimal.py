from math import *
import random 
import copy as cop
import time
import matplotlib
import numpy
#import pygame
import pygame
from pygame.locals import *


def get_angle(x1, y1, x2, y2):
  dx = x2 - x1
  dy= y2 - y1  
  return atan2(dy,dx)



#preset colours
magenta = [255, 0, 255]
black = [0, 0 , 0]
white = [255, 255 , 255]

f = lambda x: 0.0 if x < 0.0 else 1.0


 
class Unit(object):
  "A neural network unit: represented by a circle"
  def __init__(self, layer, i, x_offset, y_offset, colour = black, activation = 0.0, radius = 60, x_spacing = 150, y_spacing = 150, screen = None):
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
    self.screen = screen
    #self.prev_activation = 0.0
    #self.bias = -2     

    
  def Draw(self):
    #if self.activation > 0.0:
      #width = 2
      #self.colour[0] *= self.activation
      #self.colour[1] *=self.activation
      #self.colour[2] *=self.activation
    #else:
    width = 2
      #self.colour = black  

    #print self.i, self.layer,  self.activation  
    pygame.draw.circle(self.screen, (self.colour[0], self.colour[1], self.colour[2]), (self.x, self.y), self.radius, width)

    #font=pygame.font.Font(None,10) 
    #scoretext=font.render(str(self.prev_activation), 1,magenta)
    font=pygame.font.Font(None,50) 

    text=font.render(str(self.activation), 1,black)
    self.screen.blit(text, (self.x-25, self.y-20))

    
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
    #self.prev_activation = self.activation
    self.activation = self.in_activations - self.bias.strength
    if self.activation  > 0:
      self.activation = 1.0
    else:
      self.activation = 0.0
    #self.Colour()
    self.Draw()
    self.in_activations = 0
    print "Unit activation = ", self.activation,
    print self.in_activations, self.bias.strength
    
  def Set_bias(self, bias):
    self.bias = bias
       

class Weight(object):
  "A neural network connection weight: represented by a line"
  def __init__(self, unit_from, unit_to, colour = black, strength = 0.001, screen = None):
    self.unit_from = unit_from
    self.unit_to =  unit_to
    self.colour = colour
    self.strength = strength
    self.screen = screen
    self.d_strength = 0.0



    

class Network(object):
  "The network itself!"
  def __init__(self, patterns, targets,  learning_rate = 0.02, height = 600, width = 600):
    

    #Initialise pygame
    pygame.init()
    self.screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pyceptron")
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill([200, 200, 200])
    self.screen.blit(self.background, (0, 0))



    # Initialising network
    self.input_units =  numpy.ones(len(patterns[0])+1)
    self.output_units = numpy.zeros(len(targets))
    self.patterns = patterns
    self.targets = targets
    self.learning_rate = learning_rate
    self.weights = numpy.zeros(len(self.input_units))
    self.errors = []
    self.learning_rate = 0.2
    self.layers = 2
  
    # GUI stuff
    self.radius = int( height/ (3* max(len(self.input_units), len(self.output_units)) ))
    self.x_spacing = int(self.radius*1.5)
    self.y_spacing = int(self.radius*1.5)
    self.x_offset = int((width - (self.layers - 1) * (self.x_spacing + self.radius)) / 2.0)


  def Train(self):
        x = self.input_units 
        w = self.weights
        h = self.learning_rate
        for n in range(100):
              errors = 0.0
              for p in range(len(self.patterns)):
                    self.screen.blit(self.background, (0, 0))

                    for event in pygame.event.get():
                      if event.type == QUIT:
                        quit()
                        
                    for i in range(len(self.patterns[p])):    
                      x[i] = self.patterns[p][i]
                    print "x = ", x[0:2]
                    y = 0
                    for i in range(1+len(self.patterns[p])): 
                      y += x[i] * w[i]
                  
                    print "y = ", y
                    error = self.targets[p][0] - f(y)
                    print "f(y) = ", f(y)

                    print "error = ", error
                    for i in range(1+len(self.patterns[p])): 
                      w[i] += h * error * x[i]

                    # GUI stuff

                    x1 = self.unit_from.x
                    y1 = self.unit_from.y
                    x2 = self.unit_to.x
                    y2 = self.unit_to.y
                    r1 = self.unit_from.radius
                    r2 = self.unit_to.radius
                    a = get_angle(x1, y1, x2, y2)
                    pygame.draw.line(self.screen, self.colour, (x1 + r1 * cos(a),  y1 + r1 * sin(a)), (x2 - r2 * cos(a), y2 - r2 * sin(a)), 1)

        print "Done training"
        
  def Run(self):
    x = self.input_units
    w = self.weights
    
    errors = 0.0
    h = 0.4  
    for p in range(len(self.patterns)):
            for i in range(len(self.patterns[p])):    
              x[i] = self.patterns[p][i]
            print "x = ", x[0:2]  
            y = 0
            for i in range(1+len(self.patterns[p])): 
              y += x[i] * w[i]

            print "y = ", y
            error = self.targets[p][0] - f(y)
            print "f(y) = ", f(y)

            print "error = ", error
            



       #time.sleep(0.5)

Patterns = [
            [0.0, 0.0],
            [0.0, 1.0],
            [1.0, 0.0],
            [1.0, 1.0]
           ]

Targets = [
           [0.0], #first target, corresponds to first pattern
           [0.0],
           [0.0],
           [1.0],
         
          ]  
          

def Main():
  #below this line are things that will be run - above it are just declarations and definitions of classes, etc.
  N = Network(Patterns, Targets)

  N.Train()
  
  N.Run()

  #refresh the screen
  #pygame.display.update()

  #loop to fall into once the main stuff has been done
  #while True:
    #for event in pygame.event.get():
      #if event.type == QUIT:
         #quit()

if __name__ == "__main__":
  Main()