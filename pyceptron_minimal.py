from math import *
import random 
import copy as cop
import time
import matplotlib
import numpy
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

#f = lambda x: 0.0 if x < 0.0 else 1.0
def f(x):
  if x < 0.0:
    return 0.0
  else:
    return 1.0

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
    self.output_units = numpy.zeros(len(targets[0]))
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
    self.input_units_x =  numpy.ones(len(self.patterns[0]))
    self.input_units_y =  numpy.ones(len(self.patterns[0]))
    self.output_units_x =  numpy.ones(len(self.output_units))
    self.output_units_y =  numpy.ones(len(self.output_units))
    
    for i in range(len(self.patterns[0])):
      y_offset = int((height - ((len(self.patterns[0])-1) * (self.y_spacing + self.radius))) / 2.0)
      self.input_units_x[i] = 0 * (self.x_spacing+self.radius) + self.x_offset     # constant represents what layer they are on
      self.input_units_y[i] = i * (self.y_spacing+self.radius)  + y_offset

    for i in range(len(self.output_units)):
      y_offset = int((height - ((len(self.output_units)-1) * (self.y_spacing + self.radius))) / 2.0)
      self.output_units_x[i] = 1 * (self.x_spacing+self.radius) + self.x_offset    # constant represents what layer they are on
      self.output_units_y[i] = i * (self.y_spacing+self.radius)  + y_offset

    # More GUI stuff
    self.screen.blit(self.background, (0, 0))
    for i in range(len(self.patterns[0])):

      x1 = self.input_units_x[i]
      y1 = self.input_units_y[i]
      x2 = self.output_units_x[0]
      y2 = self.output_units_y[0]
      r1 = self.radius
      r2 = self.radius
      a = get_angle(x1, y1, x2, y2)
      pygame.draw.line(self.screen, black, (x1 + r1 * cos(a),  y1 + r1 * sin(a)), (x2 - r2 * cos(a), y2 - r2 * sin(a)), 1)
      pygame.draw.circle(self.screen, black, (int(x1), int(y1)), self.radius, 2)

    for i in range(len(self.output_units)):
      x2 = self.output_units_x[i]
      y2 = self.output_units_y[i]
      pygame.draw.circle(self.screen, black, (int(x2), int(y2)), self.radius, 2)

    pygame.display.update()
 

  def Draw(self):
    # GUI stuff
    
    for event in pygame.event.get():
      if event.type == QUIT:
        quit()
        pygame.display.update()
        
    for i in range(len(self.input_units)-1):

      x1 = self.input_units_x[i]
      y1 = self.input_units_y[i]
      x2 = self.output_units_x[0]
      y2 = self.output_units_y[0]
      r1 = self.radius
      r2 = self.radius

      rect = pygame.Rect(int(x1)-25, int(y1)-20, 50, 40)
      pygame.draw.rect(self.screen, [200, 200, 200], rect, 0)
      font=pygame.font.Font(None,50)
      text=font.render(str(self.input_units[i]), 1,black)
      self.screen.blit(text, (int(x1)-25, int(y1)-20))
      pygame.display.update(rect)
          
          
    for i in range(len(self.output_units)):
      x2 = self.output_units_x[i]
      y2 = self.output_units_y[i]
      rect = pygame.Rect(int(x2)-25, int(y2)-20, 78, 40)
      pygame.draw.rect(self.screen, [200, 200, 200], rect, 0)
      font=pygame.font.Font(None,50)
      text=font.render(str(self.output_units[i]), 1,black)
      self.screen.blit(text, (int(x2)-25, int(y2)-20))
      pygame.display.update(rect)


      
  def Train(self):
       
        x = self.input_units 
        w = self.weights
        h = self.learning_rate
        
        for n in range(100):
              for p in range(len(self.patterns)):
                        
                    for i in range(len(self.patterns[p])):    
                      x[i] = self.patterns[p][i]
                    print "x = ", x[0:2]
                    y = 0
                    for i in range(1+len(self.patterns[p])): 
                      y += x[i] * w[i]

                    self.output_units[0] = f(y)
                    print "y = ", y
                    error = self.targets[p][0] - self.output_units[0]
                    print "f(y) = ", self.output_units[0]

                    print "error = ", error
                    for i in range(1+len(self.patterns[p])): 
                      w[i] += h * error * x[i]

                    self.Draw()

                    
  def Run(self):
    x = self.input_units
    w = self.weights
    
    errors = 0.0
    while True:
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

                  self.Draw()


                  time.sleep(0.5)

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
  pygame.display.update()

  #loop to fall into once the main stuff has been done
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
         quit()

if __name__ == "__main__":
  Main()