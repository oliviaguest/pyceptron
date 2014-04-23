from math import *
import random 
import copy as cop
import time

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

  def Draw(self):
    if self.unit_from:
      x1 = self.unit_from.x
      y1 = self.unit_from.y
      x2 = self.unit_to.x
      y2 = self.unit_to.y
      r1 = self.unit_from.radius
      r2 = self.unit_to.radius
      a = get_angle(x1, y1, x2, y2)
      pygame.draw.line(self.screen, self.colour, (x1 + r1 * cos(a),  y1 + r1 * sin(a)), (x2 - r2 * cos(a), y2 - r2 * sin(a)), 1)


  def Propagate(self):
    "Send activations from self.unit_from to self.unit_to"
    self.unit_to.in_activations += self.unit_from.activation * self.strength

  def Update(self, target, learning_rate, pattern=None, batch = True):
    error = target - self.unit_to.activation
    if pattern ==None:
          self.d_strength -= learning_rate * error 
          print"Output error:", error,
          print "Bias:", self.strength
    else:
          self.d_strength -= learning_rate * error * self.unit_from.activation
          
          print"Output error:", error,
          print "Weight:", self.strength
          #print "Error:", error,
          #print "Unit from:", self.unit_from.activation
    #self.strength += learning_rate * self.unit_to.activation

    #print "Learning rate:", learning_rate
    #print "Output activation:", self.unit_to.activation
    self.Draw()
    return error
  def Apply_batch(self):
    self.strength += self.d_strength
    self.d_strength = 0.0
    
class Bias(Weight):
  pass
    
  #def Update(self, target, learning_rate):
    #error = target - self.unit_to.activation
    #self.strength += learning_rate * error
    ##self.strength += learning_rate * self.unit_to.activation
    #print"Output error:", error,
    #print "Weight:", self.strength
    ##print "Learning rate:", learning_rate
    ##print "Output activation:", self.unit_to.activation
    ##self.Draw()
    #return error
