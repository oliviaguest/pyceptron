from pyceptron import *


# Uncomment one of the followling patterns and targets. If you don't the network will be trained and run on a default pattern. One of these patterns is problematic, why?  ~ Olivia






#Patterns = [ ## NOT ##
            #[0.0],
            #[1.0],
           #]

#Targets = [
           #[1.0], #first target, corresponds to first pattern
           #[0.0],
         
          #]
          
          
#Patterns = [ ## OR ## 
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
          
          
#Patterns = [ ## AND ##
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

          
#Patterns = [ ## XOR ## 
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
          
          
N = Network(Patterns, Targets)

N.Train()

N.Run()
  

#loop to fall into once the main stuff has been done
while (1):
  for event in pygame.event.get():
    if event.type == QUIT:
      quit()