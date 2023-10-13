# This file contains all the constants needed to set up the project. Set them as you prefer

SPEED=1 # starting speed of both police and car
COUNTER=100000 # number of points to be scored before increasing the speed of the police cars

ENVSIZE=(20,20) # height and width of the environment
CARSIZE=(5,4) # height and width of the car. A good choice to have something realistic is ~1/4 of the height and ~1/8 of the width of the environment
PACMAN=False # if True, the car is a pacman and can exit the environment from one side and re-enter from the opposite side
QSIZE=432

AGENT="SARSA" # agent to be used for training: SARSA, Qlearning, ExpectedSARSA

IMPORTPOLICY="goodpol3.txt" # If you want to use a old policy, set with the name of the file containing the policy. Otherwise, set with 0 to train a new policy
EXPORTPOLICY=0 # If you want to save the learned policy in a txt file, set with the name of the file. Otherwise, set with 0
SAVESCORES=0 # If you want to save the scores in a txt file, set with the name of the file. Otherwise, set with 0

NSTEPS=1000000 # number of steps to be played 
RENDERSTEPS=False # if True, the environment is printed in the terminal at each step
PLOTSTEPS=True # if True, the environment is plotted and animated (the animation won't stop at NSTEPS in this case, but will continue until the user closes the plot)
WAIT=1 # time in milliseconds between each step in the case PLOTSTEPS=True