class Network(object):
  "The network itself!"
  def __init__(self, patterns, targets,  units = [1, 1], learning_rate = 0.015, height = 600, width = 600):
    

    #initialise pygame
    #pygame.init()
    #self.screen = pygame.display.set_mode((width, height))
    #pygame.display.set_caption("Pyceptron")
    #self.background = pygame.Surface(self.screen.get_size())
    #self.background = self.background.convert()
    #self.background.fill([200, 200, 200])
    #self.screen.blit(self.background, (0, 0))




    self.units = units
    self.patterns = patterns
    self.targets = targets

    if len(patterns[0]) != units[0]:
      self.units[0] = len(patterns[0])
    if len(targets[0]) != units[-1]:
      self.units[-1] = len(targets[0])
    self.layers =  len(self.units)
    self.layer = [0.0] * self.layers
    self.weights = [1.0] * self.layers
    self.biases = [0] * (self.layers)
    self.learning_rate = learning_rate
    for l in range(self.layers):
      self.layer[l] = [0] * self.units[l]
      if l > 0:
        #we want weights to only exist between two layers, so the 0th layer on its own cannot have any connections
        self.weights[l] = [0] * self.units[l-1]
        for unit_on_prev_layer in range(self.units[l-1]):
          self.weights[l][unit_on_prev_layer] =  [0] * self.units[l]
        self.biases[l] = [0] * self.units[l]

  

    radius = int( height/ (3* max( max( self.units ), self.layers) ))
    x_spacing = int(radius*1.5)
    y_spacing = int(radius*1.5)

    x_offset = int((width - (self.layers - 1) * (x_spacing + radius)) / 2.0)
    self.weights = [0, 0, 0]
    self.errors = []
    self.learning_rate = 0.2

    ##initialisation of network
    #for l in range(self.layers):
      #for unit_on_this_layer in range(self.units[l]):
       ##cycle through the units to actually create the units for the layer we are on
       #y_offset = int((height - ((self.units[l]-1) * (y_spacing + radius))) / 2.0)
       #self.layer[l][unit_on_this_layer] = Unit(l, unit_on_this_layer, x_offset, y_offset, black, 0.0, radius, x_spacing, y_spacing, screen = self.screen)
       #self.layer[l][unit_on_this_layer].Draw()

       #if l > 0:
         ##we want weights to only exist between two layers, so the 0th layer on its own cannot have any connections
          #for unit_on_prev_layer in range(self.units[l-1]):
            ##cycle through the units of the previous layer so we can connect them to their counterparts on this layer
            #self.weights[l][unit_on_prev_layer][unit_on_this_layer] = Weight(self.layer[l-1][unit_on_prev_layer], self.layer[l][unit_on_this_layer], strength = random.gauss(0.5, 0.01),  screen = self.screen)
            #self.weights[l][unit_on_prev_layer][unit_on_this_layer].Draw()
          #self.biases[l][unit_on_this_layer] = Bias(None, self.layer[l][unit_on_this_layer],strength = random.gauss(-1.0, 0.01))
          #self.layer[l][unit_on_this_layer].Set_bias(self.biases[l][unit_on_this_layer])

  def Run(self):
        x = self.units # last unit is bias
        w = self.weights
        x.append(1.0)
        w.append(0.0)
        errors = 0.0
        h = 0.4
        #while True:
        for n in range(100):
              errors = 0.0
              for p in range(len(self.patterns)):
                    #print "Running: Input Pattern:", self.patterns[p],
                    #self.screen.blit(self.background, (0, 0))

                    #for event in pygame.event.get():
                      #if event.type == QUIT:
                        #quit()
                        
                    for i in range(len(self.patterns[p])):    
                      x[i] = self.patterns[p][i]
                    print "x = ", x  
                    y = 0
                    for i in range(1+len(self.patterns[p])): 
                      y += x[i] * w[i]
                  
                    print "y = ", y
                    error = self.targets[p][0] - f(y)
                    print "f(y) = ", f(y)

                    print error
                    #errors.append(error)
                    errors += error
                    print errors
                    for i in range(1+len(self.patterns[p])): 
                      w[i] += h * error * x[i]
                    print "w = ", w
                
              #if errors == 0.0:
                    #break;
        print "Done training"      

        for p in range(len(self.patterns)):
            for i in range(len(self.patterns[p])):    
              x[i] = self.patterns[p][i]
            print "x = ", x  
            y = 0
            for i in range(1+len(self.patterns[p])): 
              y += x[i] * w[i]

            print "y = ", y
            error = self.targets[p][0] - f(y)
            print "f(y) = ", f(y)

            print error
            #errors.append(error)
            errors += error 
            #print("{}: {} -> {}".format(x, y, f(y)))

            #for unit_on_this_layer in range(self.units[0]):
              #self.layer[0][unit_on_this_layer].Clamp(self.patterns[p][unit_on_this_layer])

            #for unit_on_this_layer in range(self.units[1]):
              #for unit_on_prev_layer in range(self.units[0]):
                #self.weights[1][unit_on_prev_layer][unit_on_this_layer].Propagate()
                #self.weights[1][unit_on_prev_layer][unit_on_this_layer].Draw()
            
            #for unit_on_this_layer in range(self.units[1]):
              #self.layer[1][unit_on_this_layer].Update()

            #print "Output:", self.layer[-1][-1].activation
            
            
            #pygame.display.update()
            #time.sleep(1)

  def Train(self):
    error = 1.0
    #for x in range(5000):
    #while True:
    while error != 0.0:

      error = 0.0
      #clamp the input layer to a pattern p
      for p in range(len(self.patterns)):
          self.screen.blit(self.background, (0, 0))

          for event in pygame.event.get():
            if event.type == QUIT:
              quit()

          for unit_on_this_layer in range(self.units[0]):
            self.layer[0][unit_on_this_layer].Clamp(self.patterns[p][unit_on_this_layer])

          for unit_on_this_layer in range(self.units[1]):
            for unit_on_prev_layer in range(self.units[0]):
              self.weights[1][unit_on_prev_layer][unit_on_this_layer].Propagate()

          for unit_on_this_layer in range(self.units[1]):
            self.layer[1][unit_on_this_layer].Update()
      
          for unit_on_this_layer in range(self.units[1]):
              error += fabs(self.biases[1][unit_on_this_layer].Update(self.targets[p][unit_on_this_layer], self.learning_rate))
              for unit_on_prev_layer in range(self.units[0]):
                error += fabs(self.weights[1][unit_on_prev_layer][unit_on_this_layer].Update(self.targets[p][unit_on_this_layer], self.learning_rate, pattern =self.patterns[p][unit_on_prev_layer]))
          #time.sleep(1)
              print "Input:", self.patterns[p],
              print "Target:", self.targets[p][unit_on_this_layer],
              print unit_on_this_layer,
              print "Output:", self.layer[1][unit_on_this_layer].activation

          pygame.display.update()
          
      for unit_on_this_layer in range(self.units[1]):
          self.biases[1][unit_on_this_layer].Apply_batch()
          for unit_on_prev_layer in range(self.units[0]):
             self.weights[1][unit_on_prev_layer][unit_on_this_layer].Apply_batch()    
      error /= len(self.patterns)
      print "Network error:", error




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
          
#Patterns=[[0.5,1.5], [-0.5, 0.5], [0.5, 0.5]] 
#Targets=[[1.0], [0], [1]]
          
#Patterns = [
            #[-1, -1], #first pattern
            #[-1, 1.0],
            #[1.0, -1],
            #[1.0, 1.0]
           #]

#Targets = [
           #[0], #first target, corresponds to first pattern
           #[0],
           #[0],
           #[1.0]
          #]
          
#Patterns = [
            #[-1.0], #first pattern
           
            #[1.0]
           #]

#Targets = [
          
           #[1.0],
           #[0.0]
          #]
#Patterns = [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 0.0]]
#Targets = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]

def Main():
  #below this line are things that will be run - above it are just declarations and definitions of classes, etc.
  N = Network(Patterns, Targets)

  #N.Train()
  
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