from math import pi
import random as r
import copy as cop
import time

import pygame
from pygame.locals import *

import pyceptron


height = 600
width = 600
#initialise pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pyceptron")
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((200, 200, 200))
screen.blit(background, (0, 0))



#preset colours
magenta = [255, 0, 255]
black = [0, 0 , 0]
white = [255, 255 , 255]


radius = int(height/10)
x_spacing = int(radius*2.5)
y_spacing = int(radius*2.5)


#Units = [3, 2]
#Patterns = [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 0.0]]
#Targets = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]


	
#below this line are things that will be run - above it are just declarations and definitions of classes, etc.
N = pyceptron.Network(Units, Patterns, Targets)

N.Train()
      
      
#refresh the screen
pygame.display.update()

#loop to fall into once the main stuff has been done
while (1):
  for event in pygame.event.get():
    if event.type == QUIT:
      quit()