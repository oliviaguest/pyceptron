#! /usr/bin/env python
from math import pi
import random as r
import copy as cop
import time



#import pygame
import pygame
from pygame.locals import *

#initialise pygame
pygame.init()
screen = pygame.display.set_mode((569, 569))
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

  
class Unit(object):
  "A neural network unit: represented as a circle graphically, and as an object in Python"
  def __init__(self, i, j):
    self.i = i
    self.j = j

#initialisation of network
for i in range(layers):
  for j in range(Units[i]):
    Layer[i][j] = Unit(i,j)

#refresh the screen
pygame.display.update()

#loop to fall into once the main stuff has been done
while (1):
  for event in pygame.event.get():
    if event.type == QUIT:
      quit()