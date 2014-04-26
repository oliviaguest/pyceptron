from pyceptron import *

#Patterns = [
            #[0.0, 0.0],
            #[1.0, 1.0],
           #]

#Targets = [
           #[1.0], #first target, corresponds to first pattern
           #[0.0],
         
          #]
          
          
#Patterns = [
            #[0.0, 0.0],
            #[0.0, 1.0],
            #[1.0, 0.0],
            #[1.0, 1.0]
           #]

#Targets = [
           #[0.0], #first target, corresponds to first pattern
           #[1.0],
           #[1.0],
           #[1.0],
         
          #]
          
#Patterns = [
            #[0.0, 0.0],
            #[0.0, 1.0],
            #[1.0, 0.0],
            #[1.0, 1.0]
           #]

#Targets = [
           #[0.0], #first target, corresponds to first pattern
           #[1.0],
           #[1.0],
           #[0.0],
         
          #]          
#Patterns = [
            #[0.0, 0.0],
            #[0.0, 1.0],
            #[1.0, 0.0],
            #[1.0, 1.0]
           #]

#Targets = [
           #[0.0], #first target, corresponds to first pattern
           #[0.0],
           #[0.0],
           #[1.0],
         
          #]  

N = Network(Patterns, Targets)

N.Train()

N.Run()
  

#loop to fall into once the main stuff has been done
while (1):
  for event in pygame.event.get():
    if event.type == QUIT:
      quit()